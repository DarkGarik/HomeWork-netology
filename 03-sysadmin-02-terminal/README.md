1. Команда `cd` внутреняя, тоесть встроенная в оболочку. Для работы в командной строке должен быть минимальный набор комманд.  
2. `grep` с ключем `-c` даст тотже результат что и `grep <some_string> <some_file> | wc -l` :
```bash
vagrant@vagrant:~$ grep 2 test1 | wc -l
3
vagrant@vagrant:~$ grep -c 2 test1
3 
```
man grep
```bash
   General Output Control
       -c, --count
              Suppress normal output; instead print a count of matching lines for each input file.  With the  -v,  --invert-match  option  (see  below),
              count non-matching lines.
```
3. PID `1` у процесса `systemd`
```bash
vagrant@vagrant:~$ pstree -p
systemd(1)─┬─VBoxService(825)─┬─{VBoxService}(827)
           │                  ├─{VBoxService}(828) 
....
```
4. vagrant@vagrant:~$ `ls 123 2>/dev/pts/1` 
```bash
vagrant@vagrant:~$ tty
/dev/pts/0
vagrant@vagrant:~$ ls /dev/pts
0  1  ptmx
vagrant@vagrant:~$ ls 123 2>/dev/pts/1
```
5. Получится
```bash 
vagrant@vagrant:~$ ls
test  test1
vagrant@vagrant:~$ cat test1
123
321
vagrant@vagrant:~$ cat test1 > test2
vagrant@vagrant:~$ cat test2
123
321
```
6. Получится, например `top > /dev/pts/0`  
7. 
