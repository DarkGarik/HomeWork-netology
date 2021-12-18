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
services:
- drive.google.com: 74.125.131.194
  google.com: 173.194.220.113
  mail.google.com: 173.194.73.18

```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

---

### Как сдавать задания

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
