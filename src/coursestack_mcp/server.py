"""CourseStack MCP server.

Wraps the CourseStack REST API (https://app.coursestack.com/api) so an AI
assistant can help author courses: create content, chapters, and lessons/quizzes.

Authentication is HTTP Basic with the API key as the username and an empty
password (equivalent to `curl -u "<key>:"`). Configure via environment:

    COURSESTACK_API_KEY   required, e.g. sk_...
    COURSESTACK_BASE_URL  optional, defaults to https://app.coursestack.com
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Load COURSESTACK_* from a .env at the project root, if present. Real environment
# variables always take precedence over the file.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

BASE_URL = os.environ.get("COURSESTACK_BASE_URL", "https://app.coursestack.com").rstrip("/")

# We authenticate with HTTP Basic (API key as username). That is only safe over
# TLS — otherwise the key travels base64-encoded (not encrypted) in the clear.
# Refuse a plaintext base URL rather than leak the key. localhost is allowed for
# local testing against a dev server.
if BASE_URL.startswith("http://") and not BASE_URL.startswith(
    ("http://localhost", "http://127.0.0.1")
):
    raise RuntimeError(
        f"Refusing to use plaintext HTTP base URL {BASE_URL!r}: Basic-auth API keys "
        "must only be sent over HTTPS. Use an https:// URL for COURSESTACK_BASE_URL."
    )

mcp = FastMCP("coursestack")


def _api_key() -> str:
    key = os.environ.get("COURSESTACK_API_KEY")
    if not key:
        raise RuntimeError(
            "COURSESTACK_API_KEY is not set. Create an API key in the CourseStack "
            "developer settings and expose it as the COURSESTACK_API_KEY env var."
        )
    return key


def _request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
) -> Any:
    """Call the CourseStack API and return parsed JSON (or {'ok': True} for empty bodies)."""
    # Basic auth: API key as username, empty password.
    with httpx.Client(
        base_url=BASE_URL,
        auth=(_api_key(), ""),
        timeout=30.0,
        headers={"Accept": "application/json"},
    ) as client:
        resp = client.request(method, path, params=_clean(params), json=_clean(json))

    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise RuntimeError(f"CourseStack API {method} {path} -> {resp.status_code}: {detail}")

    if resp.status_code == 204 or not resp.content:
        return {"ok": True}
    return resp.json()


def _clean(d: dict[str, Any] | None) -> dict[str, Any] | None:
    """Drop keys whose value is None so we never overwrite fields with null."""
    if d is None:
        return None
    return {k: v for k, v in d.items() if v is not None}


def _page_params(
    page_size: int | None,
    next_key: str | None,
    sort_field: str | None,
    sort_direction: str | None,
) -> dict[str, Any]:
    return {
        "page_size": page_size,
        "next_key": next_key,
        "sort_field": sort_field,
        "sort_direction": sort_direction,
    }


# --------------------------------------------------------------------------- #
# Content  (the authoring container that becomes a course)                     #
# --------------------------------------------------------------------------- #


@mcp.tool()
def list_content(
    page_size: int | None = None,
    next_key: str | None = None,
    sort_field: str | None = None,
    sort_direction: str | None = None,
) -> Any:
    """List authoring content (courses/labs) on the account.

    Returns an object with a `content` array and `paging_info` (use
    `paging_info.next_key` as `next_key` to fetch the next page).
    """
    return _request(
        "GET",
        "/api/content",
        params=_page_params(page_size, next_key, sort_field, sort_direction),
    )


@mcp.tool()
def get_content(content_id: str) -> Any:
    """Get a single content item (course) by its ID, including its settings."""
    return _request("GET", f"/api/content/{content_id}")


@mcp.tool()
def create_content(
    title: str,
    subtitle: str,
    metadata: dict[str, Any] | None = None,
    source_content_id: str | None = None,
) -> Any:
    """Create a new content item — the top-level authoring container for a course.

    Args:
        title: Course title (required).
        subtitle: Short subtitle/tagline (required).
        metadata: Optional free-form metadata object.
        source_content_id: Optional ID to clone an existing content item from.

    After creating content, add chapters with `create_chapter`, then add
    lessons/quizzes into those chapters with `create_lesson`.
    """
    return _request(
        "POST",
        "/api/content",
        json={
            "title": title,
            "subtitle": subtitle,
            "metadata": metadata,
            "source_content_id": source_content_id,
        },
    )


@mcp.tool()
def update_content(
    content_id: str,
    title: str | None = None,
    subtitle: str | None = None,
    metadata: dict[str, Any] | None = None,
    scoring_enabled: bool | None = None,
    vpn_enabled: bool | None = None,
    ai_tutor_enabled: bool | None = None,
    ai_tutor_context: str | None = None,
    ai_tutor_instructions: str | None = None,
) -> Any:
    """Update a content item's title, subtitle, and settings. Only provided fields change."""
    return _request(
        "POST",
        f"/api/content/{content_id}",
        json={
            "title": title,
            "subtitle": subtitle,
            "metadata": metadata,
            "scoring_enabled": scoring_enabled,
            "vpn_enabled": vpn_enabled,
            "ai_tutor_enabled": ai_tutor_enabled,
            "ai_tutor_context": ai_tutor_context,
            "ai_tutor_instructions": ai_tutor_instructions,
        },
    )


