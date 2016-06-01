import requests
import json

"""
Modify these please
"""
url='http://10.114.217.157/ins'
switchuser='admin'
switchpassword='cisco123'

myheaders={'content-type':'application/json'}
payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": "config t ;vlan 999 ;name web",
    "output_format": "json"
  }
}
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
