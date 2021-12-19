# import json, socket, time, os, yaml

# def write_files(data):
#     with open(os.getcwd()+"/04-script-03-yaml/services.json", "w") as write_j:
#         json.dump(data, write_j, indent=2)
#     with open(os.getcwd()+"/04-script-03-yaml/services.yaml", "w") as write_y:
#         yaml.dump(data, write_y, indent=2)

# domains = ("drive.google.com", "mail.google.com", "google.com")
# resolv = dict.fromkeys(domains)

# for domain in domains:
#     ip = socket.gethostbyname(domain)
#     resolv[domain] = ip

# data = {"services":[resolv]}
# write_files(data)
# str = "file.file.file.json".split(".")
# print(str)

# str.pop()[-1]
# print(str)
# str = ".".join(str)+".json"
# print(str)
# print(str.split(".")[-1])




import json, sys, os, mimetypes, yaml
in_file = sys.argv[1]
# print(in_file.split(".")[1])

# if in_file.split(".")[1] in ['yaml', 'yml']:
#     print("ok")
# else:
#     print("no ok")

def check_yaml(in_file):
    with open(in_file, "r") as read_file:
        one_line = read_file.readlines()
        print(one_line[-1])
        if one_line[0][:3] == "---" and one_line[-1] in ["...", "...\n"]:
            print("ok")
        else:
            print("no ok")

def check_json(in_file):
    with open(in_file, "r") as read_file:
        one_line = read_file.readlines()
        if one_line[0][0] == "{" and one_line[-1][-2:] == "}\n":
            print("ok")
        elif one_line[0][0] == "{" and one_line[-1][-1] == "}":
            print("ok")
        else:
            print("no ok")
    # if type[0] == "application/json":
    #     return True
    # else:
    #     return False
check_json(in_file)
# check_yaml(in_file)