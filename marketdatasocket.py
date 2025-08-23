from kiteconnect import KiteConnect, KiteTicker
import os
from dotenv import load_dotenv
import NiftySymbol as ns
import pandas as pd

def get_token_from_symbol(symbols):
    ins = pd.read_csv("Csvs/NSE_all_instruments.csv")
    by_key = {
        (row["exchange"], row["tradingsymbol"]): row
        for _, row in ins.iterrows()
    }
    resolved = []
    for s in symbols:
        key = ("NSE", s)
        if key not in by_key:
            raise RuntimeError(f"Instrument not found: {key}")
        row = by_key[key]
        resolved.append(row["instrument_token"])
    return resolved

class KiteMarketDataSocket:
    def __init__(self, token_list):
        load_dotenv("..env")
        api_key = os.getenv("KITE_API_KEY")
        access_token = os.getenv("KITE_ACCESS_TOKEN")

        self.token_list = token_list
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)
        
        self.kws = KiteTicker(api_key, access_token)

        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self.kws.on_error = self.on_error
        self.kws.on_disconnect = self.on_disconnect

    def on_connect(self, ws, response):
        print("Connected. Subscribing to tokens:", self.token_list)
        ws.subscribe(self.token_list)
        # ws.set_mode(ws.MODE_LTP, self.token_list)  # Receive full tick data
        print("Subscribed to tokens:", self.token_list)

    def on_ticks(self, ws, ticks):
        # Called when ticks received
        print("Ticks:", ticks)
        # Process tick data here

    def on_close(self, ws, code, reason):
        print(f"Connection closed. Code: {code}, Reason: {reason}") 

    def on_error(self, ws, error):
        print("Error:", error)

    def on_disconnect(self, ws, code, reason):
        print(f"Disconnected. Code: {code}, Reason: {reason}")

    def connect(self):
        self.kws.connect()

if __name__ == "__main__":
    # List of instrument tokens to track; replace with actual tokens you want
    instruments = ns.NiftyMidcap100
    tokens = get_token_from_symbol(instruments)
    md_socket = KiteMarketDataSocket(tokens)
    md_socket.connect()
