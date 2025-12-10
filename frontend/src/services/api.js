import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const noteService = {
  createNote: (noteData) => api.post('/notes/', noteData),
  getNotes: () => api.get('/notes/'),
  getNote: (id) => api.get(`/notes/${id}`),
  updateNote: (id, noteData) => api.put(`/notes/${id}`, noteData),
  deleteNote: (id) => api.delete(`/notes/${id}`),
  searchNotes: (query, limit = 10) => api.post('/notes/search', { query, limit }),
};

export const graphService = {
  buildGraph: () => api.post('/graph/build'),
  getGraph: () => api.get('/graph/'),
  getRelatedNotes: (noteId, limit = 5) => api.get(`/graph/related/${noteId}`, { params: { limit } }),
};

export const aiService = {
  summarize: (content) => api.post('/ai/summarize', { content }),
  generateIdeas: (topic, context = '') => api.post('/ai/generate-ideas', { topic, context }),
  extractTags: (content) => api.post('/ai/extract-tags', { content }),
};

export default api;
