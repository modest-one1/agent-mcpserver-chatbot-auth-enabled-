// pkceUtils.js
// Utility functions for PKCE flow

function dec2hex(dec) {
  return dec.toString(16).padStart(2, '0');
}

export function generateCodeVerifier() {
  const array = new Uint8Array(32);
  window.crypto.getRandomValues(array);
  return Array.from(array, dec2hex).join('');
}

export async function generateCodeChallenge(codeVerifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await window.crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

export function getAuthUrl(authEndpoint, clientId, redirectUri, codeChallenge) {
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: clientId,
    redirect_uri: redirectUri,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256',
    scope: process.env.REACT_APP_SCOPES
  });
  return `${authEndpoint}?${params.toString()}`;
}

export async function exchangeToken(tokenEndpoint, clientId, code, codeVerifier, redirectUri) {
  const params = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: clientId,
    code,
    code_verifier: codeVerifier,
    redirect_uri: redirectUri,
  });
  const response = await fetch(tokenEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString(),
  });
  const data = await response.json();
  return data.access_token || JSON.stringify(data);
}
