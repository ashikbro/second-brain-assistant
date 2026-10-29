from second_brain import NoteStore


def test_note_lifecycle_search_and_export():
    store = NoteStore()
    note = store.create("Project Plan", "Build a local search index", ["Work", "planning"])
    assert store.get(note.id).tags == ("planning", "work")
    assert [item.id for item in store.search("search", tag="work")] == [note.id]
    assert "#planning #work" in store.export_markdown(note.id)
    assert '"title": "Project Plan"' in store.export_json(note.id)

    updated = store.update(note.id, body="Ship deterministic search first")
    assert updated.body.startswith("Ship")
    assert store.archive(note.id).archived is True
    assert store.search("search") == []
    assert store.search("search", include_archived=True)[0].id == note.id


def test_empty_title_is_rejected():
    store = NoteStore()
    try:
        store.create("  ", "body")
    except ValueError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("empty title was accepted")
