# COURSE spec schema (premium)

A course is a single Python file in `courses/<slug>.py` assigning `COURSE = {...}`.
`course_builder.build(COURSE)` consumes it — idempotent, safe to re-run.

```python
COURSE = {
  "title": "Administración de Linux",
  "subtitle": "…",
  # provision (or reuse) an individual lab machine, embedded in every lab
  "lab_system": {"name": "linuxbox", "image_id": "428356ac-de2b-4618-8f1a-f34d7b55001f", "size": "micro"},
  "modules": [
    {
      "name": "Módulo 1: …",
      # PREMIUM: rendered into an "Objetivos del módulo" lesson at the top of the module
      "level": "Principiante | Intermedio | Avanzado",
      "duration": "~45 min",
      "objectives": ["Objetivo medible 1", "Objetivo 2", "Objetivo 3"],
      "lessons": [
        {"kind": "text", "name": "Bienvenida al curso", "markdown": "…"},   # module 1 only
        {"kind": "text", "name": "Conceptos: …", "markdown": "…"},          # deep theory
        {"kind": "text", "name": "Cheatsheet: …", "markdown": "…"},         # reference lesson
        {"kind": "lab",  "name": "Lab 01: …", "markdown": "…instrucciones…",
         "system": True,                                      # embed lab machine (default True)
         "rubric": ["Criterio 1 (X pts)", "Criterio 2 (X pts)"],   # PREMIUM: appended as "Rúbrica"
         "solution_markdown": "# Solución comentada\n\n```bash\n…\n```\n\n## Explicación paso a paso\n…"},
        {"kind": "quiz", "name": "Quiz Módulo 1: …", "passing_percent": 70,
         "questions": [
            ("Enunciado (usa escenarios, no solo memoria)", [("correcta", True), ("d", False), ("d", False), ("d", False)]),
         ]},
      ],
    },
    # … final module should end with an "Examen Final" quiz (passing_percent 80, 8–10 questions)
  ],
}
```

## Rules

- **Language:** Spanish unless told otherwise.
- **Lesson kinds:** `text` (concepts, welcome, cheatsheets), `lab` (hands-on; auto-gets the lab machine + optional rubric + a "Solución comentada" lesson from `solution_markdown`), `quiz` (`question-multiple-choice`, exactly one `True` per question).
- **Premium bar (every course):**
  - Every module has `objectives` + `level` + `duration`.
  - Concept lessons are deep (~2500–4500 chars): definition → por qué importa → cómo funciona → ejemplos reales → errores comunes ("gotchas"). Use ```fenced code```, tables, and callouts.
  - ≥ 2 graded labs per module where the topic allows, each with a `rubric` and a commented solution.
  - One `Cheatsheet: …` text lesson per module (or a course-level one) distilling commands/patterns.
  - Quizzes are **scenario-based** (4 Q each), and the course ends with a graded **Examen Final** (8–10 Q, `passing_percent: 80`).

## Python constraints

- Valid Python, `COURSE` literal only — no imports/functions.
- Triple-quoted markdown; NEVER embed `"""` inside a string (code fences use backticks).
- Use raw strings `r"""…"""` when markdown contains backslashes (regex, `\d`, crontab `\%`).
- Validate before building:
  `python3 -c "import ast; ast.parse(open('courses/<slug>.py').read()); print('OK')"`

## Build

```bash
cd ~/Projects/course && set -a && . ./.env && set +a
uv run python -c "import sys; sys.path.insert(0,'courses'); from course_builder import build; import <slug> as c; print(build(c.COURSE))"
```
