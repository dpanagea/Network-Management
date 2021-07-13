import pandas as pd

def flows_dict(path):
	protocol = []
	tp_src = []
	tp_dst = []
	dl_src = []
	dl_dst = []
	actions = []
	
	protocols = ["tcp", "udp","icmp","arp"]
	l = path.split('\n')
	for x in l:
		x = x.replace(', ', ',')
		x = x.replace(' ', ',')
		x = x.replace('\r','')
		if "cookie=0x0" in x:
			flag = 0
			for p in protocols:
				if p in x:
					protocol.append(p)
					flag = 1
					break
				else:
					continue
			if flag == 0:
				protocol.append("NO")
			try:
				y = x.split("tp_src=", 1)[1].split("," , 1)[0]
			except:
				y = "NO"
			tp_src.append(y)
			try:
				y = x.split("tp_dst=", 1)[1].split("," , 1)[0]
			except:
				y = "NO"
			tp_dst.append(y)
			try:
				y = x.split("dl_src=", 1)[1].split(",", 1)[0]
			except:
				y = "NO"
			dl_src.append(y)
			try:
				y = x.split("dl_dst=", 1)[1].split(",", 1)[0]
			except:
				y = "NO"
			dl_dst.append(y)
			try:
				y = x.split("actions=", 1)[1].split("\n" , 1)[0]
			except:
				y = "NO"
			actions.append(y)
		
	table = {"PROTOCOL": protocol,
		"TP_SRC": tp_src,
		"TP_DST": tp_dst,
		"DL_SRC": dl_src,
		"DL_DST":dl_dst,
		"ACTIONS": actions}  
	return (table)


class Rule:
	info = ''

	def __init__(self):
		self.info = "ovs-ofctl add-flow *br '*prot,tp_src=*port1,tp_dst=*port2,dl_src=*src,dl_dst=*dst,actions=*act'"

	def general_update(self,br,act,prot='NO',port1='NO',port2='NO',src='NO',dst='NO'):
		self.info = self.info.replace('*br',str(br))

		if prot == 'NO':
			self.info = self.info.replace('*prot,','')
		else:
			self.info = self.info.replace('*prot',prot)

                if port1 == 'NO':
                        self.info = self.info.replace('tp_src=*port1,','')
                else:
                        self.info = self.info.replace('*port1',port1)

                if port2 == 'NO':
                        self.info = self.info.replace('tp_dst=*port2,','')
                else:
                        self.info = self.info.replace('*port2',port2)

		if src == 'NO':
			self.info = self.info.replace('dl_src=*src,','')
		else:
			self.info = self.info.replace('*src',src)

		if dst == 'NO':
			self.info = self.info.replace('dl_dst=*dst,','')
		else:
			self.info = self.info.replace('*dst',dst)

		if act == 'block':
			self.info = self.info.replace('*act','drop')
		elif act == 'allow':
			self.info = self.info.replace('*act','normal')


class Firewall:
	table = {}
	rule_counter = 0
	controller = None
	bridge = None

	def __init__(self,br,contr):
		self.bridge = br
		self.controller = contr
		print("(^) Firewall is now ONLINE.\n(^) Type help for available commands or exit to access previous menu.")

	def get_table(self):
		result = self.bridge.cmd("ovs-ofctl dump-flows %s" % self.bridge)	
		self.table = flows_dict(result)

	def print_table(self):
		if self.rule_counter == 0:
			print("(^) There are no entries/rules in the table.")
		else:
			print(pd.DataFrame(self.table))

	def dupl_check(self,act,prot="NO",port1="NO",port2="NO",src="NO",dst="NO"):
		if act == "block":
			act = "drop"
		elif act == "allow":
			act = "normal"
		if bool(self.table.get('PROTOCOL')):		
			tbl = self.table
			for i in range(self.rule_counter):
				if tbl["PROTOCOL"][i] == prot and tbl["ACTIONS"][i] == act:
					if tbl["TP_SRC"][i] == port1 and tbl["TP_DST"][i] == port2 and tbl["DL_SRC"][i] == src and tbl["DL_DST"][i] == dst:
						print("(^) Found duplicate! Cannot add rule twice.")
						return -1
	
	def apply_rule(self,rule):
		self.rule_counter = self.rule_counter + 1
		self.bridge.cmd(rule)

	#In the following 2 methods a rule for the Firewall is created. Before applying it, there is a duplicate check.

	def create_basic(self):
		r = Rule()
		print("1.Block incoming ping requests.\n2.Block UDP traffic.\n3.Block incoming TCP traffic on port 80 from any IP address.")
		x = raw_input("Select an option: ")
		if x == '1':
			r.general_update(self.bridge,"block",prot='icmp')
			check = self.dupl_check("block",prot='icmp')
		elif x == '2':
			r.general_update(self.bridge,"block",prot='udp')
			check = self.dupl_check("block",prot='udp')
		elif x == '3':
			r.general_update(self.bridge,"block",prot='tcp',port2='80')
			check = self.dupl_check("block",prot='tcp',port2='80')
		else:
			print("(^) Wrong choice.")
		if check != -1:
			self.apply_rule(r.info)

	def create_custom(self):
		r = Rule()
		print("(^) Make your custom rule selections. If irrelevant field input NO.")
                act = raw_input("(^) Desired Action: (block/allow) ")
		prot = raw_input("(^) Protocol Name: (arp,icmp,tcp,udp) ")
		port1 = raw_input("(^) Source Port: ")
		port2 = raw_input("(^) Destination Port: ")
		src = raw_input("(^) Source Client: ")
		dst = raw_input("(^) Select Destination: ")
		check = self.dupl_check(act,prot=prot,port1=port1,port2=port2,src=src,dst=dst)
		if check != -1:
			r.general_update(self.bridge,act,prot=prot,port1=port1,port2=port2,src=src,dst=dst)
			self.apply_rule(r.info)

def Run_Firewall(bridge,controller):
	fw = Firewall(bridge,controller)
	while(1):
		x = raw_input("(^) Insert Command: ")
		if x == 'SR':
			fw.get_table()
			fw.print_table()
		elif x == 'CBR':
			rule = fw.create_basic()
		elif x == 'CCR':
			rule = fw.create_custom()
		elif x == 'exit':
			break
		elif x == 'help':
			print("(^) Commands:\nSR = Show Rules.\nCBR = Create Basic Rule.\nCCR = Create Custom Rule.")
		else:
			print("(^) Invalid Input.")
