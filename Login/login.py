from kiteconnect import KiteConnect
from helper import get_api_cred, get_account_cred

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
    print("🚀Kite Session Created successfully")

    # instrument = kite.instruments("NSE")
    # instrument = pd.DataFrame(instrument)
    # # instrument.to_csv('instrument.csv',index=False)
    # print(instrument)