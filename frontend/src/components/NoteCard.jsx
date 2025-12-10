import React from 'react';
import { noteService } from '../services/api';

const NoteCard = ({ note, onEdit, onDelete, showScore }) => {
  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        await noteService.deleteNote(note.id);
        onDelete(note.id);
      } catch (err) {
        console.error('Failed to delete note:', err);
      }
    }
  };

  return (
    <div className="note-card">
      <h3>{note.title}</h3>
      {note.summary && <p style={{ fontStyle: 'italic', color: '#888' }}>{note.summary}</p>}
      <p>{note.content.substring(0, 150)}{note.content.length > 150 ? '...' : ''}</p>
      
      {showScore && (
        <div style={{ marginBottom: '0.5rem', color: '#667eea' }}>
          Relevance: {(showScore * 100).toFixed(1)}%
        </div>
      )}

      <div className="note-tags">
        {note.tags?.map((tag, idx) => (
          <span key={idx} className="tag">{tag}</span>
        ))}
        {note.auto_tags?.map((tag, idx) => (
          <span key={idx} className="tag auto-tag">{tag}</span>
        ))}
      </div>
      
      <div className="note-actions">
        <button className="btn btn-secondary" onClick={() => onEdit(note)}>
          Edit
        </button>
        <button className="btn btn-danger" onClick={handleDelete}>
          Delete
        </button>
      </div>
      
      <div style={{ marginTop: '1rem', fontSize: '0.875rem', color: '#999' }}>
        Created: {new Date(note.created_at).toLocaleDateString()}
      </div>
    </div>
  );
};

export default NoteCard;
