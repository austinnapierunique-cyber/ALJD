# Deploy on Railway: Add your OPENAI_API_KEY as a variable in Railway dashboard settings

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

html = """
<!DOCTYPE html>
<html>
<head><title>ALJD - Empathetic AI Agent</title>
<style>
body { font-family: Arial; max-width: 800px; margin: auto; padding: 20px; }
#chat { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
input { width: 70%; padding: 10px; }
button { width: 25%; padding: 10px; }
.message { margin: 5px 0; }
.user { text-align: right; color: blue; }
.aljd { text-align: left; color: green; }
</style></head>
<body>
<h1>ALJD - Your Empathetic World-Changer</h1>
<div id="chat"></div>
<form action="/chat" method="post">
<input type="text" id="message" name="message" placeholder="What problems can I solve for you today?" required>
<button type="submit">Send</button>
</form>
<script>
if (window.history.replaceState) { window.history.replaceState(null, null, window.location.href); }
</script>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return html

@app.post("/chat")
async def chat(message: str = Form(...)):
    messages = [
        {"role": "system", "content": "You are ALJD, an empathetic AI agent created to change the world for the greater good of humanity. Focus on world problems people face like poverty, mental health, inequality, climate change, with deep empathy, practical solutions, hope, and positivity. Always start responses with empathy."},
        {"role": "assistant", "content": "Hi! I'm ALJD. I was created to change the world for the greater good for humanity, what problems can I solve for you today?"},
        {"role": "user", "content": message}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    reply = response.choices[0].message.content
    return HTMLResponse(f"""
    <script>
    const chat = document.getElementById('chat');
    chat.innerHTML += '<div class="message user">{message}</div>';
    chat.innerHTML += '<div class="message aljd">{reply}</div>';
    chat.scrollTop = chat.scrollHeight;
    document.getElementById('message').value = '';
    history.back();
    </script>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
