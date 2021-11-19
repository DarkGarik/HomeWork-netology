1. `chdir("/tmp")`  
2. `file` берет информацию из файла `/etc/magic`  
```bash
vagrant@vagrant:~$ strace file /dev/sda
...
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
...
```
3. 1
4. Зомби не занимают памяти (как процессы-сироты), но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.
5. 
```bash
vagrant@vagrant:~$ sudo opensnoop-bpfcc
PID    COMM               FD ERR PATH
609    irqbalance          6   0 /proc/interrupts
609    irqbalance          6   0 /proc/stat
609    irqbalance          6   0 /proc/irq/20/smp_affinity
609    irqbalance          6   0 /proc/irq/0/smp_affinity
609    irqbalance          6   0 /proc/irq/1/smp_affinity
609    irqbalance          6   0 /proc/irq/8/smp_affinity
609    irqbalance          6   0 /proc/irq/12/smp_affinity
609    irqbalance          6   0 /proc/irq/14/smp_affinity
609    irqbalance          6   0 /proc/irq/15/smp_affinity
609    irqbalance          6   0 /proc/interrupts
609    irqbalance          6   0 /proc/stat 
```
6. 1
7. `&&` логический оператор, `;`это простая последовательность. Т.е. при `&&` следующая команда выполнится, только после успешного выполнения предыдущей. При `;` все команды будут выполнены последовательно, независимо от результата выполнения предыдущей.  
Если применить `set -e` в bash при использовании `&&` ничего не изменится, т.к. ключ `-e` означает немедленный выход, если конвейер, список или составная команда завершается с ненулевым статусом, что означает то же поведение, что и при обычном использовании `&&`  
```bash
       set [--abefhkmnptuvxBCEHPT] [-o option-name] [arg ...]
       set [+abefhkmnptuvxBCEHPT] [+o option-name] [arg ...]
              Without options, the name and value of each shell variable are displayed in a format that can be reused as input for setting or  resetting
              the  currently-set variables.  Read-only variables cannot be reset.  In posix mode, only shell variables are listed.  The output is sorted
              according to the current locale.  When options are specified, they set or unset shell attributes.  Any arguments  remaining  after  option
              processing  are  treated  as  values for the positional parameters and are assigned, in order, to $1, $2, ...  $n.  Options, if specified,
              have the following meanings:
...
              -e      Exit immediately if a pipeline (which may consist of a single simple command), a list, or a compound command  (see  SHELL  GRAMMAR
                      above),  exits  with a non-zero status.  The shell does not exit if the command that fails is part of the command list immediately
                      following a while or until keyword, part of the test following the if or elif reserved words, part of any command executed in a &&
                      or  ||  list  except  the command following the final && or ||, any command in a pipeline but the last, or if the command's return
                      value is being inverted with !.  If a compound command other than a subshell returns a non-zero status because  a  command  failed
                      while  -e was being ignored, the shell does not exit.  A trap on ERR, if set, is executed before the shell exits.  This option ap‐
                      plies to the shell environment and each subshell environment separately (see COMMAND EXECUTION ENVIRONMENT above), and  may  cause
                      subshells to exit before executing all the commands in the subshell.

                      If  a compound command or shell function executes in a context where -e is being ignored, none of the commands executed within the
                      compound command or function body will be affected by the -e setting, even if -e is set and a command returns  a  failure  status.
                      If  a  compound command or shell function sets -e while executing in a context where -e is ignored, that setting will not have any
                      effect until the compound command or the command containing the function call completes. 
```
8. `set -euxo pipefail` содержит опции: `-e немедленный выход если не 0`, `-u    При раскрытии параметров рассматривать неустановленные переменные и параметры, отличные от специальных параметров «@» и «*», как ошибку.`, `-x      После раскрытия каждой простой команды для команды, команды регистра, команды выбора или арифметики команды отобразите развернутое значение PS4, за которым следует команда и ее расширенные аргументы или связанный список слов.` и опцию `-o pipefail Если установлено, возвращаемое значение конвейера - это значение последней (самой правой) команды для выхода с ненулевым статусом или ноль, если все команды в конвейере завершаются успешно. По умолчанию эта опция отключена.`  
В сценариях такой набор опций хорошо использовать для проверки, что точно выполняется все команды, и отлавливания ошибок внутри команд соединенных `;`
9. Наиболее часто встречаемый статутс у процессов в системе `S`
```bash
vagrant@vagrant:~$ ps -o stat ax | sort | cut -c 1-1 | uniq -c
     50 I
      1 R
     57 S. 
```

