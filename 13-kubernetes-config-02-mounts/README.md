# Домашнее задание к занятию "13.2 разделы и монтирование"
Приложение запущено и работает, но время от времени появляется необходимость передавать между бекендами данные. А сам бекенд генерирует статику для фронта. Нужно оптимизировать это.
Для настройки NFS сервера можно воспользоваться следующей инструкцией (производить под пользователем на сервере, у которого есть доступ до kubectl):
* установить helm: curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
* добавить репозиторий чартов: helm repo add stable https://charts.helm.sh/stable && helm repo update
* установить nfs-server через helm: helm install nfs-server stable/nfs-server-provisioner

В конце установки будет выдан пример создания PVC для этого сервера.

## Задание 1: подключить для тестового конфига общую папку
В stage окружении часто возникает необходимость отдавать статику бекенда сразу фронтом. Проще всего сделать это через общую папку. Требования:
* в поде подключена общая папка между контейнерами (например, /static);
* после записи чего-либо в контейнере с беком файлы можно получить из контейнера с фронтом.


### Ответ:

[deployment](1/deployment.yaml)

```bash
gorkov@gorkov-big-home:~$ kubectl get nodes
NAME    STATUS   ROLES           AGE   VERSION
cp1     Ready    control-plane   24h   v1.25.4
node1   Ready    <none>          23h   v1.25.4
gorkov@gorkov-big-home:~$ kubectl get po
NAME                    READY   STATUS    RESTARTS       AGE
db-0                    1/1     Running   1 (109m ago)   23h
main-6df7df484c-mq942   2/2     Running   2 (109m ago)   23h
gorkov@gorkov-big-home:~$ kubectl exec -it main-6df7df484c-mq942 -- /bin/bash
Defaulted container "frontend" out of: frontend, backend
root@main-6df7df484c-mq942:/app# ls /static/
root@main-6df7df484c-mq942:/app# ls         
Dockerfile  demo.conf	item.html  list.json	      package.json  styles
build	    index.html	js	   package-lock.json  static	    webpack.config.js
root@main-6df7df484c-mq942:/app# touch /static/123
root@main-6df7df484c-mq942:/app# ls /static/
123
root@main-6df7df484c-mq942:/app# exit
exit
gorkov@gorkov-big-home:~$ kubectl exec -it main-6df7df484c-mq942 -c backend -- /bin/bash
root@main-6df7df484c-mq942:/app# ls /static/
123
```

## Задание 2: подключить общую папку для прода
Поработав на stage, доработки нужно отправить на прод. В продуктиве у нас контейнеры крутятся в разных подах, поэтому потребуется PV и связь через PVC. Сам PV должен быть связан с NFS сервером. Требования:
* все бекенды подключаются к одному PV в режиме ReadWriteMany;
* фронтенды тоже подключаются к этому же PV с таким же режимом;
* файлы, созданные бекендом, должны быть доступны фронту.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---