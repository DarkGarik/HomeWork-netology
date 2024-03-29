1. В Linux список сетевых интерфейсов можно посмотреть , например, командой `ip -c -br l`  
```bash
~$ ip -c -br l
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
ens3             UP             02:00:17:00:22:c5 <BROADCAST,MULTICAST,UP,LOWER_UP>

```
В Windows есть утилита `ipconfig`:  
```
C:\Users\Sergey>ipconfig

Настройка протокола IP для Windows


Адаптер Ethernet VirtualBox Host-Only Network:

   DNS-суффикс подключения . . . . . :
   Локальный IPv6-адрес канала . . . : fe80::f588:7ff3:7d93:1d6a%6
   IPv4-адрес. . . . . . . . . . . . : 192.168.56.1
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз. . . . . . . . . :

Адаптер беспроводной локальной сети Подключение по локальной сети* 1:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер беспроводной локальной сети Подключение по локальной сети* 10:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер беспроводной локальной сети Беспроводная сеть:

   DNS-суффикс подключения . . . . . :
   Локальный IPv6-адрес канала . . . : fe80::4020:d609:2c70:f542%13
   IPv4-адрес. . . . . . . . . . . . : 192.168.1.94
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз. . . . . . . . . : 192.168.1.1

Адаптер Ethernet Сетевое подключение Bluetooth:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :
```  

2. LLDP – протокол для обмена информацией между соседними устройствами, позволяет определить к какому порту коммутатора подключен сервер. В Linux есть пакет `lldpd`, посмотреть соседей можно по команде `lldpctl`  
   
3. Для разделения L2 коммутатора на несколько виртуальных сетей используется технология `VLAN`. В Linux есть одноименный пакет `vlan`. На примере Debian подобных систем `vlan` можно настроить прописав в `/etc/network/interfaces` следующее:

```bash
auto eth0.1400
iface eth0.1400 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        vlan_raw_device eth0
```
где `1400` это `vlan id`, а `vlan_raw_device eth0` указывает на каком сетевом интерфейсе должен создаться `vlan` интерфейс.  

4. Агрегация портов называется `LAG`. В Linux это делается при помощи модуля `bonding` и утилиты `ifenslave`: `apt install ifenslave`, `modprobe bonding`

Например в Dedian подобных системах в `/etc/network/interfaces`:
```
auto bond0

iface bond0 inet static
    address 10.31.1.5
    netmask 255.255.255.0
    network 10.31.1.0
    gateway 10.31.1.254
    bond-slaves eth0 eth1
    bond-mode active-backup
    bond-miimon 100
    bond-downdelay 200
    bond-updelay 200
```
  
5. В сети с маской `/29` 6(шесть) адресов:
```
~$ ipcalc 192.168.0.0/29
Address:   192.168.0.0          11000000.10101000.00000000.00000 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   192.168.0.0/29       11000000.10101000.00000000.00000 000
HostMin:   192.168.0.1          11000000.10101000.00000000.00000 001
HostMax:   192.168.0.6          11000000.10101000.00000000.00000 110
Broadcast: 192.168.0.7          11000000.10101000.00000000.00000 111
Hosts/Net: 6                     Class C, Private Internet
```  
32 подсети с маской `/29` можно получить из сети с маской `/24`:  
```bash
$ ipcalc 10.10.10.0/24 /29
...

Subnets after transition from /24 to /29

Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111

 1.
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
HostMin:   10.10.10.1           00001010.00001010.00001010.00000 001
HostMax:   10.10.10.6           00001010.00001010.00001010.00000 110
Broadcast: 10.10.10.7           00001010.00001010.00001010.00000 111
Hosts/Net: 6                     Class A, Private Internet

 2.
Network:   10.10.10.8/29        00001010.00001010.00001010.00001 000
HostMin:   10.10.10.9           00001010.00001010.00001010.00001 001
HostMax:   10.10.10.14          00001010.00001010.00001010.00001 110
Broadcast: 10.10.10.15          00001010.00001010.00001010.00001 111
Hosts/Net: 6                     Class A, Private Internet

 ...
 31.
Network:   10.10.10.240/29      00001010.00001010.00001010.11110 000
HostMin:   10.10.10.241         00001010.00001010.00001010.11110 001
HostMax:   10.10.10.246         00001010.00001010.00001010.11110 110
Broadcast: 10.10.10.247         00001010.00001010.00001010.11110 111
Hosts/Net: 6                     Class A, Private Internet

 32.
Network:   10.10.10.248/29      00001010.00001010.00001010.11111 000
HostMin:   10.10.10.249         00001010.00001010.00001010.11111 001
HostMax:   10.10.10.254         00001010.00001010.00001010.11111 110
Broadcast: 10.10.10.255         00001010.00001010.00001010.11111 111
Hosts/Net: 6                     Class A, Private Internet


Subnets:   32
Hosts:     192

```

6. В ситуации, когда частные подсети уже заняты, и надо организовать стык между 2-мя организациями, можно взять адреса из подсети `100.64.0.0/10` В соответствии с RFC6598, используется как транслируемый блок адресов для межпровайдерских взаимодействий.  
Например `100.64.0.0/26`:
```bash
$ ipcalc 100.64.0.0/26
Address:   100.64.0.0           01100100.01000000.00000000.00 000000
Netmask:   255.255.255.192 = 26 11111111.11111111.11111111.11 000000
Wildcard:  0.0.0.63             00000000.00000000.00000000.00 111111
=>
Network:   100.64.0.0/26        01100100.01000000.00000000.00 000000
HostMin:   100.64.0.1           01100100.01000000.00000000.00 000001
HostMax:   100.64.0.62          01100100.01000000.00000000.00 111110
Broadcast: 100.64.0.63          01100100.01000000.00000000.00 111111
Hosts/Net: 62                    Class A

```  

7. Проверить ARP таблицу в Linux и Windows можно командой `arp -a`.  
В Windows удалить запись можно с ключем `-d` подставив параметром IP адрес, если подставить `*`, то очистится вся таблица.  
В Linux полностью очистить таблицу с помощью утилиты `arp` сразу нельзя. Но можно выполнить `ip link set arp off dev eth0; ip link set arp on dev eth0`, что приведет к сбросу таблицы `arp` при перезапуске сетевого интерфейса.