import json, sys, os, yaml
in_file = sys.argv[1]

def check_yaml(in_file):
    with open(in_file, "r") as read_file:
        one_line = read_file.readlines()
        if one_line[0][:3] == "---" and one_line[-1] in ["...", "...\n"]:
            return True
        else:
            return False

def check_json(in_file):
    with open(in_file, "r") as read_file:
        one_line = read_file.readlines()
        if one_line[0][0] == "{" and one_line[-1][-2:] == "}\n":
            return True
        elif one_line[0][0] == "{" and one_line[-1][-1] == "}":
            return True
        else:
            return False

def conv_to_yaml(in_file):
    if len(in_file.split(".")) > 1 and in_file.split(".")[-1] == "json":
        out_file = in_file.split(".")
        out_file.pop()[-1]
        out_file = ".".join(out_file)+".yaml"
    else:
        print("Расширение файла не соответствует содержанию.\n\".yaml\" будет добавлено в конец имени файла без замены текущего раширения.")
        out_file = in_file+".yaml"
    with open(in_file, "r") as read_file:
        try:
            data = json.load(read_file)
        except Exception as err:
            print(err)
            exit()
    with open(out_file, "w") as write_file:
        yaml.dump(data, write_file, indent=2, explicit_start=True, explicit_end=True)
    return

def conv_to_json(in_file):
    if len(in_file.split(".")) > 1 and in_file.split(".")[-1] in ["yaml", "yml"]:
        out_file = in_file.split(".")
        out_file.pop()[-1]
        out_file = ".".join(out_file)+".json"
    else:
        print("Расширение файла не соответствует содержанию.\n\".json\" будет добавлено в конец имени файла без замены текущего раширения.")
        out_file = in_file+".json"
    with open(in_file, "r") as read_file:
        try:
            data = yaml.safe_load(read_file)
        except Exception as err:
            print(err)
            exit()           
    with open(out_file, "w") as write_file:
        json.dump(data, write_file, indent=2)
    return

if os.path.isfile(in_file) != True:
    print("Файл не найден")
elif check_json(in_file):
    conv_to_yaml(in_file)
elif check_yaml(in_file):
    conv_to_json(in_file)
else:
    print("Файл не соответствует формату json или yaml")
