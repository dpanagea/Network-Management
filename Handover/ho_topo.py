from mn_wifi.net import Mininet_wifi
from mininet.link import TCLink
from mininet.node import RemoteController, OVSKernelSwitch
from mn_wifi.node import OVSKernelAP

class Topology():
	net = None
	sta1 = None
	sta2 = None

	def __init__(self,gap):
       		print("Create a Network.")
        	self.net = Mininet_wifi(link=TCLink, accessPoint=OVSKernelAP, switch=OVSKernelSwitch)
		
		if gap == "YES":
			rng = 20
		else:
			rng = 33

		print("*** Creating nodes")
		self.sta1 = self.net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', position='25,70,0', range=5)
		self.sta2 = self.net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', position='120,50,0', range=5)
		h3 = self.net.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
		s1 = self.net.addSwitch('s1')
        	ap1 = self.net.addAccessPoint('ap1', ssid = "ssid_1", mode="g", channel = "1", position='25,60,0', range=rng)
		ap2 = self.net.addAccessPoint('ap2', ssid = "ssid_2", mode="g", channel = "6", position='75,60,0', range=rng)
		ap3 = self.net.addAccessPoint('ap3', ssid = "ssid_3", mode="g", channel = "2", position='130,60,0', range=rng)
        	c1 = self.net.addController('c1', controller=RemoteController, ip='192.168.1.3',port=6633)

		self.net.setPropagationModel(model="logDistance", exp=2)

		print("*** Configuring WiFi nodes")
        	self.net.configureWifiNodes()

        	print("*** Adding Links")
		self.net.addLink(ap1,s1)
		self.net.addLink(ap2,s1)
		self.net.addLink(ap3,s1)
		self.net.addLink(h3,s1)

		self.net.plotGraph(max_x=160, max_y=125)
	
		self.net.startMobility(time=0)
		self.net.mobility(self.sta1, 'start', time=30, position='25,70,0')
        	self.net.mobility(self.sta1, 'stop', time=37, position='115,70,0')
        	self.net.mobility(self.sta2, 'start', time=60, position='120,50,0')
        	self.net.mobility(self.sta2, 'stop', time=67, position='30,50,0')
        	self.net.stopMobility(time=80)
		
        	print("*** Starting Network")
        	self.net.build()
        	c1.start()
		s1.start ( [c1] )
        	ap1.start( [c1] )
		ap2.start( [c1] )
		ap3.start( [c1] )
	
	def stream(self):
		#sta1 is the streamer
		self.sta1.cmd('vlc-wrapper --sout "#rtp{dst=10.0.0.2,port=5004,mux=ts},dst=display" &')
		#sta2 is the receiver
		self.sta2.cmd('vlc-wrapper rtp://@10.0.0.2:5004 &')

