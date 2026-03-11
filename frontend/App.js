import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import './App.css';
import { generateCodeChallenge, generateCodeVerifier, getAuthUrl, exchangeToken } from './pkceUtils';

const AUTHORIZATION_ENDPOINT = process.env.REACT_APP_AUTHORIZATION_ENDPOINT; // Replace with your auth server
const TOKEN_ENDPOINT = process.env.REACT_APP_TOKEN_ENDPOINT; // Replace with your token endpoint
const CLIENT_ID = process.env.REACT_APP_CLIENT_ID; // Replace with your client id
const REDIRECT_URI = "http://localhost:3000/auth/callback";
const BACKEND_LOG_ENDPOINT = "http://localhost:8003/api/log-token";


function LoginPage({ setVerifier, setAuthUrl }) { 
  const handleLogin = async () => {
    const codeVerifier = generateCodeVerifier();
    setVerifier(codeVerifier);
    const codeChallenge = await generateCodeChallenge(codeVerifier);
    const url = getAuthUrl(AUTHORIZATION_ENDPOINT, CLIENT_ID, REDIRECT_URI, codeChallenge);
    setAuthUrl(url);
    window.location.href = url;
  };
  return (
    <>
      <button onClick={handleLogin} style={{ padding: 12, fontSize: 16 }}>Login with PKCE</button>
    </>
  );
}

function CallbackPage({ verifier, setToken }) {
  const location = useLocation();
  React.useEffect(() => {
    const params = new URLSearchParams(location.search);
    const code = params.get('code');
    if (code && verifier) {
      exchangeToken(TOKEN_ENDPOINT, CLIENT_ID, code, verifier, REDIRECT_URI)
        .then((tok) => {
          setToken(tok);
          fetch(BACKEND_LOG_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: tok }),
          }).catch(console.error);
        })
        .catch(console.error);
    }
  }, [location.search, verifier, setToken]);
  return <p>Processing authentication...</p>;
}

function App() {
  const [token, setToken] = useState(null);
  const [verifier, setVerifier] = useState('');
  const [authUrl, setAuthUrl] = useState('');

  return (
    <Router>
      <div className="App" style={{ maxWidth: 400, margin: 'auto', padding: 32, fontFamily: 'sans-serif' }}>
        <h2>MCP Client PKCE Auth Demo</h2>
        <Routes>
          <Route
            path="/"
            element={
              !token ? (
                <LoginPage setVerifier={setVerifier} setAuthUrl={setAuthUrl} />
              ) : (
                <div>
                  <h3>Access Token</h3>
                  <textarea value={token} readOnly rows={6} style={{ width: '100%' }} />
                </div>
              )
            }
          />
          <Route
            path="/auth/callback"
            element={<CallbackPage verifier={verifier} setToken={setToken} />}
          />
        </Routes>
        {authUrl && <p>Redirecting to: <a href={authUrl}>{authUrl}</a></p>}
      </div>
    </Router>
  );
}

export default App;
