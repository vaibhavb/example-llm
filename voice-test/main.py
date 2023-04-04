from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging
import openai

app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
chat_history = []
voice_history = {}

@app.get("/")
async def read_root():
  return HTMLResponse(content=open("index.html", "r").read(), status_code=200)


@app.get("/tony")
async def get(request: Request):
  return templates.TemplateResponse("tony.html", {"request": request})


@app.post("/whisper")
async def whisper(request: Request):
  data = await request.json()
  text = data.get("text", "")

  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Q: {text}\nA:",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
  )
  generated_text = response.choices[0].text.strip()

  return {"text": generated_text}


@app.post("/ask")
async def ask(request: Request):
  # Receive and send back the client message
  data = await request.json()
  question = data.get("question", "")
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Q: {question}\nA:",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
  )
  answer = response.choices[0].text.strip()
  chat_history.append((question, answer))
  return {"answer": answer}

@app.post("/voice_webhook")
async def voice(request: Request):
  voice_url = "test"
  data = await request.json()
  print(data)
  return {"voice_url": voice_url}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=9000)
