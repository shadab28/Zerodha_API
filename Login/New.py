from kiteconnect import KiteConnect

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

kite = KiteConnect(api_key=API_KEY)

print("Login URL:", kite.login_url())
# 1) Visit printed URL, complete login, and you'll be redirected with ?request_token=XXXX
request_token = "paste_from_redirect"

data = kite.generate_session(request_token, api_secret=API_SECRET)
access_token = data["access_token"]
kite.set_access_token(access_token)

# Optional: persist to a file for reuse in the same day
with open("access_token.txt", "w") as f:
    f.write(access_token)

