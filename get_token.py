import requests
import urllib3
import json

# --------------------------

# ignore certificate warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://10.10.10.101:443/j_security_check"

payload = 'j_username=admin&j_password=C1sc0123!'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.cookies.get('JSESSIONID'))
