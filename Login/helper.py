import os
from configparser import ConfigParser

folder = os.path.dirname(os.path.abspath(__file__))

def get_api_cred(file_segment):
    configur = ConfigParser()
    path = os.path.join(folder, 'cred.ini')
    configur.read(path)
    if not configur.has_section(file_segment):
        raise ValueError(f"❌ Missing section: [{file_segment}] in cred.ini")
    try:
        key = configur.get(file_segment, 'key')
        secret = configur.get(file_segment, 'secret')
    except Exception as e:
        raise ValueError(f"❌ Error reading credentials: {e}")
    return key, secret

# key, secret= (get_api_cred(file_segment='tradecred'))
# print(key, secret)

def get_account_cred(file_segment):
    configur = ConfigParser()
    path = os.path.join(folder, 'cred.ini')
    configur.read(path)
    if not configur.has_section(file_segment):
        raise ValueError(f"❌ Missing section: [{file_segment}] in cred.ini")
    try:
        username = configur.get(file_segment, 'username')
        password = configur.get(file_segment, 'password')
        googleauth = configur.get(file_segment, 'googleauth')
    except Exception as e:
        raise ValueError(f"❌ Error reading credentials: {e}")
    return username, password, googleauth