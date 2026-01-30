from datetime import datetime, time
import pytz

IST = pytz.timezone("Asia/Kolkata")


def market_open():
    now = datetime.now(IST).time()
    return time(9, 15) <= now <= time(15, 30)
