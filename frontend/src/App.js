import React, { useState } from 'react';
import './App.css';

function App() {
  const [nicInput, setNicInput] = useState('');
  const [validationResult, setValidationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showTrace, setShowTrace] = useState(false);

  const API_URL = 'http://localhost:5000';

  const handleValidate = async () => {
    setValidationResult(null);
    setError(null);

    if (!nicInput.trim()) {
      setError('Please enter a NIC number');
      return;
    }

    setIsLoading(true);

    try {
      const endpoint = showTrace ? '/validate-nic-trace' : '/validate-nic';
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nic: nicInput }),
      });

      const data = await response.json();

      if (response.ok) {
        setValidationResult(data);
      } else {
        setError(data.message || 'Validation failed');
      }
    } catch (err) {
      setError('Failed to connect to backend. Make sure the Flask server is running on port 5000.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleValidate();
    }
  };

  const handleClear = () => {
    setNicInput('');
    setValidationResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sri Lankan NIC Validator</h1>
        <p className="subtitle">Deterministic Finite Automaton (DFA)</p>
      </header>

      <main className="App-main">
        <div className="input-section">
          <label htmlFor="nic-input">Enter NIC Number:</label>
          <div className="input-group">
            <input
              id="nic-input"
              type="text"
              value={nicInput}
              onChange={(e) => setNicInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="e.g., 981234567V or 199812345678"
              className="nic-input"
              disabled={isLoading}
            />
            <button
              onClick={handleValidate}
              disabled={isLoading}
              className="btn btn-primary"
            >
              {isLoading ? 'Validating...' : 'Validate NIC'}
            </button>
            <button
              onClick={handleClear}
              disabled={isLoading}
              className="btn btn-secondary"
            >
              Clear
            </button>
          </div>

          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={showTrace}
                onChange={(e) => setShowTrace(e.target.checked)}
              />
              <span>Show DFA state transitions </span>
            </label>
          </div>
        </div>

        <div className="info-card">
          <h2>Valid NIC Formats</h2>
          <ul>
            <li><strong>Old NIC:</strong> 9 digits followed by 'V' or 'X'
              <span className="example"> (e.g., 981234567V)</span>
            </li>
            <li><strong>New NIC:</strong> 12 digits
              <span className="example"> (e.g., 199812345678)</span>
            </li>
          </ul>
        </div>

        {error && (
          <div className="result-card error">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {validationResult && (
          <div className={`result-card ${validationResult.result === 'ACCEPT' ? 'success' : 'reject'}`}>
            <h3>
              {validationResult.result === 'ACCEPT' ? 'ACCEPTED' : 'REJECTED'}
            </h3>
            <div className="result-details">
              <p><strong>Input:</strong> {validationResult.input}</p>
              <p><strong>Result:</strong> {validationResult.result}</p>
              <p><strong>Final State:</strong> {validationResult.final_state}</p>
              {validationResult.format && (
                <p><strong>Format:</strong> {validationResult.format}</p>
              )}
            </div>

            {validationResult.trace && (
              <div className="trace-section">
                <h4>DFA State Transitions:</h4>
                <div className="trace-list">
                  {validationResult.trace.map((step, index) => (
                    <div key={index} className="trace-step">
                      {step.step === 0 ? (
                        <span>Start → <strong>{step.state}</strong></span>
                      ) : (
                        <span>
                          Read '<strong>{step.input}</strong>' → <strong>{step.state}</strong>
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>
          Automata Theory Project - DFA Implementation for NIC Validation
        </p>
        <p className="footer-note">
          Backend: Python (Flask) | Frontend: React | DFA State Machine
        </p>
      </footer>
    </div>
  );
}

export default App;
