# Modular FastAPI app setup
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from modules.config import Config
from modules.auth import verify_bearer_token
from modules.agent import build_agent
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(title="FastAPI backend with LangChain MCP integration")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    metadata: dict | None = None

class TokenLogRequest(BaseModel):
    token: str

agent_executor = None
available_tools = []

@app.get("/api/tools")
async def get_tools_endpoint(request: Request):
    auth_header = request.headers.get("authorization")
    await verify_bearer_token(auth_header)
    return {"tools": available_tools}

@app.post("/api/chat")
async def chat(req: ChatRequest, request: Request):
    auth_header = request.headers.get("authorization")
    await verify_bearer_token(auth_header)
    print("Received chat request with message:", req.message)
    global agent_executor, available_tools
    access_token = auth_header.split()[1] if auth_header else None
    if agent_executor is None:
        agent_executor, tools = await build_agent(access_token)
        if not tools:
            raise HTTPException(status_code=500, detail="No tools available from MCP servers")
        available_tools = [{"name": t.name, "description": getattr(t, "description", "")} for t in tools]
    user_message = req.message
    metadata = req.metadata or {}
    import asyncio, traceback
    async def run_agent_in_thread(prompt_text: str):
        input = {
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt_text},
            ]
            
        }
        loop = asyncio.get_running_loop()
        # Use run_in_executor to handle the synchronous invocation
        return await loop.run_in_executor(None, agent_executor.ainvoke, input)
    try:
        result = await run_agent_in_thread(user_message)
        if isinstance(result, dict):
          result_text = result['messages'][-1].content if 'messages' in result and result['messages'] else str(result)
        else:
            result = await result
            result_text = result['messages'][-1].content if 'messages' in result and result['messages'] else str(result)
    except Exception as e:
        tb = traceback.format_exc()
        print("Agent execution error:", e, tb)
        raise HTTPException(status_code=500, detail=f"Agent execution error: {e}")
    return {"message": result_text}

@app.post("/api/log-token")
async def log_token(req: TokenLogRequest):
    token_value = (req.token or "").replace("\n", "\\n")
    timestamp = datetime.utcnow().isoformat() + "Z"
    log_path = r"C:\Users\sandav\Downloads\MCP PKCE AUTH FLOW\backend\token.log"
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} {token_value}\n")
    return {"status": "logged"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
