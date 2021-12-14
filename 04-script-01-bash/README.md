1. Переменные `a` и `b` мы объявили не явно числами `1` и `2` соответственно.  
Переменная `c` просто выведет строку `a+b`.  
В переменной `d` мы также получаем строку, но свормированную из двух переменных `$a` и `$b`.  
В переменной `e` мы уже используем конструкцию `$(( ))` которая позволяет нам произвести стандартную опрецию с целыми числами, которые мы как раз получим из переменных `$a` и `$b`, тоесть соответственно получим сумму чисел `1` и `2`.  
```bash
gorkov@gorkov-me:~$ cat test 
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))

echo -e "$a\n$b\n$c\n$d\n$e"
gorkov@gorkov-me:~$ bash test 
1
2
a+b
1+2
3
gorkov@gorkov-me:~$ 
```
  
2. В скрипте пропущена одна закрывающая скобка в цикле `while` и надо было добавить в условие `if` команду выхода из цикла.  
```bash
#!/usr/bin/env bash

while ((1==1))
do
    curl https://localhost:4757
    if (($? != 0))
    then
        date >> curl.log
        else
        break
    fi
done
```
  
3. Скрипт доступности IP:  
```bash
#!/usr/bin/env bash
count=(1 2 3 4 5)
ip_all=(192.168.0.1 173.194.222.113 87.250.250.242)
for ip in ${ip_all[@]}
do
    for i in ${count[@]}
    do
        curl --output /dev/null --silent --connect-timeout 3 http://$ip
        if (("$?" != "0"))
        then
            out="Service $ip not response"
            else
            out="Service $ip ok"
        fi
        echo `date` $out >> test.log
    done
done
```
  
4. Доработанный скрипт
```bash
#!/usr/bin/env bash
count=(1 2 3 4 5)
ip_all=(192.168.0.1 173.194.222.113 87.250.250.242)
for ip in ${ip_all[@]}
do
    for i in ${count[@]}
    do
        curl --output /dev/null --silent --connect-timeout 3 http://$ip
        if (("$?" != "0"))
        then
            echo $ip >> error
            exit
            else
            out="Service $ip ok"
        fi
        echo `date` $out >> test.log
    done
done
```