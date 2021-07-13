from mn_wifi.net import Mininet_wifi
from mininet.link import TCLink
from mininet.node import RemoteController, OVSKernelSwitch
from mn_wifi.node import OVSKernelAP
from time import sleep

class Topology:
	net = None
	bridges = []
	clients = []
	odl = None

	def __init__(self):
		print("*** Creating Network.")
		self.net = Mininet_wifi(link=TCLink, accessPoint=OVSKernelAP, switch=OVSKernelSwitch)

		print("*** Creating Nodes.")
		sta1 = self.net.addStation('station1', mac='00:00:00:00:00:01', ip='10.0.0.1', position='20,20,0', range=2)
		sta2 = self.net.addStation('station2', mac='00:00:00:00:00:02', ip='10.0.0.2', position='80,20,0', range=2)
		sta3 = self.net.addStation('station3', mac='00:00:00:00:00:03', ip='10.0.0.3', position='20,40,0', range=2)
		sta4 = self.net.addStation('station4', mac='00:00:00:00:00:04', ip='10.0.0.4', position='80,40,0', range=2)
		self.clients.append(sta1)
		self.clients.append(sta2)
		self.clients.append(sta3)
		self.clients.append(sta4)
		h5 = self.net.addHost('host5',mac='00:00:00:00:00:05',ip='10.0.0.5')
		self.clients.append(h5)
		s1 = self.net.addSwitch('switch1')
		ap1 = self.net.addAccessPoint('ap1', ssid = "open_wifi-1", mode="g", channel = "1", position='30,30,0',range=20)
		ap2 = self.net.addAccessPoint('ap2', ssid = "open_wifi-2", mode="g", channel = "6", position='70,30,0',range=20)
		self.bridges.append(s1)
		self.bridges.append(ap1)
		self.bridges.append(ap2)
		self.odl = self.net.addController(name='ODL', controller=RemoteController, ip='192.168.1.3',port=6633)

		print("*** Configuring WiFi Nodes.")
		self.net.configureWifiNodes()

		print("*** Adding Links.")
		self.net.addLink(ap1,s1)
		self.net.addLink(ap2,s1)
		self.net.addLink(h5,s1)

		print("*** Starting Network.")
		self.net.build()
		self.odl.start()
		s1.start( [self.odl] )
		ap1.start( [self.odl] )
		ap2.start( [self.odl] )
		print("*** Network Initiated.")

	def get_ip(self,name):
                temp = str(name)
                this_ip = "10.0.0."+temp[-1]
                return this_ip

	def get_mac(self,name):
	        temp = str(name)
        	this_mac = "00:00:00:00:00:0"+temp[-1]
        	return this_mac

	def get_bridge_id(self,bridge):
        	if 'ap' in bridge:
                	index = bridge[2:]
	                id = 1152921504606846976
	        elif 'switch' in bridge:
	                index = bridge[6:]
	                id = 0
	        id = id + int(index)
	        bridge_id = "openflow:%s" % (str(id))
	        return(bridge_id)

	def try_ping(self):
		print("*** Checking network components' reachability.")
		sleep(3)
		for i in range(len(self.clients)-1):
			first = self.clients[i]
			for second in self.clients[i+1:]:
				outcome = first.cmd("ping -c 2 " + self.get_ip(second))
				if ", 0% packet loss" in outcome:
					print("%s -> %s : O" % (first,second))
				else:
					print("%s -> %s : X" % (first,second))

	def print_elements(self):
		print("*** Showing all network bridges:"),
		for i in self.bridges:
			print(i),
		print("\n*** Showing all network clients:"),
		for i in self.clients:
			print(i),
		print("\n*** Showing network controller:"),
		print(self.odl),
		print("with IP: "+self.odl.ip)
		adv = raw_input("*** Show client detailed information? (YES/NO) ")
		if adv == 'YES':
			for i in self.clients:
				print(str(i)+": "+self.get_ip(i)+", "+self.get_mac(i))

	def choose_component(self,choice):
		temp = []
		if choice == "br":
        		temp = self.bridges
        		print("Choose the bridge by typing one of the following option: ")
    		elif choice == "cl" :
        		temp = self.clients
        		print("Choose the clients by typing one of the following option: ")
		elif choice == "cont":
			return self.odl.ip
		else:
			print("Wrong Component Choice.")
			return
		index_len = len(temp)
		for seq in range(0,index_len):
			print(seq+1,str(temp[seq]))
		option = int(input())
		if option > index_len or option < 0:
			print("This choice does not exist, index is out of range!")
		else:
			return temp[option-1]

