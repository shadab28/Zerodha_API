from kiteconnect import KiteConnect
from dotenv import load_dotenv
import pandas as pd
import os
if __name__ == "__main__":
    load_dotenv(".env")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    key = os.getenv("KITE_API_KEY")
    secret = os.getenv("KITE_API_SECRET")
    kite = KiteConnect(api_key = key)
    print(kite.login_url())

    # kite = kiteconnect.access_token = secret
    code  = input("Enter the request_token by copying it from your browser: ")

    request_token = str(code)
    data = kite.generate_session(request_token, api_secret=secret)
    kite.set_access_token(data['access_token'])
    access_token = data['access_token']

    with open(".env", "r") as f:
        lines = f.readlines()

    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("KITE_ACCESS_TOKEN="):
                f.write(f"KITE_ACCESS_TOKEN={access_token}\n")
            else:
                f.write(line)

    print("✅ KITE_ACCESS_TOKEN updated in .env")

    historical_data = True

    if historical_data:
        instrument = 738561  # Example instrument token
        from_date = "2025-08-01"
        to_date = "2025-08-22"

        hist_data = kite.historical_data(instrument, from_date, to_date, interval="day")
        print(hist_data)


    download_instrumet = False
    if download_instrumet:
        for exchange in ['NSE', 'BSE']:
            instrument = kite.instruments(exchange)
            instrument = pd.DataFrame(instrument)
            instrument.to_csv(f'Csvs/{exchange}_all_instruments.csv',index=False)
            print("Data for", exchange, "downloaded", instrument.head())