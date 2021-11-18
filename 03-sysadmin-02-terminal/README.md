1. Команда `cd` внутренняя, тоесть встроенная в оболочку bash. Не является отдельной программой.
```bash
vagrant@vagrant:~$ type cd
cd is a shell builtin 
```
2. `grep` с ключем `-c` даст тотже результат, что и `grep <some_string> <some_file> | wc -l` :
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
4. `ls 123 2>/dev/pts/1` 
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
7. Команда `bash 5>$1` перенаправит файловый дескриптор `5` в стандартный `stdout` `1`. Поэтому команда `echo netology > /proc/$$/fd/5` выведет на экран `netology`, т.к. файловый дескриптор `5` перенаправлен в стандартный поток вывода.
8. 
```bash
vagrant@vagrant:~$ bash 5>&2
vagrant@vagrant:~$ (la && ls 123)
.bash_history  .bashrc  .config   .local    .selected_editor  .sudo_as_admin_successful  .wget-hsts
.bash_logout   .cache   .lesshst  .profile  .ssh              .vbox_version
ls: cannot access '123': No such file or directory 
vagrant@vagrant:~$ (la && ls 123) 2>&1 >/proc/$$/fd/5 | cat > outfile
.bash_history  .bashrc  .config   .local   .profile          .ssh                       .vbox_version
.bash_logout   .cache   .lesshst  outfile  .selected_editor  .sudo_as_admin_successful  .wget-hsts
vagrant@vagrant:~$ cat outfile
ls: cannot access '123': No such file or directory
vagrant@vagrant:~$
```
9. `cat /proc/$$/environ` содержит переменную среду текущего сеанса. Похожий вывод будет у команд `env` или `printenv`
10. `/proc/<PID>/cmdline` хранит в себе командную строку процесса.  
`/proc/<PID>/exe` представляет собой символическую ссылку, , содержащую фактический путь к исполняемой команде.
11. `4.2` и `4a` от AMD
```bash
vagrant@vagrant:~$ cat /proc/cpuinfo | grep sse
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt rdtscp lm constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid tsc_known_freq pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm cmp_legacy cr8_legacy abm sse4a misalignsse 3dnowprefetch ssbd vmmcall fsgsbase avx2 rdseed clflushopt arat
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt rdtscp lm constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid tsc_known_freq pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm cmp_legacy cr8_legacy abm sse4a misalignsse 3dnowprefetch ssbd vmmcall fsgsbase avx2 rdseed clflushopt arat
```
12. При выполнении команды `ssh localhost 'tty'` - `tty` выполняется вне терминала, поэтому pty не выделяется. Чтобы это обойти можно использовать ключ `-t` у `ssh`  
```bash
vagrant@vagrant:~$ ssh -t localhost 'tty'
vagrant@localhost's password:
/dev/pts/2
Connection to localhost closed. 
```
13. 
```bash
vagrant@vagrant:~$ top
top - 19:06:15 up  8:09,  1 user,  load average: 0.07, 0.05, 0.01
Tasks: 106 total,   1 running, 105 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.4 us,  0.0 sy,  0.0 ni, 97.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :    981.0 total,    183.5 free,    113.6 used,    684.0 buff/cache
MiB Swap:    980.0 total,    978.2 free,      1.8 used.    701.9 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
      1 root      20   0  168660  12644   8320 S   0.0   1.3   0:18.81 systemd
      2 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kthreadd
      3 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_gp
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_par_gp
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker/0:0H-kblockd
      9 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 mm_percpu_wq
     10 root      20   0       0      0      0 S   0.0   0.0   0:00.45 ksoftirqd/0
     11 root      20   0       0      0      0 I   0.0   0.0   0:02.30 rcu_sched
     12 root      rt   0       0      0      0 S   0.0   0.0   0:00.38 migration/0
     13 root     -51   0       0      0      0 S   0.0   0.0   0:00.00 idle_inject/0
     14 root      20   0       0      0      0 S   0.0   0.0   0:00.00 cpuhp/0
     15 root      20   0       0      0      0 S   0.0   0.0   0:00.00 cpuhp/1
     16 root     -51   0       0      0      0 S   0.0   0.0   0:00.00 idle_inject/1
     17 root      rt   0       0      0      0 S   0.0   0.0   0:00.59 migration/1
     18 root      20   0       0      0      0 S   0.0   0.0   0:00.85 ksoftirqd/1
     20 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker/1:0H-kblockd
     21 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kdevtmpfs
     22 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 netns
     23 root      20   0       0      0      0 S   0.0   0.0   0:00.00 rcu_tasks_kthre
     24 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kauditd
     25 root      20   0       0      0      0 S   0.0   0.0   0:00.01 khungtaskd
     26 root      20   0       0      0      0 S   0.0   0.0   0:00.00 oom_reaper
     27 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 writeback
[1]+  Stopped                 top
vagrant@vagrant:~$ bg
[1]+ top &
vagrant@vagrant:~$ jobs -l
[1]+ 62077 Stopped (signal)        top
vagrant@vagrant:~$ disown top
-bash: warning: deleting stopped job 1 with process group 62077
vagrant@vagrant:~$ ps -a
    PID TTY          TIME CMD
  62077 pts/0    00:00:00 top
  62078 pts/0    00:00:00 ps
vagrant@vagrant:~$ screen -x
vagrant@vagrant:~$ reptyr 62077 
```
 14. Команда tee читает из стандартного ввода и записывает как в стандартный вывод, так и в один или несколько файлов одновременно.  
При конструкции `echo string | sudo tee /root/new_file` tree получит вывод команды echo, повысит права на sudo и запишет в файл.  
