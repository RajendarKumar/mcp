import pytest
from mcp import Client
from mcp.types import TextContent, TextResourceContents

from mcp_demo.notes import NotesStore
from mcp_demo.server import create_server


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_create_and_list_notes() -> None:
    server = create_server()

    async with Client(server, raise_exceptions=True) as client:
        created = await client.call_tool(
            "create_note",
            {"title": "MCP", "content": "Tools let a model take action."},
        )
        listed = await client.call_tool("list_notes", {})

    assert created.is_error is False
    assert created.structured_content == {
        "id": "1",
        "title": "MCP",
        "content": "Tools let a model take action.",
    }
    assert listed.is_error is False
    assert listed.structured_content == {
        "result": [
            {
                "id": "1",
                "title": "MCP",
                "content": "Tools let a model take action.",
            }
        ]
    }


@pytest.mark.anyio
async def test_get_and_delete_notes() -> None:
    server = create_server()

    async with Client(server, raise_exceptions=True) as client:
        await client.call_tool(
            "create_note",
            {"title": "MCP", "content": "Notes can be looked up and deleted."},
        )
        found = await client.call_tool("get_note", {"note_id": "1"})
        not_found = await client.call_tool("get_note", {"note_id": "missing"})
        deleted = await client.call_tool("delete_note", {"note_id": "1"})
        not_deleted = await client.call_tool("delete_note", {"note_id": "1"})
        remaining = await client.call_tool("list_notes", {})

    assert found.is_error is False
    assert found.structured_content == {
        "result": {
            "id": "1",
            "title": "MCP",
            "content": "Notes can be looked up and deleted.",
        },
    }
    assert not_found.is_error is False
    assert not_found.structured_content == {"result": None}
    assert deleted.is_error is False
    assert deleted.structured_content == {"result": True}
    assert not_deleted.is_error is False
    assert not_deleted.structured_content == {"result": False}
    assert remaining.structured_content == {"result": []}


@pytest.mark.anyio
async def test_notes_resource_and_summary_prompt() -> None:
    server = create_server()

    async with Client(server, raise_exceptions=True) as client:
        await client.call_tool(
            "create_note",
            {"title": "Resources", "content": "The host chooses what to read."},
        )
        resource = await client.read_resource("notes://all")
        prompt = await client.get_prompt(
            "summarize_notes",
            {"topic": "resources"},
        )

    assert len(resource.contents) == 1
    resource_content = resource.contents[0]
    assert isinstance(resource_content, TextResourceContents)
    assert '"title": "Resources"' in resource_content.text

    assert len(prompt.messages) == 1
    prompt_content = prompt.messages[0].content
    assert isinstance(prompt_content, TextContent)
    assert prompt_content.text == (
        "Summarize the notes about resources. "
        "Call out the key points and any open questions."
    )


def test_notes_store_owns_ids_and_returns_snapshots() -> None:
    store = NotesStore()

    first = store.create("First", "First note")
    snapshot = store.list_all()
    second = store.create("Second", "Second note")

    assert first.id == "1"
    assert second.id == "2"
    assert len(snapshot) == 1
    assert [note.id for note in store.list_all()] == ["1", "2"]
