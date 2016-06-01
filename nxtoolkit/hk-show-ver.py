import requests
import json
import sys

"""
Modify these please
"""
switch_IPs_file = sys.argv[1]




switchuser='admin'
switchpassword='cisco123'

myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1
    },
    "id": 1
  }
]
f = open(switch_IPs_file, 'r')
for IP in f:
  IP = IP.strip("\n")
  url='http://' + IP + '/ins'
  response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
  version = response['result']['body']['kickstart_ver_str']
  print "Switch %s: has version %s" %(IP, version)
