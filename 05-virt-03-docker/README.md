
# Домашнее задание к занятию "5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"


---

## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

### Ответ:
https://hub.docker.com/r/gorkov/nginx  


## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
- Nodejs веб-приложение;
- Мобильное приложение c версиями для Android и iOS;
- Шина данных на базе Apache Kafka;
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
- Мониторинг-стек на базе Prometheus и Grafana;
- MongoDB, как основное хранилище данных для java-приложения;
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.

### Ответ:
- Возможно для высоконагруженных приложений лучше использовать полноценную виртуализацию, но я думаю что и на docker вполне себе будет работать.
- Подойдет использование Docker, удобно упаковать все зависимости.
- Честно говоря, не знаю как работают мобильные приложения под капотом, но допускаю, что БД и само приложение можно завернуть в docker без проблем.
- Apache Kafka отлично работает на docker, есть много образов на docker hub, в том числе и от разработчиков Kafka.
- Для Elasticsearch кластера вполне себе подходит docker, есть множество примеров реализации такой схемы.
- Также как и для логированния, для мониторинга на базе Prometheus и Grafana подходит docker.
- MongoDB вполне себе работает на docker, да и смо java-приложение можно завернуть в отдельный docker контейнер.
- Gitlab server отлично запускается и работает на docker, есть официальный мануал по этому поводу https://docs.gitlab.com/ee/install/docker.html Docker Registry также работает на docker.

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.

### Ответ:

``` bash
vagrant@server1:~/debian$ sudo mkdir /data
vagrant@server1:~/debian$ sudo chmod 777 /data
vagrant@server1:~/debian$ docker run -it -v /data:/data -d centos bash
5d4b2156153e4266106409f0fbdda4fd1c151a08489155c539b0f6a99c114854
vagrant@server1:~/debian$ docker run -it -v /data:/data -d debian bash
6d96e23f2e8b57d4e3dbc7f9defb28ae2629be0cf3af9c8e7e12c14dfe327a3a
vagrant@server1:~/debian$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED              STATUS              PORTS     NAMES
6d96e23f2e8b   debian    "bash"    56 seconds ago       Up 56 seconds                 tender_wilbur
5d4b2156153e   centos    "bash"    About a minute ago   Up About a minute             busy_newton
vagrant@server1:~/debian$ docker exec -it busy_newton bash
[root@5d4b2156153e /]# echo test > /data/centos.txt
[root@5d4b2156153e /]# exit
exit
vagrant@server1:~/debian$ echo test > /data/host.txt
vagrant@server1:~/debian$ docker exec -it tender_wilbur bash
root@6d96e23f2e8b:/# ls /data
centos.txt  host.txt
root@6d96e23f2e8b:/# cat /data/centos.txt
test
root@6d96e23f2e8b:/# cat /data/host.txt
test
root@6d96e23f2e8b:/# exit
exit
```

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.


---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---