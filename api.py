# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from five_start_trade import state
except ImportError:
    state = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Trading API is running"}

@app.get("/status")
def status():
    return {"status": "running"}

@app.get("/positions")
def positions():
    return state