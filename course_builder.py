"""Reusable, idempotent course builder for CourseStack.

Give it a COURSE spec (see SPEC SCHEMA below) and it will create/update the whole
course — content, chapters, lessons, commented solutions, quizzes — attach a lab
system to every lab, and put each chapter in the intended order. Safe to re-run:
existing items are matched by name and updated in place instead of duplicated.

    from course_builder import build
    from my_course_spec import COURSE
    build(COURSE)

SPEC SCHEMA
-----------
COURSE = {
  "title": str,
  "subtitle": str,
  # optional: provision (or reuse) an individual lab machine, attached to labs
  "lab_system": {"name": "linuxbox", "image_id": "<uuid>", "size": "micro"},
  "modules": [
    {
      "name": "Módulo 1: ...",
      "lessons": [
        {"kind": "text", "name": "...", "markdown": "..."},
        {"kind": "lab",  "name": "Lab 01: ...", "markdown": "...",
         "system": True,                       # embed the lab machine (default True)
         "solution_markdown": "..."},          # -> creates "Solución comentada: <name>"
        {"kind": "quiz", "name": "Quiz ...", "passing_percent": 70,
         "questions": [ ("¿Pregunta?", [("resp correcta", True), ("otra", False)]), ... ]},
      ],
    },
  ],
}
"""

from __future__ import annotations

import uuid
from coursestack_mcp import server as s

_uid = lambda p: p + uuid.uuid4().hex


# --------------------------------------------------------------------------- #
# content blocks
# --------------------------------------------------------------------------- #

def _text_doc(markdown: str, system_id: str | None = None) -> dict:
    items = [{"type": "text", "id": _uid("b-"), "markdown": markdown}]
    if system_id:
        items.append({"type": "system", "id": _uid("sys-"), "system_id": system_id})
    return {"type": "lesson", "id": _uid("l-"), "items": items}


def _quiz_doc(questions) -> dict:
    items = []
    for q, answers in questions:
        items.append({
            "id": _uid("q-"), "type": "question-multiple-choice",
            "question": q, "points": 1,
            "answers": [{"id": _uid("a-"), "answer": a, "correct": c} for a, c in answers],
        })
    return {"type": "quiz", "pages": [{"id": _uid("p-"), "items": items}]}


# --------------------------------------------------------------------------- #
# paginated helpers
# --------------------------------------------------------------------------- #

def _all_content() -> list[dict]:
    out, key = [], None
    while True:
        r = s.list_content(page_size=100, next_key=key)
        out += r.get("content", [])
        pi = r.get("paging_info", {}); key = pi.get("next_key")
        if not pi.get("has_more") or not key:
            return out


def _all_lessons(cid: str) -> list[dict]:
    out, key = [], None
    while True:
        r = s.list_lessons(cid, page_size=100, next_key=key)
        out += r.get("lessons", [])
        pi = r.get("paging_info", {}); key = pi.get("next_key")
        if not pi.get("has_more") or not key:
            return out


# --------------------------------------------------------------------------- #
# ensure-* (idempotent create-or-find)
# --------------------------------------------------------------------------- #

def _ensure_content(title: str, subtitle: str) -> str:
    for c in _all_content():
        if c["title"] == title:
            return c["id"]
    return s.create_content(title, subtitle).get("content", {}).get("id") \
        or s.create_content(title, subtitle)["content"]["id"]


def _ensure_system(cid: str, spec: dict) -> str | None:
    if not spec:
        return None
    existing = s._request("GET", f"/api/content/{cid}/system-configs").get("system_configs", [])
    for sc in existing:
        if sc["name"] == spec["name"]:
            return sc["id"]
    body = {
        "name": spec["name"], "type": "individual",
        "image_id": spec["image_id"], "size": spec.get("size", "micro"),
        "entire_course": True, "internet_access": spec.get("internet_access", False),
        "upload_enabled": False, "download_enabled": False, "bedrock_enabled": False,
    }
    created = s._request("POST", f"/api/content/{cid}/system-configs", json=body)
    return created.get("system_config", created).get("id")


