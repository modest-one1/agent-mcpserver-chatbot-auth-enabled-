import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", None)
    AUDIENCE = os.getenv("CLIENT_ID", None)
    MCP_CONNECTIONS_JSON = os.getenv("MCP_CONNECTIONS_JSON", "{}")
    REACT_BUILD_DIR = os.getenv("REACT_BUILD_DIR", "./frontend/build")
    JWKS_URL = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys" if AZURE_TENANT_ID else None
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    EMAIL_SERVER_URL = os.getenv("EMAIL_SERVER_URL", "http://localhost:8000/mcp")
    MATH_SERVER_URL = os.getenv("MATH_SERVER_URL", "http://localhost:9001/mcp")
    EMAIL_TRANSPORT = os.getenv("EMAIL_TRANSPORT", "streamable_http")
    MATH_TRANSPORT = os.getenv("MATH_TRANSPORT", "streamable_http")
