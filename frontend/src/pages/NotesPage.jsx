import React, { useState, useEffect } from 'react';
import NoteForm from '../components/NoteForm';
import NoteCard from '../components/NoteCard';
import SearchBox from '../components/SearchBox';
import { noteService } from '../services/api';

const NotesPage = () => {
  const [notes, setNotes] = useState([]);
  const [searchResults, setSearchResults] = useState(null);
  const [editingNote, setEditingNote] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    setLoading(true);
    try {
      const response = await noteService.getNotes();
      setNotes(response.data);
    } catch (err) {
      console.error('Failed to load notes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNoteCreated = () => {
    setEditingNote(null);
    loadNotes();
  };

  const handleEdit = (note) => {
    setEditingNote(note);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = (noteId) => {
    setNotes(notes.filter(note => note.id !== noteId));
  };

  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  const displayNotes = searchResults !== null ? searchResults : notes;

  return (
    <div>
      <NoteForm 
        onNoteCreated={handleNoteCreated} 
        editNote={editingNote}
        onCancel={() => setEditingNote(null)}
      />
      
      <SearchBox onSearchResults={handleSearchResults} />

      {searchResults !== null && (
        <div style={{ marginBottom: '1rem' }}>
          <button 
            className="btn btn-secondary" 
            onClick={() => setSearchResults(null)}
          >
            Clear Search Results
          </button>
        </div>
      )}

      {loading ? (
        <div className="loading">Loading notes...</div>
      ) : displayNotes.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#666' }}>
          No notes found. Create your first note above!
        </div>
      ) : (
        <div className="notes-grid">
          {displayNotes.map((item) => {
            const note = item.note || item;
            const score = item.similarity_score;
            return (
              <NoteCard 
                key={note.id} 
                note={note} 
                onEdit={handleEdit}
                onDelete={handleDelete}
                showScore={score}
              />
            );
          })}
        </div>
      )}
    </div>
  );
};

export default NotesPage;
