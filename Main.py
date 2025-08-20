from kiteconnect import KiteTicker
import time
from Login.helper import get_api_cred

API_KEY = get_api_cred(file_segment='tradecred')[0]

with open("access_token.txt", "r") as f:
    ACCESS_TOKEN = f.read().strip()

ws = KiteTicker(API_KEY, ACCESS_TOKEN)

import pandas as pd

df_instr = pd.DataFrame(pd.read_csv("Csvs/NSE_all_instruments.csv"))

nifty = df_instr[(df_instr.tradingsymbol == "NIFTY 50") & (df_instr.exchange == "NSE")]
# For equity or futures example:
reliance = df_instr[(df_instr.tradingsymbol == "RELIANCE") & (df_instr.exchange == "NSE")]

# print(df_instr.head())
# Build list of instrument tokens
TOKENS = int(reliance.iloc[0]["instrument_token"])
print(TOKENS)

def on_connect(ws, response):
    ws.subscribe(TOKENS)
    ws.set_mode(ws.MODE_FULL, TOKENS)  # FULL gives depth + more fields

def on_ticks(ws, ticks):
    # ticks is a list of dicts, one per subscribed token
    for t in ticks:
        token = t["instrument_token"]
        ltp = t.get("last_price")
        volume = t.get("volume_traded")
        # process or enqueue for strategy
        process_tick(t)

def on_error(ws, code, reason):
    print("WS error:", code, reason)

def on_close(ws, code, reason):
    print("WS closed:", code, reason)

ws.on_connect = on_connect
ws.on_ticks = on_ticks
ws.on_error = on_error
ws.on_close = on_close

# Start event loop (blocks)
ws.connect(threaded=True)

# Keep main thread alive (or manage with proper service/supervisor)
while True:
    time.sleep(1)
