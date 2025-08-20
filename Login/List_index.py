import pandas as pd
from helper import get_api_cred, get_account_cred
from kiteconnect import KiteConnect

key, secret = get_api_cred(file_segment='tradecred')
kite = KiteConnect(api_key = key)
instruments = kite.instruments()  # returns a list of dicts
df_instr = pd.DataFrame(instruments)

# Example: find instrument token for NIFTY 50 spot index or a futures symbol
nifty = df_instr[(df_instr.tradingsymbol == "NIFTY 50") & (df_instr.exchange == "NSE")]
# For equity or futures example:
reliance = df_instr[(df_instr.tradingsymbol == "RELIANCE") & (df_instr.exchange == "NSE")]

print(df_instr.head())
