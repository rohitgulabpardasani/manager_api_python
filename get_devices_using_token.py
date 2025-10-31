import requests
import urllib3
import json

# ============================================
# 🔧 STUDENT TODO SECTION — FILL THESE VALUES 🔧
# ============================================

# 1️⃣  vManage connection info
VMANAGE  = ""
TOKEN    = ""                 # e.g. "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 2️⃣  API endpoint for the resource you want to access
URL =           # Refer to the API docs to extract the Endpoint + Resource URL

# ============================================
# ⚙️ DO NOT MODIFY BELOW THIS LINE
# ============================================

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.verify = False

def ensure_json_or_die(r: requests.Response, label: str) -> dict:
    ct = r.headers.get("content-type", "")
    if not r.ok:
        print(f"❌ {label} failed: HTTP {r.status_code}")
        print("Content-Type:", ct)
        print(r.text[:400])
        raise SystemExit(1)
    if "json" not in ct.lower():
        print(f"❌ {label} is not JSON (Content-Type: {ct})")
        print("Body preview:")
        print(r.text[:400])
        raise SystemExit(1)
    try:
        return r.json()
    except Exception:
        print(f"❌ {label}: JSON parse error")
        print(r.text[:400])
        raise SystemExit(1)

def try_cookie_jsessionid() -> dict:
    # Treat TOKEN as JSESSIONID cookie
    session.cookies.clear()
    session.cookies.set("JSESSIONID", TOKEN)
    headers = {"Accept": "application/json"}
    r = session.get(URL, headers=headers, allow_redirects=False)
    if r.is_redirect:
        # Redirect to login means cookie not valid
        loc = r.headers.get("Location", "")
        print(f"❌ Cookie auth redirected to: {loc or '[no Location]'}")
        raise RuntimeError("cookie_redirect")
    return ensure_json_or_die(r, "Cookie auth request")

def try_x_auth_token() -> dict:
    session.cookies.clear()
    headers = {
        "X-Auth-Token": TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    r = session.get(URL, headers=headers, allow_redirects=False)
    if r.is_redirect:
        loc = r.headers.get("Location", "")
        print(f"❌ X-Auth-Token redirected to: {loc or '[no Location]'}")
        raise RuntimeError("xauth_redirect")
    return ensure_json_or_die(r, "X-Auth-Token request")

def try_bearer() -> dict:
    session.cookies.clear()
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    r = session.get(URL, headers=headers, allow_redirects=False)
    if r.is_redirect:
        loc = r.headers.get("Location", "")
        print(f"❌ Bearer redirected to: {loc or '[no Location]'}")
        raise RuntimeError("bearer_redirect")
    return ensure_json_or_die(r, "Bearer request")

def main():
    print("🔐 Trying JSESSIONID cookie auth...")
    try:
        payload = try_cookie_jsessionid()
        print("✅ Cookie auth worked.")
    except Exception:
        print("↪️  Falling back to X-Auth-Token header...")
        try:
            payload = try_x_auth_token()
            print("✅ X-Auth-Token worked.")
        except Exception:
            print("↪️  Falling back to Authorization: Bearer header...")
            payload = try_bearer()
            print("✅ Bearer worked.")

    devices = payload.get("data", [])
    if not isinstance(devices, list):
        print("ℹ️ Unexpected payload shape; printing raw JSON:")
        print(json.dumps(payload, indent=2))
        return

    print(f"{'TYPE':10} {'HOSTNAME':15} {'SYSTEM-IP':15} {'REACH':10} {'MODEL/PLATFORM'}")
    for d in devices:
        dev_type = d.get("device-type") or d.get("personality") or ""
        model = (
            d.get("deviceModel")
            or d.get("device-model")
            or d.get("platform")
            or d.get("model")
            or ""
        )
        print(
            f"{dev_type:10} {d.get('host-name',''):15} {d.get('system-ip',''):15} "
            f"{d.get('reachability',''):10} {model}"
        )

if __name__ == "__main__":
    main()

