from kiteconnect import KiteConnect
from helper import get_api_cred, get_account_cred
import pandas as pd
key, secret = get_api_cred(file_segment='tradecred')
username, password, googleauth = get_account_cred(file_segment='accountcred')

if __name__ == "__main__":
    kite = KiteConnect(api_key = key)
    print(kite.login_url())

    # kite = kiteconnect.access_token = secret
    code  = input("Enter the request_token by copying it from your browser: ")

    request_token = str(code)
    data = kite.generate_session(request_token, api_secret=secret)
    kite.set_access_token(data['access_token'])
    access_token = data['access_token']

    # Optional: persist to a file for reuse in the same day
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    print("🚀Kite Session Created successfully")

    download_instrumet = False
    if download_instrumet:
        for exchange in ['NSE', 'BSE']:
            instrument = kite.instruments(exchange)
            instrument = pd.DataFrame(instrument)
            instrument.to_csv(f'Csvs/{exchange}_all_instruments.csv',index=False)
            print(instrument)