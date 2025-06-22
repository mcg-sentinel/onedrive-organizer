import msal
import os
import webbrowser

CLIENT_ID = os.getenv("ONEDRIVE_CLIENT_ID", "YOUR_CLIENT_ID")
TENANT_ID = os.getenv("ONEDRIVE_TENANT_ID", "common")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Files.ReadWrite.All", "Sites.ReadWrite.All", "offline_access"]

def get_token():
    """Authenticate via device code flow and return an access token."""
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError("Failed to create device flow")
    print(f"Please go to {flow['verification_uri']} and enter code {flow['user_code']}")
    webbrowser.open(flow["verification_uri"])
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        return result["access_token"]
    raise RuntimeError(f"Failed to acquire token: {result.get('error_description')}")
