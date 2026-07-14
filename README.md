# coursestack-mcp

A local [MCP](https://modelcontextprotocol.io) server that lets an AI assistant help you
author courses on [CourseStack](https://coursestack.com) through its REST API.

It exposes tools for the authoring workflow:

- **Content** (the course container): `list_content`, `get_content`, `create_content`, `update_content`, `delete_content`
- **Chapters** (sections): `list_chapters`, `create_chapter`, `update_chapter`, `move_chapter`, `delete_chapter`
- **Lessons & quizzes**: `list_lessons`, `get_lesson`, `create_lesson`, `update_lesson`, `move_lesson`, `delete_lesson`
- **Courses**: `get_course`

A course is authored as a **content** item → **chapters** → **lessons/quizzes**.

### Lesson body structure

A lesson's `content` is a document of ordered, typed blocks — each needs a unique `id`:

```json
{ "type": "lesson", "id": "any-id", "items": [
    { "type": "text",  "id": "b1", "markdown": "# Title\n\nProse..." },
    { "type": "video", "id": "b2", "url": "https://...", "alt_text": "..." },
    { "type": "question-multiple-choice", "id": "q1", "question": "...", "answers": ["..."], "points": 1 }
] }
```

Block types: `text` (markdown — the main one for written material), `video`, `video-hosted`,
`iframe`, `file`, `code-playground`, `system`, `network`, `jupyter`, `workspace`, `aws-lab`,
`question-multiple-choice`, `question-free-text`. A quiz uses `{ "type": "quiz", "pages": [...] }`.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
cd ~/Projects/course
uv sync
cp .env.example .env   # then put your key in .env
```

Get an API key from the CourseStack developer settings. The server authenticates with
HTTP Basic auth using the key as the username (equivalent to `curl -u "<key>:"`).

## Configuration

| Env var | Required | Default |
|---------|----------|---------|
| `COURSESTACK_API_KEY` | yes | — |
| `COURSESTACK_BASE_URL` | no | `https://app.coursestack.com` |

## Run / register with Claude Code

Register it as a local stdio MCP server (user scope, so it's available everywhere):

```bash
claude mcp add coursestack --scope user \
  --env COURSESTACK_API_KEY=sk_your_key_here \
  -- uv run --directory ~/Projects/course coursestack-mcp
```

Then in Claude Code, ask it to e.g. *"create a new CourseStack course called … with chapters …"*.

## Development

```bash
uv run coursestack-mcp          # run the server over stdio
uv run mcp dev src/coursestack_mcp/server.py   # open the MCP Inspector
```
