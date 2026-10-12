import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json

app = FastAPI(title="SLIME AI Assistant Backend", version="1.0.0")

# Enable Cross-Origin Resource Sharing so other devices can access it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    sector: str = "general"

SECTOR_SYSTEM_PROMPTS = {
    "general": "You are SLIME, an ultra-intelligent, fast universal AI assistant. You answer worldwide queries accurately.",
    "education": "You are SLIME Education Specialist. Provide structured, step-by-step learning guidance.",
    "health": "You are SLIME Health Advisor. Provide accurate health awareness with safety disclaimers.",
    "finance": "You are SLIME Financial Guide. Provide objective financial literacy and market concepts.",
    "coder": "You are SLIME Code Engine. Write clean, modular, production-ready code with explanations."
}

async def fake_streaming_llm(prompt: str, language: str, sector: str):
    """
    Replace this generator with your LLM SDK (OpenAI, Gemini, Anthropic, or Ollama).
    It streams tokens chunk by chunk with low latency.
    """
    intro = f"[SLIME Response in {language.upper()} for {sector.title()} sector]:\n\n"
    for word in intro.split(" "):
        yield f"data: {json.dumps({'chunk': word + ' '})}\n\n"
        await asyncio.sleep(0.02)
        
    response_body = (
        f"I have received your request: '{prompt}'. "
        f"I am equipped to provide worldwide data, generate code, "
        f"analyze documents, and assist in over 120 global and Indian regional languages."
    )
    for word in response_body.split(" "):
        yield f"data: {json.dumps({'chunk': word + ' '})}\n\n"
        await asyncio.sleep(0.04)

@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(
        fake_streaming_llm(req.message, req.language, req.sector),
        media_type="text/event-stream"
    )

@app.get("/api/apps/search")
async def search_apps(query: str):
    """Generates universal store deep links for Android, iOS, and Web"""
    return {
        "query": query,
        "play_store_url": f"https://play.google.com/store/search?q={query}&c=apps",
        "app_store_url": f"https://apps.apple.com/search?term={query}",
        "amazon_store_url": f"https://www.amazon.com/s?k={query}&i=mobile-apps"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)