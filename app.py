# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from five_start_trade import state
from contextlib import asynccontextmanager
from main import main

# try:
#     from five_start_trade import state
# except ImportError:
#     state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("starting bot from app")
    thread = threading.Thread(target=main, daemon=True)
    thread.start()
    print(f"bot started {thread.is_alive()}")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# def start_bot():
#     from main import main

#     threading.Thread(target=main, daemon=True).start()


@app.get("/")
def root():
    return {"message": "Trading API is running"}


@app.get("/status")
def status():
    return {"status": "running"}


@app.get("/positions")
def positions():
    return state
