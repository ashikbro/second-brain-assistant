import React, { useState, useEffect } from 'react';
import { noteService } from '../services/api';

const NoteForm = ({ onNoteCreated, editNote, onCancel }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (editNote) {
      setTitle(editNote.title);
      setContent(editNote.content);
      setTags(editNote.tags.join(', '));
    }
  }, [editNote]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const noteData = {
        title,
        content,
        tags: tags.split(',').map(tag => tag.trim()).filter(tag => tag),
      };

      if (editNote) {
        await noteService.updateNote(editNote.id, noteData);
      } else {
        await noteService.createNote(noteData);
      }

      setTitle('');
      setContent('');
      setTags('');
      onNoteCreated();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save note');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="note-form">
      <h2>{editNote ? 'Edit Note' : 'Create New Note'}</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            placeholder="Enter note title"
          />
        </div>
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            placeholder="Enter note content"
          />
        </div>
        <div className="form-group">
          <label htmlFor="tags">Tags (comma-separated)</label>
          <input
            type="text"
            id="tags"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="e.g., work, ideas, research"
          />
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Saving...' : editNote ? 'Update Note' : 'Create Note'}
          </button>
          {editNote && (
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default NoteForm;
