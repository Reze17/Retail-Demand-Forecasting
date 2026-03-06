from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes.health import health_check_router
from app.api.routes.call import call_router
from app.core.process import chat_agent   # your async function that creates the agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print("Starting up: creating agent and MCP client...")
    agent = await chat_agent()           # create the agent once
    app.state.agent = agent               # store in app.state for reuse
    print("Agent ready.")
    yield
    # --- Shutdown ---
    print("Shutting down: cleaning up MCP client...")
    # If the agent or its client has a close method, call it
    if hasattr(agent, "client") and hasattr(agent.client, "close"):
        await agent.client.close()
    # If the client provides an async aclose method, use it
    # Alternatively, if MultiServerMCPClient has its own cleanup, adjust accordingly
    print("Cleanup done.")

# Attach lifespan to the FastAPI app
app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_check_router)
app.include_router(call_router)

# Static files and frontend route (unchanged)
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_chat_interface():
    html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "API is running. Place index.html in static folder."}