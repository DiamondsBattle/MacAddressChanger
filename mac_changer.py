# PROG.DSB ++ PROG.DLB

import subprocess
import argparse as argp
import re


def getArguments():
	parser = argp.ArgumentParser()
	parser.add_argument('-i', '--interface', dest='interface', help='Interface to change it\'s MAC address')
	parser.add_argument('-m', '--mac', dest='new_mac', help='New MAC address')
	options = parser.parse_args()
	if not options.interface:
		parser.error('[-] Please specify an interface, use --help for more info.')
	elif not options.new_mac:
		parser.error('[-] Please specify a new MAC address, use --help for more info.')
	return options

def changeMac(interface, new_mac):
	print(f'[+] Changing MAC address for {interface} to {new_mac}')
	subprocess.call(['ifconfig', interface, 'down'])
	subprocess.call(['ifconfig' , interface, 'hw', 'ether', new_mac])	
	subprocess.call(['ifconfig', interface, 'up'])

def getCurrentMac(interface):
	ifconfig_result = subprocess.check_output(['ifconfig', interface])

	mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))
	try:
		return mac_address_search_result.group(0)
	except:
		print('[-] Could not read MAC address')


options = getArguments()

current_mac = getCurrentMac(options.interface)
print(f'[i] Current MAC : {current_mac}')

changeMac(options.interface, options.new_mac)

current_mac = getCurrentMac(options.interface)

if current_mac == options.new_mac:
	print(f'[+] MAC address was changed to {current_mac}.')
else:
	print('[-] MAC address wasn\'t changed.')