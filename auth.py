from msal import PublicClientApplication, ConfidentialClientApplication
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = [
    "https://analysis.windows.net/powerbi/api/Report.Read.All",
    # "offline_access",
]


app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY,
)


def build_auth_url():
    return app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)


def get_token_by_auth_code(code: str):
    return app.acquire_token_by_authorization_code(
        code, scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
