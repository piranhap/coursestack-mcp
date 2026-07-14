---
name: build-course
description: Build a premium, monetizable CourseStack course by synthesizing source PDFs from a local folder into an original course. Use when the user drops PDFs (e.g. several authors on one topic) into a folder and wants "the ultimate compendium" turned into an intense, paid-tier course — or asks to build/author a CourseStack course from source material.
---

# Build a premium CourseStack course from source PDFs

Turn a folder of reference PDFs (often several authors on one topic) into ONE original,
premium, hands-on CourseStack course. The pipeline lives in `~/Projects/course`
(`course_builder.py` engine + `courses/*.py` specs). Read `references/spec-schema.md`
before authoring — it defines the spec and the premium bar.

## Non-negotiable: originality (this is what makes it sellable AND legal)

The PDFs are **reference to learn from, not content to copy**. Different authors,
different copyrights. You MUST:
- Synthesize concepts in **our own words**; write **original** examples, labs, and quizzes.
- NEVER reproduce an author's prose, figures, tables, or exercises verbatim or near-verbatim.
- Where authors differ, reconcile and explain the tradeoff — that synthesis is the value.
If a source is a single copyrighted textbook you'd be mirroring 1:1, stop and tell the user.

## Inputs

Confirm with the user (infer sensible defaults, ask only what's missing):
- **Source folder** of PDFs, e.g. `~/Projects/course/sources/<slug>/`.
- **Topic / title** and **language** (default: Spanish).
- Whether to reuse the **linuxbox** lab machine (default yes; image `428356ac-de2b-4618-8f1a-f34d7b55001f`).

## Pipeline

### 1. Ingest (parallel)
- `ls -la <folder>` to inventory PDFs; get page counts.
- Spawn **one `general-purpose` subagent per PDF, in a single message** (parallel). Each:
  - Reads its PDF with the Read tool in page batches (max 20 pages/call; loop through all pages).
  - Returns STRUCTURED notes only (no verbatim copying): `{author/title, key_concepts[],
    commands_tools[], worked_examples_summarized[], coverage_map[], notable_gaps[],
    strong_sections[]}`.
- Collect the notes. If a PDF is huge, tell the subagent to prioritize breadth of coverage.

### 2. Synthesize the compendium
- Merge all notes into a master outline: dedupe topics, reconcile conflicts, order
  pedagogically (foundational → advanced), and list gaps to fill from your own knowledge.
- Target **6–8 modules**. For each: objectives, concepts to cover, 1–3 labs, a cheatsheet.
- Write the outline to `sources/<slug>/OUTLINE.md` and show the user a summary. Offer a
  chance to adjust before authoring (skip if they said "just build it").

### 3. Author the spec (premium)
- Follow `references/spec-schema.md` EXACTLY. Produce `courses/<slug>.py`.
- Depth matters — this is the paid tier. For a large course, delegate **per-module
  authoring to parallel subagents** (each writes one module dict), then assemble. Give each
  subagent the module's slice of the compendium + the schema + the originality rule.
- Every module: `objectives`/`level`/`duration`, deep concept lessons, ≥2 graded labs with
  `rubric` + commented solutions, a `Cheatsheet:` lesson, scenario-based quiz. End the course
  with an **Examen Final** quiz (8–10 Q, `passing_percent: 80`).
- Validate it parses: `python3 -c "import ast; ast.parse(open('courses/<slug>.py').read()); print('OK')"`.

### 4. Build
```bash
cd ~/Projects/course && set -a && . ./.env && set +a
uv run python -c "import sys; sys.path.insert(0,'courses'); from course_builder import build; import <slug> as c; print(build(c.COURSE))"
```
The engine creates content, chapters, lessons, solutions, quizzes, objectives lessons,
provisions the linuxbox, embeds it in labs, removes the stub chapter, and orders everything.
Re-run freely — it updates in place.

### 5. QA
- Integrity check: paginate lessons, confirm every quiz has ≥4 questions, every lab embeds a
  `system` block, every solution has a code fence, module count matches the spec.
- Accuracy spot-check: sample 3–4 concept lessons against the compendium notes for technical
  correctness. Fix by editing the spec and re-running `build`.

## Deliver
Report: course title + content_id, module/lesson counts, and remind the user to review a few
lessons in the CourseStack UI before publishing. Commit `courses/<slug>.py` (never the PDFs or
`.env`). Keep source PDFs out of git — add `sources/` to `.gitignore` if not already.

## Notes
- Run everything from `~/Projects/course`; the API key loads from `.env`.
- Reference examples already in the repo: `courses/admin_linux.py`, `courses/forense_linux.py`.
- The whole format is proven — 5 courses already live.
