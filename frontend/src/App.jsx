import React, { useState } from 'react';
import NotesPage from './pages/NotesPage';
import GraphPage from './pages/GraphPage';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('notes');

  return (
    <div className="app">
      <header className="header">
        <h1>🧠 Second Brain Assistant</h1>
        <p>Your AI-powered personal knowledge management system</p>
      </header>
      
      <nav className="nav">
        <button 
          className={currentPage === 'notes' ? 'active' : ''}
          onClick={() => setCurrentPage('notes')}
        >
          📝 Notes
        </button>
        <button 
          className={currentPage === 'graph' ? 'active' : ''}
          onClick={() => setCurrentPage('graph')}
        >
          🕸️ Knowledge Graph
        </button>
      </nav>

      <div className="container">
        {currentPage === 'notes' && <NotesPage />}
        {currentPage === 'graph' && <GraphPage />}
      </div>
    </div>
  );
}

export default App;
