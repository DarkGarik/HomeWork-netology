#!/usr/bin/env python3
import socket, time, json, os, yaml

def write_files(data):
    with open(os.getcwd()+"/04-script-03-yaml/services.json", "w") as write_j:
        json.dump(data, write_j, indent=2)
    with open(os.getcwd()+"/04-script-03-yaml/services.yaml", "w") as write_y:
        yaml.dump(data, write_y, indent=2)

domains = ("drive.google.com", "mail.google.com", "google.com")
resolv = dict.fromkeys(domains)

for domain in domains:
    ip = socket.gethostbyname(domain)
    resolv[domain] = ip

data = {"services":[resolv]}
write_files(data)

while True:
    for domain in domains:
        ip = socket.gethostbyname(domain)
        if ip == resolv[domain]:
            print(domain+" - "+ip)
        else:
            print("[ERROR] "+domain+" IP mismatch:"+resolv[domain]+" "+ip)
            print(domain+" - "+ip)
            resolv[domain] = ip
            write_files(data)
        time.sleep(1)
    