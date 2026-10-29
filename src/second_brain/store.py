"""A small SQLite-backed notes store with deterministic search and export."""

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3


@dataclass(frozen=True)
class Note:
    id: int
    title: str
    body: str
    tags: tuple[str, ...]
    archived: bool
    created_at: str
    updated_at: str


class NoteStore:
    def __init__(self, path: str | Path = ":memory:"):
        self.connection = sqlite3.connect(str(path))
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                tags TEXT NOT NULL,
                archived INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )

    def close(self) -> None:
        self.connection.close()

    def create(self, title: str, body: str, tags: list[str] | tuple[str, ...] = ()) -> Note:
        title = title.strip()
        if not title:
            raise ValueError("title cannot be empty")
        now = datetime.now(timezone.utc).isoformat()
        normalized_tags = tuple(sorted({tag.strip().lower() for tag in tags if tag.strip()}))
        cursor = self.connection.execute(
            "INSERT INTO notes(title, body, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (title, body, json.dumps(normalized_tags), now, now),
        )
        self.connection.commit()
        return self.get(cursor.lastrowid)

    def get(self, note_id: int) -> Note:
        row = self.connection.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        if row is None:
            raise KeyError(f"note {note_id} does not exist")
        return self._note(row)

    def update(self, note_id: int, *, title: str | None = None, body: str | None = None,
               tags: list[str] | tuple[str, ...] | None = None) -> Note:
        current = self.get(note_id)
        next_title = current.title if title is None else title.strip()
        if not next_title:
            raise ValueError("title cannot be empty")
        next_tags = current.tags if tags is None else tuple(
            sorted({tag.strip().lower() for tag in tags if tag.strip()})
        )
        now = datetime.now(timezone.utc).isoformat()
        self.connection.execute(
            "UPDATE notes SET title = ?, body = ?, tags = ?, updated_at = ? WHERE id = ?",
            (next_title, current.body if body is None else body, json.dumps(next_tags), now, note_id),
        )
        self.connection.commit()
        return self.get(note_id)

    def archive(self, note_id: int) -> Note:
        self.get(note_id)
        self.connection.execute("UPDATE notes SET archived = 1 WHERE id = ?", (note_id,))
        self.connection.commit()
        return self.get(note_id)

    def search(self, query: str = "", tag: str | None = None, include_archived: bool = False) -> list[Note]:
        terms = [term.lower() for term in re.findall(r"\w+", query)]
        rows = self.connection.execute(
            "SELECT * FROM notes WHERE archived = 0 OR ? ORDER BY updated_at DESC",
            (int(include_archived),),
        ).fetchall()
        results = []
        for row in rows:
            note = self._note(row)
            haystack = f"{note.title} {note.body}".lower()
            if terms and not all(term in haystack for term in terms):
                continue
            if tag and tag.lower() not in note.tags:
                continue
            results.append(note)
        return results

    def export_json(self, note_id: int) -> str:
        note = self.get(note_id)
        return json.dumps(note.__dict__, indent=2)

    def export_markdown(self, note_id: int) -> str:
        note = self.get(note_id)
        tags = " ".join(f"#{tag}" for tag in note.tags)
        return f"# {note.title}\n\n{tags}\n\n{note.body}\n"

    @staticmethod
    def _note(row: sqlite3.Row) -> Note:
        return Note(
            id=row["id"],
            title=row["title"],
            body=row["body"],
            tags=tuple(json.loads(row["tags"])),
            archived=bool(row["archived"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
