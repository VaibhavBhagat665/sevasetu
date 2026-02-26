import { useState } from 'react';
import Home from './pages/Home';
import Assistant from './pages/Assistant';
import './App.css';

/**
 * SevaSetu — Root Application
 * Switches between Home (landing) and Assistant (workflow) views.
 */
export default function App() {
  const [view, setView] = useState('home');

  return (
    <div className="app">
      {/* Nav */}
      <nav className="app-nav">
        <div className="nav-inner">
          <button className="nav-brand" onClick={() => setView('home')}>
            <span className="nav-logo">🇮🇳</span>
            <span className="nav-title">SevaSetu</span>
          </button>
          <div className="nav-links">
            {view === 'home' ? (
              <button className="btn btn-primary btn-sm" onClick={() => setView('assistant')}>
                Get Started →
              </button>
            ) : (
              <button className="btn btn-ghost btn-sm" onClick={() => setView('home')}>
                Home
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* Views */}
      {view === 'home' && <Home onGetStarted={() => setView('assistant')} />}
      {view === 'assistant' && <Assistant onBack={() => setView('home')} />}
    </div>
  );
}
