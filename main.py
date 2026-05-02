from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from bot import compose, handle_reply

app = FastAPI(title="Magicpin Vera AI Challenge")

@app.get("/")
async def root():
    """Redirect root to docs"""
    return RedirectResponse(url="/docs")


# In-memory stores for context and state
contexts_store: Dict[str, dict] = {}
user_states: Dict[str, dict] = {}

# Pydantic models for request validation
class ContextPayload(BaseModel):
    category: dict
    merchant: dict
    trigger: dict
    customer: Optional[dict] = None

class TickPayload(BaseModel):
    context_id: str

class ReplyPayload(BaseModel):
    merchant_id: str
    reply_text: str

@app.post("/v1/context")
async def create_context(payload: ContextPayload):
    """
    Stores or prepares context for processing
    """
    # Generate a simple context ID (in production, use UUID)
    context_id = f"ctx_{len(contexts_store) + 1}"
    contexts_store[context_id] = payload.model_dump()
    
    return {"context_id": context_id, "status": "stored"}

@app.post("/v1/tick")
async def process_tick(payload: TickPayload):
    """
    Uses the provided context to call compose() and return the generated message.
    """
    context_id = payload.context_id
    if context_id not in contexts_store:
        raise HTTPException(status_code=404, detail="Context not found")
        
    context = contexts_store[context_id]
    
    # Generate the message
    result = compose(
        category=context.get("category", {}),
        merchant=context.get("merchant", {}),
        trigger=context.get("trigger", {}),
        customer=context.get("customer")
    )
    return result

@app.post("/v1/reply")
async def process_reply(payload: ReplyPayload):
    """
    Accepts merchant reply text and returns the next response.
    """
    merchant_id = payload.merchant_id
    if merchant_id not in user_states:
        user_states[merchant_id] = {"history": []}
        
    state = user_states[merchant_id]
    result = handle_reply(payload.reply_text, state)
    
    # Update the state with new history
    user_states[merchant_id] = result.get("state", state)
    
    return {"response": result["response"]}

@app.get("/v1/healthz")
async def health_check():
    """
    Returns API health status.
    """
    return {"status": "ok"}

@app.get("/v1/metadata")
async def get_metadata():
    """
    Returns bot info (name, version, description).
    """
    return {
        "name": "Vera",
        "version": "1.0.0",
        "description": "Vera AI messaging bot for merchant engagement and customer recall."
    }
