# MCP Notes Demo

A small Python MCP server for learning the three core server primitives:

- **Tools** are actions the model can call: `create_note`, `list_notes`,
  `get_note`, and `delete_note`.
- **Resources** are read-only context the host can load: `notes://all`.
- **Prompts** are reusable messages a user can invoke: `summarize_notes`.

The notes live in memory, so they are cleared when the server restarts. This
keeps the example self-contained and makes the tool side effect easy to see.

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- Node.js 22.19 or newer and npm (only needed to run the MCP Inspector)

## Run the demo

From this directory, install the project dependencies:

```bash
uv sync
```

Start the server in the MCP Inspector from the project root:

```bash
uv run mcp dev src/mcp_demo/server.py
```

The Inspector opens a browser UI. Try these in order:

1. In **Tools**, call `create_note` with a title and content; note the returned ID.
2. Call `list_notes` to inspect all saved notes.
3. Call `get_note` with a note ID to retrieve one note. An unknown ID returns
   `null`.
4. Call `delete_note` with a note ID. It returns `true` if a note was deleted
   and `false` if the ID was not found.
5. In **Resources**, read `notes://all` to see the remaining notes as JSON.
6. In **Prompts**, render `summarize_notes` with a topic.

The Inspector is a client; it launches the server over the local stdio
transport. The Python SDK handles the MCP protocol, argument schemas, and
request dispatch from the function annotations and decorators.

## Run the tests

```bash
uv run pytest
```

The tests use the SDK's in-memory client, so they do not need a running server,
port, or Inspector.

## Follow the code

The project uses a `src/` layout:

```text
src/mcp_demo/
├── __init__.py
├── notes.py       # Note model and in-memory storage
└── server.py      # MCP server, tools, resource, and prompt
tests/
└── test_server.py
```

Start in [server.py](src/mcp_demo/server.py):

1. `create_server()` assembles a server and gives it an independent `NotesStore`.
2. `@server.tool()` registers model-callable functions. Type hints define the
   argument and output shapes:
   - `create_note(title, content)` creates a note and returns it with its ID.
   - `list_notes()` returns all notes.
   - `get_note(note_id)` returns a note or `None` when no matching ID exists.
   - `delete_note(note_id)` removes a note and reports success as a boolean.
3. `@server.resource(...)` publishes read-only data at a URI.
4. `@server.prompt()` registers a reusable prompt template.
5. [notes.py](src/mcp_demo/notes.py) keeps data handling separate from MCP
   protocol registration.
6. [tests/test_server.py](tests/test_server.py) connects an in-memory client
   and exercises all three primitives through MCP.

## Try changing it

- Add an `update_note` tool and test that the resource reflects the updated note.
- Add a resource template such as `notes://{note_id}` for reading one note.
- Change the prompt to include note content and inspect the rendered message.
