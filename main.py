import time
from datetime import datetime, time as dt_time,timedelta
from dotenv import load_dotenv
from kiteconnect import KiteConnect
import os
import NiftySymbol as ns
import pandas as pd

def is_market_open():
    # Example: Market open from 09:15 to 15:30 IST
    now = datetime.now().time()
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)
    return market_open <= now <= market_close

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

def get_symbol_from_token(tokens):
    ins = pd.read_csv("Csvs/NSE_all_instruments.csv")
    by_key = {
        (row["exchange"], row["instrument_token"]): row
        for _, row in ins.iterrows()
    }
    resolved = []
    for s in tokens:
        key = ("NSE", s)
        if key not in by_key:
            raise RuntimeError(f"Instrument not found: {key}")
        row = by_key[key]
        resolved.append(row["tradingsymbol"])
    return resolved

def check_signal(filter_data):
    # Calculate 50-period and 200-period moving averages on 'close' column
    filter_data['MA_50'] = filter_data['close'].rolling(window=50).mean()
    filter_data['MA_200'] = filter_data['close'].rolling(window=200).mean()

    last_close = filter_data.iloc[-1]['close']
    last_ma_50 = filter_data.iloc[-1]['MA_50']
    last_ma_200 = filter_data.iloc[-1]['MA_200']
    prev_close = filter_data.iloc[-2]['close']
    if last_close > last_ma_50 > last_ma_200:
        return "BUY"
    elif last_close < last_ma_50 < last_ma_200:
        return "SELL"
    else:
        return "HOLD"  # or whatever you want for else case

def place_order(symbol, quantity, signal):
    kite.place_order(
        tradingsymbol=order["symbol"], 
        price=order["close"],
        quantity=quantity, 
        exchange=kite.EXCHANGE_NSE, 
        order_type=kite.ORDER_TYPE_LIMIT,
        transaction_type= kite.TRANSACTION_TYPE_BUY,
        product=kite.PRODUCT_MIS, 
        variety=kite.VARIETY_REGULAR, 
        tag="OrderPlacedByPython"
        )
        
    print(f"Order placed for {symbol} with quantity {quantity} and signal {signal}")

def place_amo_order(symbol, quantity, signal):
    kite.place_order(
        tradingsymbol=order["symbol"], 
        price=order["close"],
        quantity=quantity, 
        exchange=kite.EXCHANGE_NSE, 
        order_type=kite.ORDER_TYPE_LIMIT,
        transaction_type= kite.TRANSACTION_TYPE_BUY,
        product=kite.PRODUCT_MIS, 
        variety=kite.VARIETY_AMO, 
        tag="OrderPlacedByPython"
        )
        
    print(f"After Market Order placed for {symbol} with quantity {quantity} and signal {signal}")

if __name__ == "__main__":
    instrument = ns.mystocks  # Example instrument list
    if not instrument:
        raise RuntimeError("No instruments found in NiftySymbol.py")
    tokens = get_token_from_symbol(instrument)
    load_dotenv("..env")
    api_key = os.getenv("KITE_API_KEY")
    secret = os.getenv("KITE_API_SECRET")
    access_token = os.getenv("KITE_ACCESS_TOKEN")
    kite = KiteConnect(api_key)
    kite.set_access_token(access_token)

    while True:
        if not is_market_open():
            print("Market open. Processing data...")
            to_date=datetime.now().strftime("%Y-%m-%d")
            from_date = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
            orderbook = []
            for token in tokens:
                hist_data = kite.historical_data(token, from_date, to_date, interval="5minute")
                filter_data = pd.DataFrame(hist_data).sort_values(by='date').tail(200).iloc[::-1]
                signal = check_signal(filter_data)
                if signal != "HOLD":
                    symbol = get_symbol_from_token([token])[0]
                    orderbook.append({"symbol": symbol, "signal": signal, "close": float(filter_data.iloc[-1]['close'])})
        else:
            print("Market closed. Skipping data processing.")
        for order in orderbook:
            quantity = round(10000 / order["close"])
            # print(f"Placing order for {order['symbol']} with quantity {quantity} and signal {order['signal']}")
            if is_market_open():
                place_order(order["symbol"], quantity, order["signal"])
            else:
                place_amo_order(order["symbol"], quantity, order["signal"])
            
        print("Sleeping for 5 minutes...")
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)

