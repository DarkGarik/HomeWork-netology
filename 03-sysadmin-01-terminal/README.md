# Решение
5. Оперативная память: 1024 МБ  
Процессоры: 2
Жесткий диск: 64 ГБ
6. Добавить памяти и процессоров можно следующими параметрами:
```bash
config.vm.provider "virtualbox" do |v|
	v.memory = "2048"
	v.cpus = "4"
end
```
например в нашем случае:
```bash
 Vagrant.configure("2") do |config|
 	config.vm.box = "bento/ubuntu-20.04"
		config.vm.provider "virtualbox" do |v|
			v.memory = "2048"
			v.cpus = "4"
		end
 end
```
8. * длина журнала history задается переменной `HISTSIZE` в строке `862`
```bash
    862        HISTSIZE
    863               The number of commands to remember in the command history (see HISTORY below).  If the value is 0, com‐
    864               mands  are  not saved in the history list.  Numeric values less than zero result in every command being
    865               saved on the history list (there is no limit).  The shell sets the default value to 500  after  reading
    866               any startup files. 
```
* `ignoreboth` в bash это значение параметра `HISTCONTROL` которое означет не запоминать команды начинающиеся с пробелов и повторяющиеся подряд команды:
```bash
833        HISTCONTROL
    834               A  colon-separated  list of values controlling how commands are saved on the history list.  If the list
    835               of values includes ignorespace, lines which begin with a space character are not saved in  the  history
    836               list.  A value of ignoredups causes lines matching the previous history entry to not be saved.  A value
    837               of ignoreboth is shorthand for ignorespace and ignoredups.  A value of erasedups  causes  all  previous 
```
9. В `man bash` пишем конструкцию `-N` чтобы отобразить номера строк. Далее ищем фигурные скобки `/\{` предварительно заэкранировав их.
Первым в поиске выпадают зарезервированные слова, где также указывается цикл `while { }`:
```bash
    174 RESERVED WORDS
    175        Reserved  words are words that have a special meaning to the shell.  The following words are recognized as re‐
    176        served when unquoted and either the first word of a simple command (see SHELL GRAMMAR below) or the third word
    177        of a case or for command:
    178
    179        ! case  coproc  do done elif else esac fi for function if in select then until while { } time [[ ]] 
```
Далее мы видим что фигурные скобки используються для списка:
```bash
    230        { list; }
    231               list  is simply executed in the current shell environment.  list must be terminated with a newline or semicolon.  This is known as a group
    232               command.  The return status is the exit status of list.  Note that unlike the metacharacters ( and ), { and } are reserved words and must
    233               occur  where  a  reserved  word  is permitted to be recognized.  Since they do not cause a word break, they must be separated from list by
    234               whitespace or another shell metacharacter.
```
Я думаю это и есть ответ на данный вопрос.  

10. С помощью списка можно передать в команду `touch` список имен файлов в такой конструкции `{1..10000}` в итоге командой `touch {1..10000}` создастся 10000 файлов с именами от 1 до 10000
При попытки создать 300000 файлов выходит ошибка что слишком много аргументов для команды `touch`
```bash
vagrant@vagrant:~/test$ touch {1..300000}
-bash: /usr/bin/touch: Argument list too long 
```
11. В двойных квадратных скобках выражение возвращяет 1 или 0 в зависимости от условий 
```bash
       [[ expression ]]
              Return a status of 0 or 1 depending on the evaluation of the conditional expression expression.  Expressions are composed of the primaries
              described below under CONDITIONAL EXPRESSIONS.  Word splitting and pathname expansion are not performed on the words between  the  [[  and
              ]]; tilde expansion, parameter and variable expansion, arithmetic expansion, command substitution, process substitution, and quote removal
              are performed.  Conditional operators such as -f must be unquoted to be recognized as primaries.

              When used with [[, the < and > operators sort lexicographically using the current locale.
```
конструкция `[[ -d /tmp ]]` возвращяет 1, т.к. тут происходит проверка на то, есть ли директория `/tmp`
```bash
vagrant@vagrant:~$ if [[ -d /tmp ]]; then echo '1'; else echo '0'; fi
1
vagrant@vagrant:~$ if [[ -d /tmp1 ]]; then echo '1'; else echo '0'; fi
0
```
12. 
```bash
vagrant@vagrant:~$ mkdir /tmp/new_path_directory
vagrant@vagrant:~$ cp /bin/bash /tmp/new_path_directory/
vagrant@vagrant:~$ PATH=/tmp/new_path_directory/:$PATH
vagrant@vagrant:~$ type -a bash
bash is /tmp/new_path_directory/bash
bash is /bin/bash
bash is /usr/bin/bash
```
13. `man at`:
```bash
 NAME
       at, batch, atq, atrm - queue, examine, or delete jobs for later execution
....
DESCRIPTION
       at and batch read commands from standard input or a specified file which are to be executed at a later time, using /bin/sh.

       at      executes commands at a specified time.
....
       batch   executes commands when system load levels permit; in other words, when the load average drops below 1.5, or the value  specified  in  the
               invocation of atd.
```
at - запускает команды в заданное время.  
batch - запускает команды, когда уровни загрузки системы позволяют это делать. т.е. когда средняя нагрузка падает ниже 1,5 или значения, указанного при вызове atd.


# Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"

1. Установите средство виртуализации [Oracle VirtualBox](https://www.virtualbox.org/).

1. Установите средство автоматизации [Hashicorp Vagrant](https://www.vagrantup.com/).

1. В вашем основном окружении подготовьте удобный для дальнейшей работы терминал. Можно предложить:

	* iTerm2 в Mac OS X
	* Windows Terminal в Windows
	* выбрать цветовую схему, размер окна, шрифтов и т.д.
	* почитать о кастомизации PS1/применить при желании.

	Несколько популярных проблем:
	* Добавьте Vagrant в правила исключения перехватывающих трафик для анализа антивирусов, таких как Kaspersky, если у вас возникают связанные с SSL/TLS ошибки,
	* MobaXterm может конфликтовать с Vagrant в Windows,
	* Vagrant плохо работает с директориями с кириллицей (может быть вашей домашней директорией), тогда можно либо изменить [VAGRANT_HOME](https://www.vagrantup.com/docs/other/environmental-variables#vagrant_home), либо создать в системе профиль пользователя с английским именем,
	* VirtualBox конфликтует с Windows Hyper-V и его необходимо [отключить](https://www.vagrantup.com/docs/installation#windows-virtualbox-and-hyper-v),
	* [WSL2](https://docs.microsoft.com/ru-ru/windows/wsl/wsl2-faq#does-wsl-2-use-hyper-v-will-it-be-available-on-windows-10-home) использует Hyper-V, поэтому с ним VirtualBox также несовместим,
	* аппаратная виртуализация (Intel VT-x, AMD-V) должна быть активна в BIOS,
	* в Linux при установке [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads) может дополнительно потребоваться пакет `linux-headers-generic` (debian-based) / `kernel-devel` (rhel-based).

1. С помощью базового файла конфигурации запустите Ubuntu 20.04 в VirtualBox посредством Vagrant:

	* Создайте директорию, в которой будут храниться конфигурационные файлы Vagrant. В ней выполните `vagrant init`. Замените содержимое Vagrantfile по умолчанию следующим:

		```bash
		Vagrant.configure("2") do |config|
			config.vm.box = "bento/ubuntu-20.04"
		end
		```

	* Выполнение в этой директории `vagrant up` установит провайдер VirtualBox для Vagrant, скачает необходимый образ и запустит виртуальную машину.

	* `vagrant suspend` выключит виртуальную машину с сохранением ее состояния (т.е., при следующем `vagrant up` будут запущены все процессы внутри, которые работали на момент вызова suspend), `vagrant halt` выключит виртуальную машину штатным образом.

1. Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?

1. Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: [документация](https://www.vagrantup.com/docs/providers/virtualbox/configuration.html). Как добавить оперативной памяти или ресурсов процессора виртуальной машине?

1. Команда `vagrant ssh` из директории, в которой содержится Vagrantfile, позволит вам оказаться внутри виртуальной машины без каких-либо дополнительных настроек. Попрактикуйтесь в выполнении обсуждаемых команд в терминале Ubuntu.

1. Ознакомиться с разделами `man bash`, почитать о настройках самого bash:
    * какой переменной можно задать длину журнала `history`, и на какой строчке manual это описывается?
    * что делает директива `ignoreboth` в bash?
1. В каких сценариях использования применимы скобки `{}` и на какой строчке `man bash` это описано?
1. С учётом ответа на предыдущий вопрос, как создать однократным вызовом `touch` 100000 файлов? Получится ли аналогичным образом создать 300000? Если нет, то почему?
1. В man bash поищите по `/\[\[`. Что делает конструкция `[[ -d /tmp ]]`
1. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:

	```bash
	bash is /tmp/new_path_directory/bash
	bash is /usr/local/bin/bash
	bash is /bin/bash
	```

	(прочие строки могут отличаться содержимым и порядком)
    В качестве ответа приведите команды, которые позволили вам добиться указанного вывода или соответствующие скриншоты.

1. Чем отличается планирование команд с помощью `batch` и `at`?

1. Завершите работу виртуальной машины чтобы не расходовать ресурсы компьютера и/или батарею ноутбука.

 
 ---