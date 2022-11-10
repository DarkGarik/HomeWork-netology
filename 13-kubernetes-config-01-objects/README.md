# Домашнее задание к занятию "13.1 контейнеры, поды, deployment, statefulset, services, endpoints"
Настроив кластер, подготовьте приложение к запуску в нём. Приложение стандартное: бекенд, фронтенд, база данных. Его можно найти в папке 13-kubernetes-config.

## Задание 1: подготовить тестовый конфиг для запуска приложения
Для начала следует подготовить запуск приложения в stage окружении с простыми настройками. Требования:
* под содержит в себе 2 контейнера — фронтенд, бекенд;
* регулируется с помощью deployment фронтенд и бекенд;
* база данных — через statefulset.

### Ответ:
- Собрал докер образа из папки [13-kubernetes-config](13-kubernetes-config)  
Кстати frontend из образа `node:lts-buster` не собирается, видимо приложение было рассчитано на 16 релиз, заменил на `node:16-buster`  
- закинул образа на докерхаб
- [deployment](1/deployment.yaml) для фронтенд и бекенд
- [statefulset](1/statefulset.yaml) для базы данных

```bash
gorkov@gorkov-HP-Laptop-14s:~$ kubectl get po
NAME                    READY   STATUS    RESTARTS   AGE
db-0                    1/1     Running   0          96m
main-66d745c896-qgqpw   2/2     Running   0          94m
gorkov@gorkov-HP-Laptop-14s:~$ kubectl get deployments
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
main   1/1     1            1           95m
gorkov@gorkov-HP-Laptop-14s:~$ kubectl get statefulset
NAME   READY   AGE
db     1/1     97m
gorkov@gorkov-HP-Laptop-14s:~$ kubectl get service
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
backend      ClusterIP   10.233.7.235    <none>        9000/TCP   95m
db           ClusterIP   10.233.47.227   <none>        5432/TCP   97m
frontend     ClusterIP   10.233.39.102   <none>        8000/TCP   95m
kubernetes   ClusterIP   10.233.0.1      <none>        443/TCP    44h
gorkov@gorkov-HP-Laptop-14s:~$ kubectl exec main-66d745c896-qgqpw -- curl localhost
Defaulted container "frontend" out of: frontend, backend
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Список</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/build/main.css" rel="stylesheet">
</head>
<body>
    <main class="b-page">
        <h1 class="b-page__title">Список</h1>
        <div class="b-page__content b-items js-list"></div>
    </main>
    <script src="/build/main.js"></script>
</body>
100   448  100   448    0     0   437k      0 --:--:-- --:--:-- --:--:--  437k

```

## Задание 2: подготовить конфиг для production окружения
Следующим шагом будет запуск приложения в production окружении. Требования сложнее:
* каждый компонент (база, бекенд, фронтенд) запускаются в своем поде, регулируются отдельными deployment’ами;
* для связи используются service (у каждого компонента свой);
* в окружении фронта прописан адрес сервиса бекенда;
* в окружении бекенда прописан адрес сервиса базы данных.

## Задание 3 (*): добавить endpoint на внешний ресурс api
Приложению потребовалось внешнее api, и для его использования лучше добавить endpoint в кластер, направленный на это api. Требования:
* добавлен endpoint до внешнего api (например, геокодер).

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, statefulset, service) или скриншот из самого Kubernetes, что сервисы подняты и работают.

---