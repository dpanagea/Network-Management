import ho_topo
from mn_wifi.cli import CLI

print("***Initiating Handover App.")
while(1):
	choice = raw_input("Should there be a gap between the AP's? (YES/NO) ")
	if choice == "YES" or choice == "NO":
		break
	else:
		print("Please try again. Available choices are YES or NO.")
topo = ho_topo.Topology(choice)
print("*** Features: video // CLI // exit\n")
while(1):
	option = raw_input("Make a selection: ")
	if option == "video":
		topo.stream()
	elif option == "CLI":
		CLI(topo.net)
	elif option == "exit":
		print("*** Stopping Network.")
		topo.net.stop()
		break
	else:
		print("Wrong Option.")
