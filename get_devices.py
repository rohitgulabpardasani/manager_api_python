# file: list_devices_with_model.py
import requests
import urllib3

# --- your vManage info ---
VMANAGE = "https://10.10.10.101"
USERNAME = "admin"
PASSWORD = "C1sc0123!"
# --------------------------

# ignore certificate warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. login
session = requests.Session()
login_url = f"{VMANAGE}/j_security_check"
data = {"j_username": USERNAME, "j_password": PASSWORD}
resp = session.post(login_url, data=data, verify=False)

if "JSESSIONID" not in resp.cookies:
    print("Login failed! Check credentials or URL.")
    exit()

# 2. get all devices
url = f"{VMANAGE}/dataservice/device"
devices = session.get(url, verify=False).json().get("data", [])

# 3. print results
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
    print(f"{dev_type:10} {d.get('host-name',''):15} {d.get('system-ip',''):15} "
          f"{d.get('reachability',''):10} {model}")

