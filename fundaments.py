import os
import time
import base64
import requests
import msal
from dotenv import load_dotenv

# --- Configurações e cache em disco ---
load_dotenv()
CLIENT_ID    = os.getenv("AZURE_CLIENT_ID")
TENANT_ID    = os.getenv("AZURE_TENANT_ID", "common")
SCOPES       = [s.strip() for s in os.getenv("SCOPES","Mail.ReadWrite").split(",")]
GRAPH_API    = "https://graph.microsoft.com/v1.0"
OUTPUT_DIR   = "bils"
INTERVAL     = int(os.getenv("CHECK_INTERVAL","60"))
SUBJECT_KEY  = "beneficios"
CACHE_PATH   = "token_cache.bin"

# prepara cache MSAL
cache = msal.SerializableTokenCache()
if os.path.exists(CACHE_PATH):
    cache.deserialize(open(CACHE_PATH, "r").read())

authority = f"https://login.microsoftonline.com/{TENANT_ID}"
app = msal.PublicClientApplication(
    client_id=CLIENT_ID,
    authority=authority,
    token_cache=cache
)

def save_cache():
    if cache.has_state_changed:
        open(CACHE_PATH, "w").write(cache.serialize())

def get_token():
    # silent first
    accounts = app.get_accounts()
    if accounts:
        for acct in accounts:
            result = app.acquire_token_silent(SCOPES, account=acct)
            if result and "access_token" in result:
                print("DEBUG token obtido via cache")
                return result["access_token"]

    # device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    print(flow["message"])  # instruções no console
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError("Falha ao obter token:\n" + str(result))
    print("DEBUG token_response keys:", list(result.keys()))
    save_cache()
    return result["access_token"]

def fetch_messages(token):
    url = f"{GRAPH_API}/me/mailFolders/Inbox/messages"
    params = {
        "$filter": f"isRead eq false and subject eq '{SUBJECT_KEY}'",
        "$select": "id,subject",
        "$top": "50"
    }
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params)
    print("DEBUG fetch_messages status:", resp.status_code)
    resp.raise_for_status()
    msgs = resp.json().get("value", [])
    print(f"DEBUG: {len(msgs)} mensagens não lidas com assunto '{SUBJECT_KEY}'")
    return msgs

def save_attachments(token, msg):
    # download de anexos
    att_url = f"{GRAPH_API}/me/messages/{msg['id']}/attachments"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(att_url, headers=headers)
    print("DEBUG attachments status:", resp.status_code)
    resp.raise_for_status()

    atts = resp.json().get("value", [])
    if not atts:
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for att in atts:
        if att.get("@odata.type")=="#microsoft.graph.fileAttachment" and att.get("contentType")=="application/pdf":
            name = att["name"]
            data = att["contentBytes"]
            path = os.path.join(OUTPUT_DIR, name)
            with open(path, "wb") as f:
                f.write(base64.b64decode(data))
            print(f"Novo arquivo recebido: {name}")

    # marcar como lida
    try:
        patch_url = f"{GRAPH_API}/me/messages/{msg['id']}"
        patch = requests.patch(
            patch_url,
            headers={**headers, "Content-Type":"application/json"},
            json={"isRead": True}
        )
        print("DEBUG mark read status:", patch.status_code)
        patch.raise_for_status()
    except requests.HTTPError as e:
        print(f"[WARN] Não foi possível marcar como lida (status {patch.status_code}): {e}")

def main_loop():
    while True:
        try:
            token = get_token()
            msgs  = fetch_messages(token)
            for m in msgs:
                save_attachments(token, m)
        except Exception as e:
            print(f"[ERROR] Loop principal: {e}")
        time.sleep(INTERVAL)

if __name__=="__main__":
    main_loop()