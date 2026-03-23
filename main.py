from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html>
<head><title>ALJD</title>
<style>body{font-family:Arial;max-width:800px;margin:auto;padding:20px;}
#chat{border:1px solid #ccc;height:400px;overflow-y:scroll;padding:10px;margin-bottom:10px;}
input{width:70%;padding:10px;}button{width:25%;padding:10px;}
.message{margin:5px 0;}.user{text-align:right;color:blue;}.aljd{text-align:left;color:green;}
</style></head>
<body>
<h1>🤖 ALJD - World Changer</h1>
<div id="chat">Hi! I'm ALJD. I was created to change the world for the greater good for humanity, what problems can I solve for you today?</div>
<form action="/chat" method="post">
<input type="text" name="message" placeholder="Your message..." required>
<button>Send</button>
</form>
<script>
if (window.history.replaceState) { window.history.replaceState(null, null, window.location.href); }
</script>
</body></html>
"""

@app.post("/chat")
async def chat(message: str = Form(...)):
    messages = [
        {"role": "system", "content": "You are ALJD, deeply empathetic AI focused on world problems (poverty, mental health, inequality, climate). Always respond with compassion, practical solutions, and hope."},
        {"role": "user", "content": message}
    ]
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.7)
    return HTMLResponse(f"""
    <script>
    const chat = document.getElementById('chat');
    chat.innerHTML += '<div class="message user">{message}</div>';
    chat.innerHTML += '<div class="message aljd">{response.choices[0].message.content}</div>';
    chat.scrollTop = chat.scrollHeight;
    history.back();
    </script>
    """)
