"""Note data model and in-memory storage for the demo."""

from pydantic import BaseModel, ConfigDict


class Note(BaseModel):
    """A note stored by the demo server."""

    model_config = ConfigDict(frozen=True)

    id: str
    title: str
    content: str


class NotesStore:
    """Simple in-memory note storage that resets when the server restarts."""

    def __init__(self) -> None:
        self._notes: list[Note] = []
        self._next_id = 1

    def create(self, title: str, content: str) -> Note:
        """Create and store a note."""
        note = Note(id=str(self._next_id), title=title, content=content)
        self._notes.append(note)
        self._next_id += 1
        return note

    def list_all(self) -> list[Note]:
        """Return a snapshot of all stored notes."""
        return self._notes.copy()
