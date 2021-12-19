# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```json
{ "info" : "Sample JSON output from our service\t",
    "elements" :[
        { "name" : "first",
        "type" : "server",
        "ip" : 7175 
        },
        { "name" : "second",
        "type" : "proxy",
        "ip : 71.78.22.43
        }
    ]
}
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

  ### Ответ:
```json
{ "info" : "Sample JSON output from our service\t",
    "elements" : [
        { "name" : "first",
        "type" : "server",
        "ip" : 7175 
        },
        { "name" : "second",
        "type" : "proxy",
        "ip" : "71.78.22.43"
        }
    ]
}
```
Не уверен на счет блока `"ip" : 7175 `, с одной стороны так тоже можно, но я для обнообразия заключил бы `7175` в ковычки.

2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
#!/usr/bin/env python3
import socket, time, json, os, yaml

def write_files(data):
    with open(os.getcwd()+"/04-script-03-yaml/services.json", "w") as write_j:
        json.dump(data, write_j, indent=2)
    with open(os.getcwd()+"/04-script-03-yaml/services.yaml", "w") as write_y:
        yaml.dump(data, write_y, indent=2, explicit_start=True, explicit_end=True)

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
    
```
### Содержимое файлов
`services.json`:
```
{
  "services": [
    {
      "drive.google.com": "74.125.131.194",
      "mail.google.com": "173.194.73.18",
      "google.com": "173.194.220.113"
    }
  ]
}
```
`services.yaml`:
```
---
services:
- drive.google.com: 74.125.131.194
  google.com: 173.194.220.113
  mail.google.com: 173.194.73.18
...

```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ответ:
Не нашёл рабочих кросплатформенных библиотек для определения типа файла. `mimetypes` в windows вообще смотрит только на расширение, что в нутри ему всё равно. `Python Magic` под Linux `json` определяет, а вот `yaml` не хочет. Поэтому написал простые проверки на соответствие синтаксиса сам.  
#### Скрипт:
```python
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

```

---

### Как сдавать задания

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
