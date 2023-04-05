from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging, openai


app = FastAPI()

templates = Jinja2Templates(directory="templates")

# A dictionary to store webhook requests
voice_webhook_requests = {}

chat_history = []

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
  data = await request.json()
  print(data)
  voice_webhook_requests[data.get("id")] = data.get("url");
  return {"id": data.get("id"), "message": "successful"}

@app.get("/voice_webhook/{request_id}")
def get_voice_webhook_request(request_id: str):
    print(request_id)
    if request_id in voice_webhook_requests:
        return voice_webhook_requests[request_id]
    else:
        raise HTTPException(status_code=404, detail="Request ID not found")

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=9000)
