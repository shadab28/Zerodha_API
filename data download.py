import time
from datetime import datetime, time as dt_time,timedelta
from dotenv import load_dotenv
from kiteconnect import KiteConnect
import os
import NiftySymbol as ns
import pandas as pd


def get_token_from_symbol(symbols):
    ins = pd.read_csv("Csvs/BSE_all_instruments.csv")
    by_key = {
        (row["exchange"], row["tradingsymbol"]): row
        for _, row in ins.iterrows()
    }
    resolved = []
    for s in symbols:
        key = ("BSE", s)
        if key not in by_key:
            print(f"Skipping symbol, instrument not found: {key}")
            continue  # Skip if not found
        row = by_key[key]
        resolved.append(row["instrument_token"])
    return resolved


def get_symbol_from_token(tokens):
    ins = pd.read_csv("Csvs/BSE_all_instruments.csv")
    by_key = {
        (row["exchange"], row["instrument_token"]): row
        for _, row in ins.iterrows()
    }
    resolved = []
    key = ("BSE", tokens)
    if key not in by_key:
        raise RuntimeError(f"Instrument not found: {key}")
    row = by_key[key]
    resolved.append(row["tradingsymbol"])
    return resolved[0]

def daterange_batches(start_date, end_date, batch_days=400):
    """Yield (from_date, to_date) pairs of max batch_days each within start and end date."""
    current = start_date
    while current < end_date:
        batch_end = min(current + timedelta(days=batch_days), end_date)
        yield current.strftime("%Y-%m-%d"), batch_end.strftime("%Y-%m-%d")
        current = batch_end + timedelta(days=1)

tokens = [...]  # your list of tokens
token_stockname_map = {...}  # token to stock name mapping, optional

if __name__ == "__main__":
    instrument = ns.bse_stock  # Example instrument list
    if not instrument:
        raise RuntimeError("No instruments found in NiftySymbol.py")
    tokens = get_token_from_symbol(instrument)
    load_dotenv(".env")
    api_key = os.getenv("KITE_API_KEY")
    secret = os.getenv("KITE_API_SECRET")
    access_token = os.getenv("KITE_ACCESS_TOKEN")
    kite = KiteConnect(api_key,disable_ssl=True)
    kite.set_access_token(access_token)
    to_date = datetime.now().strftime("%Y-%m-%d")
    # from_date = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    from_date = "2000-01-01"
    orderbook = []
    try:
        for token in tokens:
            all_batches = []
            start = datetime.strptime("2000-01-01", "%Y-%m-%d")
            end = datetime.now()
            stock_name = get_symbol_from_token(token)
            for from_date, to_date in daterange_batches(start, end, 400):
                hist_data = kite.historical_data(token, from_date, to_date, interval="day")
                all_batches.extend(hist_data)
                # print(f"Downloaded data for {stock_name} from {from_date} to {to_date}")
            df = pd.DataFrame(all_batches)
            df.to_csv(f"stock_data/{stock_name}.csv", index=False)
            print(f"Downloaded data for {stock_name} from {from_date} to {to_date}")
    except Exception as e:
        print(f"could not download data for {stock_name} due to {e}")
