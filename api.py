# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from five_start_trade import state
from bot import bot
from main import main
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# def start_bot():
#     thread = threading.Thread(target=main, daemon=True)
#     thread.start()


@app.get("/status")
def status():
    return {"status": "running"}


@app.get("/positions")
def positions():
    return {"positions": state, "count": len(state)}