def _ensure_chapter(cid: str, name: str, existing: dict) -> str:
    if name in existing:
        return existing[name]
    ch_id = s.create_chapter(cid, name)["chapter"]["id"]
    existing[name] = ch_id
    return ch_id


def _ensure_lesson(cid: str, ch_id: str, name: str, ltype: str, content: dict,
                   index: dict, passing_percent=None) -> str:
    """Create the lesson if absent, else update its content in place."""
    key = (name, ch_id)
    if key in index:
        lid = index[key]
        s.update_lesson(cid, lid, content=content)
        return lid
    created = s.create_lesson(cid, ch_id, name, type=ltype, content=content,
                              passing_percent=passing_percent)
    lid = created.get("lesson", created).get("id")
    index[key] = lid
    return lid


# --------------------------------------------------------------------------- #
# main entry point
# --------------------------------------------------------------------------- #

def build(course: dict) -> dict:
    title = course["title"]
    cid = _ensure_content(title, course["subtitle"])
    print(f"content: {title}  ({cid})")

    sys_id = _ensure_system(cid, course.get("lab_system"))
    if sys_id:
        print(f"lab system '{course['lab_system']['name']}': {sys_id}")

    chapters = {c["name"]: c["id"] for c in s.list_chapters(cid)["chapters"]}
    index = {(l["name"], l["chapter_id"]): l["id"] for l in _all_lessons(cid)}

    desired_order: dict[str, list[str]] = {}

    for mod in course["modules"]:
        ch_id = _ensure_chapter(cid, mod["name"], chapters)
        order: list[str] = []
        for les in mod["lessons"]:
            kind = les["kind"]
            if kind in ("text", "lab"):
                use_sys = sys_id if (kind == "lab" and les.get("system", True)) else None
                _ensure_lesson(cid, ch_id, les["name"], "lesson",
                               _text_doc(les["markdown"], use_sys), index)
                order.append(les["name"])
                if kind == "lab" and les.get("solution_markdown"):
                    sol_name = f"Solución comentada: {les['name']}"
                    _ensure_lesson(cid, ch_id, sol_name, "lesson",
                                   _text_doc(les["solution_markdown"]), index)
                    order.append(sol_name)
            elif kind == "quiz":
                _ensure_lesson(cid, ch_id, les["name"], "quiz",
                               _quiz_doc(les["questions"]), index,
                               passing_percent=les.get("passing_percent", 70))
                order.append(les["name"])
        desired_order[mod["name"]] = order
        print(f"  módulo listo: {mod['name']}  ({len(order)} lecciones)")

    # remove any chapter not in the spec (e.g. the default "New Chapter" stub
    # CourseStack seeds on freshly created content)
    spec_names = {m["name"] for m in course["modules"]}
    lessons_by_ch: dict[str, list[str]] = {}
    for l in _all_lessons(cid):
        lessons_by_ch.setdefault(l["chapter_id"], []).append(l["id"])
    for name, ch_id in list(chapters.items()):
        if name not in spec_names:
            for lid in lessons_by_ch.get(ch_id, []):
                s.delete_lesson(cid, lid)
            s.delete_chapter(cid, ch_id)
            del chapters[name]
            print(f"  quitado capítulo sobrante: {name}")

    # reorder each chapter to match the spec
    fresh = {(l["name"], l["chapter_id"]): l["id"] for l in _all_lessons(cid)}
    for mod_name, order in desired_order.items():
        ch_id = chapters[mod_name]
        ids = [fresh[(n, ch_id)] for n in order]
        for i in range(1, len(ids)):
            s.move_lesson(cid, ids[i], after_lesson_id=ids[i - 1])

    total = len(_all_lessons(cid))
    print(f"done: {len(course['modules'])} módulos, {total} lecciones.\n")
    return {"content_id": cid, "system_id": sys_id, "lessons": total}
