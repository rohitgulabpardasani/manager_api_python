import requests
import urllib3
import json

# ============================================
# 🔧 STUDENT TODO SECTION — FILL THESE VALUES 🔧
# ============================================

# 1️⃣  vManage connection info
VMANAGE  = ""    		   
USERNAME = ""                      
PASSWORD = ""                      

# 2️⃣  Login and API endpoints
login_url =     # Define the j_security_check for authentication
data = {                                     # Define j_username and j_password keys
}
url =         # Refer to the API docs to extract the Endpoint + Resource URL

# ============================================
# ⚙️ DO NOT MODIFY BELOW THIS LINE
# ============================================

# Ignore certificate warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- STEP 1: LOGIN ---
session = requests.Session()
resp = session.post(login_url, data=data, verify=False)

if "JSESSIONID" not in session.cookies.get_dict():
    print("❌ Login failed! Check your credentials or vManage URL.")
    print(resp.text[:200])
    raise SystemExit(1)
else:
    print("✅ Login successful!")

# Handle XSRF token if required
xsrf = session.cookies.get("XSRF-TOKEN")
headers = {"X-XSRF-TOKEN": xsrf} if xsrf else {}

# --- STEP 2: GET ALL DEVICES ---
response = session.get(url, headers=headers, verify=False)

# Parse device list
devices = response.json().get("data", [])

# --- STEP 3: DISPLAY RESULTS ---
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

