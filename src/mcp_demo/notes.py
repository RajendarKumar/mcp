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

    def get_note(self, note_id: str) -> Note | None:
        """Get a note by its ID, or None if not found."""
        for note in self._notes:
            if note.id == note_id:
                return note.model_copy()
        return None

    def list_all(self) -> list[Note]:
        """Return a snapshot of all stored notes."""
        return self._notes.copy()

    def delete(self, note_id: str) -> bool:
        """Delete a note by its ID, returning True if deleted."""
        for index, note in enumerate(self._notes):
            if note.id == note_id:
                del self._notes[index]
                return True
        return False
