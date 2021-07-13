from fw_topo import Topology
from fw_app import Firewall, Run_Firewall
from fw_api import ControllerAPI
from mn_wifi.cli import CLI

if __name__ == '__main__':
	fw_topo = Topology()
        print("*** Features: ping / nodes / firewall / exit")
        while(1):
                x = raw_input("Select an option: ")
                if x == "ping":
                	fw_topo.try_ping()
                elif x == "nodes":
                        fw_topo.print_elements()
		elif x == 'firewall':
			bridge = fw_topo.choose_component("br")
			controller = fw_topo.choose_component("cont")
			Run_Firewall(bridge,controller)
		#Hidden Feature		
		elif x == "CLI":
                        CLI(fw_topo.net)
		#Hidden Feature
                elif x == 'api':
			bridge = fw_topo.choose_component("br")
			controller = fw_topo.choose_component("cont")
			api = ControllerAPI(controller,8181)
			openflow_id = fw_topo.get_bridge_id(str(bridge))
			flows = api.get_flows(openflow_id)
			print(flows)
                elif x == "exit":
                        print("*** Stopping Network.")
                        fw_topo.net.stop()
                        break
		else:
                        print("*** Wrong selection. Please check the available features.")

