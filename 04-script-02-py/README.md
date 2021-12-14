### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-02-py/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | ???  |
| Как получить для переменной `c` значение 12?  | ???  |
| Как получить для переменной `c` значение 3?  | ???  |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
path = "~/netology/sysadm-homeworks/"
bash_command = ["cd "+path, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', path)
        print(prepare_result)
        # break
```

### Вывод скрипта при запуске при тестировании:
```
gorkov@gorkov-me:~/netology/sysadm-homeworks$ ./1.py
~/netology/sysadm-homeworks/1.py
~/netology/sysadm-homeworks/new_folder/new_file
~/netology/sysadm-homeworks/test
~/netology/sysadm-homeworks/test1
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3
import sys, subprocess
path = sys.argv[1]
bash_command = ["cd "+path, "git status"]
result_os = subprocess.Popen(' && '.join(bash_command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
(output, error) = result_os.communicate()
is_change = False
outstr = output.decode('utf-8')
for result in outstr.split('\n'):
    if result.find('fatal') != -1:
        print('"'+path+'" не является локальным репозиторием')
    elif result.find('can\'t cd') != -1:
        print('Путь "'+path+'" не существует.')
    elif result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', path)
        print(prepare_result)
```

### Вывод скрипта при запуске при тестировании:
```
gorkov@gorkov-me:~/netology/sysadm-homeworks$ ./2.py ~/netology/sysadm-homeworks/
/home/gorkov/netology/sysadm-homeworks/1.py
/home/gorkov/netology/sysadm-homeworks/new_folder/new_file
/home/gorkov/netology/sysadm-homeworks/test
/home/gorkov/netology/sysadm-homeworks/test1
gorkov@gorkov-me:~/netology/sysadm-homeworks$ ./2.py ~/netology/
"/home/gorkov/netology/" не является локальным репозиторием
gorkov@gorkov-me:~/netology/sysadm-homeworks$ ./2.py ~/netology/sysadm
Путь "/home/gorkov/netology/sysadm" не существует.
gorkov@gorkov-me:~/netology/sysadm-homeworks$ ./2.py ~/HomeWork-netology/
/home/gorkov/HomeWork-netology/README.md
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3
import socket, time

domains = ("drive.google.com", "mail.google.com", "google.com")
resolv = dict.fromkeys(domains)

for domain in domains:
    ip = socket.gethostbyname(domain)
    resolv[domain] = ip

while 1==1:
    for domain in domains:
        ip = socket.gethostbyname(domain)
        if ip == resolv[domain]:
            print(domain+" - "+ip)
        else:
            print("[ERROR] "+domain+" IP mismatch:"+resolv[domain]+" "+ip)
            print(domain+" - "+ip)
            resolv[domain] = ip
        time.sleep(1)
    
```

### Вывод скрипта при запуске при тестировании:
```
gorkov@gorkov-me:~/netology/sysadm-homeworks$ ./3.py
drive.google.com - 142.251.39.110
mail.google.com - 142.250.179.133
google.com - 142.251.39.110
drive.google.com - 142.251.39.110
mail.google.com - 142.250.179.133
google.com - 142.251.39.110
drive.google.com - 142.251.39.110
mail.google.com - 142.250.179.133
[ERROR] google.com IP mismatch:142.251.39.110 8.8.8.8
google.com - 8.8.8.8
drive.google.com - 142.251.39.110
mail.google.com - 142.250.179.133
google.com - 8.8.8.8
drive.google.com - 142.251.39.110
mail.google.com - 142.250.179.133
google.com - 8.8.8.8
drive.google.com - 142.251.39.110
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```