import pickle
from google.auth.transport.requests import Request

def get_access_token():
    try:
        with open("token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)

        if creds and creds.valid:
            print(f"Your Access Token: {creds.token}")
        elif creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh the token if expired
            print(f"Your New Access Token: {creds.token}")
        else:
            print("No valid credentials found. Re-authenticate your app.")
    except Exception as e:
        print(f"Error loading token: {e}")

get_access_token()
