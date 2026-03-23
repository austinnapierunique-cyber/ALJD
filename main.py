from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ALJD AI Agent</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: sans-serif; background: #0f0f0f; color: #fff; height: 100vh; display: flex; flex-direction: column; }
  #header { padding: 16px 20px; background: #1a1a1a; border-bottom: 1px solid #333; text-align: center; }
  #header h1 { font-size: 1.4rem; color: #4af; }
  #header p { font-size: 0.8rem; color: #888; margin-top: 4px; }
  #messages { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
  .msg { max-width: 80%; padding: 12px 16px; border-radius: 18px; line-height: 1.5; font-size: 0.95rem; }
  .user { background: #4af; color: #000; align-self: flex-end; border-bottom-right-radius: 4px; }
  .bot { background: #1e1e1e; color: #eee; align-self: flex-start; border-bottom-left-radius: 4px; border: 1px solid #333; }
  .typing { color: #888; font-style: italic; }
  #input-area { padding: 16px; background: #1a1a1a; border-top: 1px solid #333; display: flex; gap: 10px; }
  #input { flex: 1; padding: 12px 16px; border-radius: 24px; border: 1px solid #444; background: #2a2a2a; color: #fff; font-size: 1rem; outline: none; }
  #input:focus { border-color: #4af; }
  #send { padding: 12px 20px; background: #4af; color: #000; border: none; border-radius: 24px; font-weight: bold; cursor: pointer; font-size: 1rem; }
  #send:disabled { background: #555; color: #888; cursor: not-allowed; }
</style>
</head>
<body>
<div id="header">
  <h1>ALJD</h1>
  <p>Your personal AI agent</p>
</div>
<div id="messages">
  <div class="msg bot">Hi! I'm ALJD, your personal AI assistant. How can I help you today?</div>
</div>
<div id="input-area">
  <input id="input" type="text" placeholder="Type a message..." autocomplete="off" />
  <button id="send">Send</button>
</div>
<script>
  const messages = document.getElementById('messages');
  const input = document.getElementById('input');
  const sendBtn = document.getElementById('send');
  function addMsg(text, role) {
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }
  async function send() {
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    sendBtn.disabled = true;
    addMsg(text, 'user');
    const typing = addMsg('Thinking...', 'bot typing');
    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      typing.textContent = data.reply;
      typing.classList.remove('typing');
    } catch {
      typing.textContent = 'Something went wrong. Please try again.';
    }
    sendBtn.disabled = false;
    input.focus();
  }
  sendBtn.addEventListener('click', send);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
</script>
</body>
</html>"""

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
