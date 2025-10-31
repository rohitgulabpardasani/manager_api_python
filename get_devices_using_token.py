import requests
import urllib3
import json

# --------------------------

# ignore certificate warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://10.10.10.101:443/dataservice/device"

payload = {}
headers = {
  'Cookie': 'JSESSIONID=wt6Z_Au1JufSjne4bVjaS2EFW-EjuyOjfc7WjMQ9.cbc0e8eea0c9471767fb95437b6e7e576330cc7c1210d473ea27b9f1b5be095d'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(json.dumps(response.json(), indent=4, sort_keys=True))

