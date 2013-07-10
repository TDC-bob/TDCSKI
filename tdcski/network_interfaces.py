# coding=utf-8
import subprocess
import re
from tdcski import config

re_ip = re.compile(".*Adresse IPv4.*: (?P<ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*")
re_mask = re.compile(".*Masque de sous.*: (?P<mask>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*")

def all_interfaces():
    call = subprocess.check_output("ipconfig /all", universal_newlines=True)
    interfaces = []
    interfaces.append("0.0.0.0")
    interfaces.append("127.0.0.1")
    # print(call)
    for c in call.split("\n"):
        i = re_ip.match(c)
        if i:
            interfaces.append(i.group("ip"))
    return interfaces

def all_interfaces_html():
    interfaces = all_interfaces()
    output = []
    for i in interfaces:
        if i == config.server.interface:
            output.append('<option selected="selected" value="{}">{}</option>'.format(i, i))
        else:
            output.append('<option value="{}">{}</option>'.format(i, i))
    return output

def main():
    print(all_interfaces())

if __name__ == "__main__":
    main()