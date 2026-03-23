from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
conversations = {}

class Message(BaseModel):
    text: str
    conversation_id: Optional[str] = "default"

@app.get("/", response_class=HTMLResponse)
def home():
    return {"status": "ALJD is running!"}

@app.post("/chat")
def chat(msg: Message):
    if msg.conversation_id not in conversations:
        conversations[msg.conversation_id] = []
    conversations[msg.conversation_id].append({"role": "user", "content": msg.text})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are ALJD, a helpful AI assistant."}] + conversations[msg.conversation_id][-20:]
    )
    reply = response.choices[0].message.content
    conversations[msg.conversation_id].append({"role": "assistant", "content": reply})
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
