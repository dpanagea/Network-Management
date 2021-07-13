import json
import requests

class ControllerAPI:
	url = ''
	access = ()
	table = None

	def __init__(self,localhost,port,uname='admin',pword='admin',table=0):
        	self.url = "http://%s:%d/restconf" % (localhost, port)
        	self.access = (uname,pword)
		self.table = table

	def get_flows(self,bridge):
        	target_link = self.url + "/operational/opendaylight-inventory:nodes/node/%s/table/%d" % (bridge, self.table)
       		answer = requests.get(target_link,auth=self.access)
		#if flows received successfully
        	if answer.status_code == 200:
			json_object = json.loads(answer.text)
			flow_table = json.dumps(json_object,indent=1)
			return(flow_table)
		else:
        		print("*** Failed to get flows.")
			return(answer.status_code)
