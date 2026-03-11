# agent-mcpserver-chatbot-auth-enabled-
This project implements a chatbot application with a React-based frontend and an AI Agent backend. The agent is authenticated using Azure Entra ID tokens and dynamically interacts with tools hosted on an MCP Server. All tool communications are secured using bearer token authentication.
# PKCE + Azure Entra ID Authentication Architecture

Production-ready documentation for this repository's authentication flow across frontend, backend API, and MCP servers.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Repository Layout](#repository-layout)
- [Authentication Flow (End-to-End)](#authentication-flow-end-to-end)
- [Azure Entra ID App Registration Checklist](#azure-entra-id-app-registration-checklist)
- [Environment Variables](#environment-variables)
- [Local Development Setup](#local-development-setup)
- [Runtime Security Model](#runtime-security-model)
- [API and MCP Protection Details](#api-and-mcp-protection-details)
- [Troubleshooting](#troubleshooting)
- [Deployment Notes](#deployment-notes)
- [Hardening Recommendations](#hardening-recommendations)

## Overview

This project implements OAuth 2.0 Authorization Code Flow with PKCE for user sign-in and API access, backed by Azure Entra ID for token issuance and validation.

The implementation is split into three security boundaries:

1. Frontend SPA performs login, PKCE generation, and access token retrieval.
2. Backend API validates bearer tokens before exposing protected endpoints.
3. MCP servers validate JWT tokens and expose tools/resources only to authenticated clients.

## Architecture

### Components

- Frontend (`frontend/`): Initiates sign-in and sends bearer tokens to backend.
- Backend (`backend/`): Verifies JWTs and proxies/coordinates secure tool access.
- Email MCP Server (`email_mcp_server/`): JWT-protected FastMCP server for email intelligence tools.
- Math MCP Server (`math_mcp_server/`): JWT-protected MCP server for math tools.

### Identity Provider

- Provider: Azure Entra ID
- Token Type: JWT access token
- Validation Source: JWKS endpoint (`https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys`)

## Repository Layout

```text
MCP PKCE AUTH FLOW/
|- frontend/
|  |- src/
|  |  |- pkceUtils.js      # PKCE utilities: code verifier/challenge and token exchange
|  |  |- App.js            # App entry and auth wiring
|- backend/
|  |- main.py              # API entrypoint
|  |- modules/
|  |  |- auth.py           # Bearer token validation logic
|  |  |- agent.py          # MCP/backend orchestration logic
|  |  |- config.py         # App config/env handling
|- email_mcp_server/
|  |- server.py            # FastMCP server with JWTVerifier
|  |- README.md            # Service-specific docs
|- math_mcp_server/
|  |- server.py            # Math MCP endpoints/tools
|  |- mcp_middleware.py    # Middleware (listing/filter behavior)
```

## Authentication Flow (End-to-End)

### Step 1: PKCE Generation (Frontend)

The frontend generates:

- `code_verifier`: high-entropy random string
- `code_challenge`: Base64URL(SHA-256(code_verifier))

### Step 2: Authorization Request

The browser is redirected to Azure Entra ID authorize endpoint with:

- `client_id`
- `redirect_uri`
- `response_type=code`
- `scope`
- `code_challenge`
- `code_challenge_method=S256`

### Step 3: Authorization Code Return

Azure Entra ID redirects back with `code` to the SPA redirect URI.

### Step 4: Token Exchange

Frontend exchanges `code + code_verifier` at token endpoint and receives access token.

### Step 5: Backend API Access

Frontend sends `Authorization: Bearer <access_token>` to protected backend endpoints.

### Step 6: JWT Validation

Backend and MCP servers validate:

- JWT signature using JWKS
- issuer (`iss`)
- audience (`aud`)
- token lifetime (`exp`, `nbf`)

### Step 7: Authorized Execution

On successful validation, request proceeds to API/MCP tool handlers.

## Azure Entra ID App Registration Checklist

Use this checklist before first run:

1. Register application in Azure Entra ID.
2. Add SPA redirect URI(s) for local and production frontend.
3. Expose API scope or use app ID URI for audience.
4. Configure delegated permissions required by your app.
5. Enable public client flows only if your architecture requires it.
6. Capture and store the following values in environment variables:
   - Tenant ID
   - Client ID
   - API Audience / App ID URI

## Environment Variables

Recommended variables for this repository:

| Variable | Required | Description | Example |
|---|---|---|---|
| `TENANT_ID` | Yes | Azure Entra tenant GUID | `11111111-2222-3333-4444-555555555555` |
| `CLIENT_ID` | Yes | Application (client) ID | `aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee` |
| `API_AUDIENCE` | Yes | Expected `aud` claim | `api://aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee` |
| `FASTMCP_HOST` | No | MCP bind host | `0.0.0.0` |
| `FASTMCP_PORT` | No | MCP bind port | `8000` |
| `MCP_LOG_LEVEL` | No | Logging verbosity | `INFO` |

Example `.env`:

```env
TENANT_ID=11111111-2222-3333-4444-555555555555
CLIENT_ID=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
API_AUDIENCE=api://aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=8000
MCP_LOG_LEVEL=INFO
```

## Local Development Setup

### 1) Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

### 2) Email MCP Server

```bash
cd email_mcp_server
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python server.py
```

### 3) Math MCP Server

```bash
cd math_mcp_server
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python server.py
```

### 4) Frontend

```bash
cd frontend
npm install
npm start
```

## Runtime Security Model

Current model:

- Authentication: Enabled (JWT bearer validation)
- Authorization: Minimal claim checks (issuer/audience/lifetime)
- Role-based access control: Not enforced by default

This means valid authenticated users can access protected routes/tools unless additional claim-based policies are added.

## API and MCP Protection Details

### Backend

- `modules/auth.py` verifies incoming bearer token.
- Invalid/missing token returns HTTP 401.
- Protected endpoints include tool listing and chat execution routes.

### Email MCP Server

- Uses `JWTVerifier` with Entra JWKS URI.
- Verifies signature, issuer, algorithm, and audience.
- No mandatory role/scope enforcement unless explicitly configured.

### Math MCP Server

- Uses middleware and server-level authentication controls.
- Can be extended with additional claims policy checks.

## Troubleshooting

### Invalid Audience (`aud`)

- Ensure `API_AUDIENCE` exactly matches token `aud`.
- If using `api://<client-id>`, configure both app registration and server env consistently.

### Invalid Issuer (`iss`)

- Ensure issuer format matches expected tenant endpoint.
- v1/v2 tokens may have different issuer formats; keep validation config aligned.

### Signature Validation Failure

- Verify `TENANT_ID` is correct.
- Confirm JWKS endpoint is reachable from runtime environment.

### Token Works in Frontend but Fails in Backend

- Confirm backend and frontend use the same tenant/app registration.
- Confirm you are not mixing environments (dev vs prod app registrations).

### Wrong Python Environment / Pip

Always execute pip as module to avoid wrong-environment issues:

```bash
python -m pip --version
python -m pip install -r requirements.txt
```

## Deployment Notes

For GitHub and production readiness:

1. Never commit real secrets or production tenant values.
2. Commit only `.env.example`, not `.env`.
3. Add clear setup instructions in repository root `README.md`.
4. Pin dependency versions in each service `requirements.txt`.
5. Add CI checks for lint, tests, and import validation.

## Hardening Recommendations

To move from authentication-only to stronger authorization:

1. Enforce required scopes (for delegated flows).
2. Enforce app roles (for application access patterns).
3. Add per-tool authorization policies in MCP handlers.
4. Add audit logging for token subject, tenant, and action.
5. Add rate limiting and abuse protection at API gateway/server level.

---

If you use this document in GitHub, keep it versioned with code changes and update the Environment Variables and Flow sections whenever auth settings are modified.