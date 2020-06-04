#!/usr/bin/env python

import subprocess
import optparse
import re


def get_args():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC")
    parse.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parse.parse_args()
    if not options.interface:
        parse.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parse.error("[-] Please specify a new MAC, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " from 08:00:27:27:95:ae to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not get MAC address")


options = get_args()

current_mac = get_current_mac(options.interface)
print("[+] Current MAC is = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address has successfully changed to "+current_mac)
else:
    print("[-] MAC address did not get changed.")
