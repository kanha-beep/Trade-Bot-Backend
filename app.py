# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from vcp.state import state
from contextlib import asynccontextmanager
# from main import main
from vcp.vcpBot import vcpBot
import numpy as np
# from vcp.all_symbols import ALL_SYMBOLS
from vcp.trade_engine_loop import trade_engine_loop
from vcp.all_sym import get_nse_yfinance_symbols

def to_py(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: to_py(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_py(v) for v in obj]
    return obj

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting VCP scanner...")
    ALL_SYMBOLS = get_nse_yfinance_symbols(validate=False)
    print(f"Total Stocks: {len(ALL_SYMBOLS)}")
    scan_thread = threading.Thread(
        target=vcpBot,
        args=(ALL_SYMBOLS,),
        daemon=True
    )
    scan_thread.start()

    print("Starting trade engine...")
    trade_thread = threading.Thread(
        target=trade_engine_loop,
        daemon=True
    )
    trade_thread.start()

    yield
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     print("starting bot from app")
#     thread = threading.Thread(target=vcpBot,args=(ALL_SYMBOLS,), daemon=True)
#     thread.start()
#     print(f"bot started {thread.is_alive()}")
#     yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    return to_py(state)

@app.get("/trades")
def trades():
    return to_py(state.get("trades", []))