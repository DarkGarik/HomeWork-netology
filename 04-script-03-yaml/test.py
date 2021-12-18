import json, socket, time, os, yaml

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
