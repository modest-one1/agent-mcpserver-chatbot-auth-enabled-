import React, { useState } from 'react';
import './App.css';
import { generateCodeChallenge, generateCodeVerifier, getAuthUrl, exchangeToken } from './pkceUtils';

function Chat({ token }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Welcome to the chat!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim() === '') return;
    const userMsg = { sender: 'user', text: input };
    setMessages(msgs => [...msgs, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8003/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: input,
          metadata: {
            additionalProp1: {}
          }
        })
      });
      const data = await res.json();
      setMessages(msgs => [...msgs, { sender: 'bot', text: data.message ?? data.text ?? 'No response' }]);
    } catch (err) {
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Error contacting backend.' }]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Chat Interface</div>
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.sender === 'user' ? 'chat-user' : 'chat-bot'}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="chat-bot">Bot is typing...</div>}
      </div>
      <div className="chat-input-row">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type a message..."
          className="chat-input"
          disabled={loading}
        />
        <button onClick={handleSend} className="chat-send" disabled={loading}>Send</button>
      </div>
    </div>
  );
}


const AUTHORIZATION_ENDPOINT = process.env.REACT_APP_AUTHORIZATION_ENDPOINT; // Replace with your auth server
const TOKEN_ENDPOINT = process.env.REACT_APP_TOKEN_ENDPOINT; // Replace with your token endpoint
const CLIENT_ID = process.env.REACT_APP_CLIENT_ID; // Replace with your client id
const REDIRECT_URI = 'http://localhost:3000/auth/callback';


function App() {
  const [token, setToken] = useState(null);
  const [verifier, setVerifier] = useState('');
  const [authUrl, setAuthUrl] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    const codeVerifier = generateCodeVerifier();
    sessionStorage.setItem('pkce_code_verifier', codeVerifier);
    setVerifier(codeVerifier);
    const codeChallenge = await generateCodeChallenge(codeVerifier);
    const url = getAuthUrl(AUTHORIZATION_ENDPOINT, CLIENT_ID, REDIRECT_URI, codeChallenge);
    setAuthUrl(url);
    window.location.href = url;
  };

  // Handle callback
  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    // Always try to get code_verifier from sessionStorage after redirect
    const storedVerifier = sessionStorage.getItem('pkce_code_verifier');
    if (code && storedVerifier) {
      exchangeToken(TOKEN_ENDPOINT, CLIENT_ID, code, storedVerifier, REDIRECT_URI)
        .then((tok) => {
          setToken(tok);
          setLoginSuccess(true);
          sessionStorage.removeItem('pkce_code_verifier');
          window.history.replaceState({}, '', '/');
        })
        .catch((err) => {
          setError('Token exchange failed.');
          setLoginSuccess(false);
        });
    }
  }, []);

  return (
    <div className="App" style={{ maxWidth: 400, margin: 'auto', padding: 32, fontFamily: 'sans-serif' }}>
      <h2>MCP Client PKCE Auth Demo</h2>
      {error && <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>}
      {!token ? (
        <>
          <button onClick={handleLogin} style={{ padding: 12, fontSize: 16 }}>Login with PKCE</button>
          {authUrl && <p>Redirecting to: <a href={authUrl}>{authUrl}</a></p>}
        </>
      ) : (
        <Chat token={token} />
      )}
    </div>
  );
}

export default App;
