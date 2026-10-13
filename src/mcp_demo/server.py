"""MCP server exposing the notes demo as tools, a resource, and a prompt."""

import json

from mcp.server import MCPServer

from mcp_demo.notes import Note, NotesStore


def create_server() -> MCPServer:
    """Create a server instance with its own in-memory note store."""
    store = NotesStore()
    server = MCPServer(
        "Notes Demo",
        instructions=(
            "Use the note tools to create notes and the notes resource to read them."
        ),
    )

    @server.tool()
    def create_note(title: str, content: str) -> Note:
        """Create a note and return the saved note."""
        return store.create(title, content)

    @server.tool()
    def list_notes() -> list[Note]:
        """List all notes currently stored by this server."""
        return store.list_all()

    @server.resource("notes://all")
    def all_notes() -> str:
        """Read all notes as JSON application context."""
        return json.dumps(
            [note.model_dump() for note in store.list_all()],
            indent=2,
        )

    @server.prompt()
    def summarize_notes(topic: str) -> str:
        """Create a user prompt asking for a summary of notes on a topic."""
        return (
            f"Summarize the notes about {topic}. "
            "Call out the key points and any open questions."
        )

    return server


mcp = create_server()