@mcp.tool()
def delete_content(content_id: str) -> Any:
    """Delete a content item (course). This is destructive — confirm with the user first."""
    return _request("DELETE", f"/api/content/{content_id}")


# --------------------------------------------------------------------------- #
# Chapters  (sections within a content item)                                  #
# --------------------------------------------------------------------------- #


@mcp.tool()
def list_chapters(
    content_id: str,
    page_size: int | None = None,
    next_key: str | None = None,
    sort_field: str | None = None,
    sort_direction: str | None = None,
) -> Any:
    """List chapters (sections) within a content item, in order."""
    return _request(
        "GET",
        f"/api/content/{content_id}/chapters",
        params=_page_params(page_size, next_key, sort_field, sort_direction),
    )


@mcp.tool()
def create_chapter(content_id: str, name: str, metadata: dict[str, Any] | None = None) -> Any:
    """Create a chapter (section) inside a content item. New chapters append to the end."""
    return _request(
        "POST",
        f"/api/content/{content_id}/chapters",
        json={"name": name, "metadata": metadata},
    )


@mcp.tool()
def update_chapter(
    content_id: str,
    chapter_id: str,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> Any:
    """Rename a chapter or update its metadata. Only provided fields change."""
    return _request(
        "POST",
        f"/api/content/{content_id}/chapters/{chapter_id}",
        json={"name": name, "metadata": metadata},
    )


@mcp.tool()
def move_chapter(
    content_id: str,
    chapter_id: str,
    before_chapter_id: str | None = None,
    after_chapter_id: str | None = None,
) -> Any:
    """Reorder a chapter. Provide exactly one of before_chapter_id / after_chapter_id
    to place this chapter immediately before or after the referenced chapter."""
    return _request(
        "POST",
        f"/api/content/{content_id}/chapters/{chapter_id}/move",
        json={"before_chapter_id": before_chapter_id, "after_chapter_id": after_chapter_id},
    )


@mcp.tool()
def delete_chapter(content_id: str, chapter_id: str) -> Any:
    """Delete a chapter. Destructive — this removes the chapter and confirm before use."""
    return _request("DELETE", f"/api/content/{content_id}/chapters/{chapter_id}")


# --------------------------------------------------------------------------- #
# Lessons & quizzes  (the teaching units inside chapters)                      #
# --------------------------------------------------------------------------- #


@mcp.tool()
def list_lessons(
    content_id: str,
    page_size: int | None = None,
    next_key: str | None = None,
    sort_field: str | None = None,
    sort_direction: str | None = None,
) -> Any:
    """List lessons and quizzes within a content item."""
    return _request(
        "GET",
        f"/api/content/{content_id}/lessons",
        params=_page_params(page_size, next_key, sort_field, sort_direction),
    )


@mcp.tool()
def get_lesson(content_id: str, lesson_id: str) -> Any:
    """Get a single lesson or quiz by ID, including its rich `content` body."""
    return _request("GET", f"/api/content/{content_id}/lessons/{lesson_id}")


@mcp.tool()
def create_lesson(
    content_id: str,
    chapter_id: str,
    name: str,
    type: str = "lesson",
    content: Any | None = None,
    passing_percent: float | None = None,
    free_preview: bool | None = None,
    metadata: dict[str, Any] | None = None,
) -> Any:
    """Create a lesson or quiz inside a chapter.

    Args:
        content_id: The content item the chapter belongs to.
        chapter_id: The chapter to add this lesson/quiz to (required).
        name: Lesson/quiz title (required).
        type: "lesson" or "quiz" (default "lesson").
        content: Optional structured rich body, passed through verbatim. Omit to
            create an empty lesson to fill in later. Shape depends on `type`:

            For a lesson — a document of ordered blocks (each block needs a unique
            `id` and a `type`):
                {"type": "lesson", "id": "<any-id>", "items": [
                    {"type": "text",  "id": "b1", "markdown": "# Title\n\nProse..."},
                    {"type": "video", "id": "b2", "url": "https://...", "alt_text": "..."},
                    {"type": "question-multiple-choice", "id": "q1",
                     "question": "...", "answers": [...], "points": 1}
                ]}
            Block types: text (markdown), video, video-hosted, iframe, file,
            code-playground, system, network, jupyter, workspace, aws-lab,
            question-multiple-choice, question-free-text. `text`/markdown is the
            main one for written course material.

            For a quiz — pages of question blocks:
                {"type": "quiz", "pages": [{"id": "p1", "items": [ ...questions... ]}]}
        passing_percent: For quizzes, the passing score threshold (percent).
        free_preview: Whether this lesson is a free preview.
        metadata: Optional free-form metadata object.
    """
    created = _request(
        "POST",
        f"/api/content/{content_id}/lessons",
        json={
            "chapter_id": chapter_id,
            "type": type,
            "name": name,
            "passing_percent": passing_percent,
            "free_preview": free_preview,
            "metadata": metadata,
        },
    )
    # The create endpoint ignores `content` and seeds a default body, so when a
    # body is supplied we apply it with a follow-up update.
    if content is not None:
        lesson_id = created.get("lesson", created).get("id")
        if lesson_id:
            return _request(
                "POST",
                f"/api/content/{content_id}/lessons/{lesson_id}",
                json={"content": content},
            )
    return created


@mcp.tool()
def update_lesson(
    content_id: str,
    lesson_id: str,
    name: str | None = None,
    chapter_id: str | None = None,
    content: Any | None = None,
    passing_percent: float | None = None,
    free_preview: bool | None = None,
    metadata: dict[str, Any] | None = None,
) -> Any:
    """Update a lesson/quiz. Only provided fields change. Pass `content` to replace
    the lesson body, or `chapter_id` to move it to a different chapter."""
    return _request(
        "POST",
        f"/api/content/{content_id}/lessons/{lesson_id}",
        json={
            "name": name,
            "chapter_id": chapter_id,
            "content": content,
            "passing_percent": passing_percent,
            "free_preview": free_preview,
            "metadata": metadata,
        },
    )


@mcp.tool()
def move_lesson(
    content_id: str,
    lesson_id: str,
    before_lesson_id: str | None = None,
    after_lesson_id: str | None = None,
    chapter_id: str | None = None,
) -> Any:
    """Reorder a lesson, optionally moving it into a different chapter.

    Provide before_lesson_id or after_lesson_id to position it, and/or chapter_id
    to move it into another chapter."""
    return _request(
        "POST",
        f"/api/content/{content_id}/lessons/{lesson_id}/move",
        json={
            "before_lesson_id": before_lesson_id,
            "after_lesson_id": after_lesson_id,
            "chapter_id": chapter_id,
        },
    )


@mcp.tool()
def delete_lesson(content_id: str, lesson_id: str) -> Any:
    """Delete a lesson or quiz. Destructive — confirm with the user first."""
    return _request("DELETE", f"/api/content/{content_id}/lessons/{lesson_id}")


# --------------------------------------------------------------------------- #
# Courses  (published/enrollable view of content)                             #
# --------------------------------------------------------------------------- #


@mcp.tool()
def get_course(course_id: str) -> Any:
    """Get a course by ID (title, subtitle, description, and course-level details)."""
    return _request("GET", f"/api/courses/{course_id}")


def main() -> None:
    """Entry point: run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
