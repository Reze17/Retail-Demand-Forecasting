from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse

call_router = APIRouter(tags=["call"])

# Config can stay as before; it's small and stateless
config = {
    "configurable": {
        "thread_id": "1"
    }
}

@call_router.post("/call")
async def chat(request: Request, query: str = Form(...)):
    agent = request.app.state.agent   # get the singleton agent
    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    }, config)
    return JSONResponse(content={"message": response["messages"][-1].content})