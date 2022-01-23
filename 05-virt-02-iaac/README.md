
# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"


---

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.
- Какой из принципов IaaC является основополагающим?

### Ответ:
- Основные паттерны IaaC, это CI/CD, тоесть неприрывная интеграция и непрерывная доставка. Основне преимущества уже следуют из их названий. Более частый выпус изменений позволяет выявить ошибки и откатиться при необходимости.
- Основополагающим принципом IaaC является `идемпотентность`, тоесть каждый раз мы получаем один и тотже результат.

## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?
- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

### Ответ:
- Основное отличие Ansible от подобных систем в том, что Ansible использует существующую SSH инфраструктуру и не требует установки агента/клиента на целевые системы.
- Я думаю что оба метода имеют свои приимущества и не достатки. Возможно push более надежен, т.к. управление идет с управляющего сервера и для него не нужно использования отдельного агента на целевом хосте.

## Задача 3

Установить на личный компьютер:

- VirtualBox
- Vagrant
- Ansible

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*

### Ответ:

- VirtualBox установлен на Windows 11
```
Графический интерфейс VirtualBox
Версия 6.1.30 r148432 (Qt5.6.2)
```
- Vagrant на Windows 11
``` PS
PS C:\Users\Sergey> vagrant --version
Vagrant 2.2.19
```
- Ansible в Windows 11 под Cygwin
``` bash
$ ansible --version
ansible 2.8.4
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/Sergey/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.7.12 (default, Nov 23 2021, 18:58:07) [GCC 11.2.0]

```

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.
- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
```
docker ps
```

### Ответ:

Прямо досканально воспроизвести лекцию не удалось, т.к. у меня окружение на Windows и завести полностью автоматическую связку VirtualBox, vagrant, ansible не получилось.
Но тем не менее, виртуальная машина создана с помощью vagrant на virtualbox, а плейбук ansible уже запущен отдельно через cygwin командой `ansible-playbook provision.yml`, и конечный результат в виде установленного докера получен:
``` bash
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

```


``` bash
$ ansible-playbook provision.yml
 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/connection/httpapi.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/connection/psrp.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/connection/vmware_tools.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/connection/winrm.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/foreman.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/grafana_annotations.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/hipchat.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/nrdp.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/slack.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/splunk.py) as it seems to be invalid: You need either charset_normalizer or chardet installed

 [WARNING]: Skipping plugin (/usr/lib/python3.7/site-packages/ansible/plugins/callback/sumologic.py) as it seems to be invalid: You need either charset_normalizer or chardet installed


PLAY [nodes] *****************************************************************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *****************************************************************************************************************************************************************************
changed: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] **************************************************************************************************************************************************************
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [server1.netology]: FAILED! => {"changed": false, "msg": "Could not find or access '~/.ssh/id_rsa.pub' on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}
...ignoring

TASK [Checking DNS] **********************************************************************************************************************************************************************************************
changed: [server1.netology]

TASK [Installing tools] ******************************************************************************************************************************************************************************************
[DEPRECATION WARNING]: Invoking "apt" only once while using a loop via squash_actions is deprecated. Instead of using a loop to supply multiple items and specifying `package: "{{ item }}"`, please use
`package: ['git', 'curl']` and remove the loop. This feature will be removed in version 2.11. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [server1.netology] => (item=['git', 'curl'])
 [WARNING]: Could not find aptitude. Using apt-get instead


TASK [Installing docker] *****************************************************************************************************************************************************************************************
 [WARNING]: Consider using the get_url or uri module rather than running 'curl'.  If you need to use command because get_url or uri is insufficient you can add 'warn: false' to this command task or set
'command_warnings=False' in ansible.cfg to get rid of this message.

changed: [server1.netology]

TASK [Add the current user to docker group] **********************************************************************************************************************************************************************
changed: [server1.netology]

PLAY RECAP *******************************************************************************************************************************************************************************************************
server1.netology           : ok=7    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=1


Sergey@DESKTOP-78B89KM /cygdrive/c/Users/Sergey/Desktop/Education/DevOps/HomeWork/HomeWork-netology/05-virt-02-iaac/vagrant
$
```