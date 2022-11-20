# Домашнее задание к занятию "14.3 Карты конфигураций"

## Задача 1: Работа с картами конфигураций через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать карту конфигураций?

```
kubectl create configmap nginx-config --from-file=nginx.conf
kubectl create configmap domain --from-literal=name=netology.ru
```

### Как просмотреть список карт конфигураций?

```
kubectl get configmaps
kubectl get configmap
```

### Как просмотреть карту конфигурации?

```
kubectl get configmap nginx-config
kubectl describe configmap domain
```

### Как получить информацию в формате YAML и/или JSON?

```
kubectl get configmap nginx-config -o yaml
kubectl get configmap domain -o json
```

### Как выгрузить карту конфигурации и сохранить его в файл?

```
kubectl get configmaps -o json > configmaps.json
kubectl get configmap nginx-config -o yaml > nginx-config.yml
```

### Как удалить карту конфигурации?

```
kubectl delete configmap nginx-config
```

### Как загрузить карту конфигурации из файла?

```
kubectl apply -f nginx-config.yml
```

### Ответ:
```powershell
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get nodes
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   109s   v1.25.3
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl create configmap nginx-config --from-file=nginx.conf
configmap/nginx-config created
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl create configmap domain --from-literal=name=netology.ru
configmap/domain created
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmaps
NAME               DATA   AGE
domain             1      22s
kube-root-ca.crt   1      2m43s
nginx-config       1      42s
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmap
NAME               DATA   AGE
domain             1      42s
kube-root-ca.crt   1      3m3s
nginx-config       1      62s
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmap nginx-config
NAME           DATA   AGE
nginx-config   1      102s
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl describe configmap domain
Name:         domain
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
name:
----
netology.ru

BinaryData
====

Events:  <none>
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmap nginx-config -o yaml
apiVersion: v1
data:
  nginx.conf: "server {\r\n    listen 80;\r\n    server_name  netology.ru www.netology.ru;\r\n
    \   access_log  /var/log/nginx/domains/netology.ru-access.log  main;\r\n    error_log
    \  /var/log/nginx/domains/netology.ru-error.log info;\r\n    location / {\r\n
    \       include proxy_params;\r\n        proxy_pass http://10.10.10.10:8080/;\r\n
    \   }\r\n}\r\n"
kind: ConfigMap
metadata:
  creationTimestamp: "2022-11-19T12:22:49Z"
  name: nginx-config
  namespace: default
  resourceVersion: "461"
  uid: f5d69cf6-d697-4ba9-9468-fa91faa53d7a
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmap domain -o json
{
    "apiVersion": "v1",
    "data": {
        "name": "netology.ru"
    },
    "kind": "ConfigMap",
    "metadata": {
        "creationTimestamp": "2022-11-19T12:23:09Z",
        "name": "domain",
        "namespace": "default",
        "resourceVersion": "476",
        "uid": "90526d4e-29c3-4dbf-a585-5da7a82f9d9a"
    }
}
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmaps -o json > configmaps.json
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmap nginx-config -o yaml > nginx-config.yml
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl delete configmap nginx-config
configmap "nginx-config" deleted
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl apply -f nginx-config.yml
configmap/nginx-config created
PS C:\Users\gorkov\Desktop\netology\homework\clokub-homeworks\14.3> kubectl get configmaps
NAME               DATA   AGE
domain             1      4m38s
kube-root-ca.crt   1      6m59s
nginx-config       1      11s
```

## Задача 2 (*): Работа с картами конфигураций внутри модуля

Выбрать любимый образ контейнера, подключить карты конфигураций и проверить
их доступность как в виде переменных окружения, так и в виде примонтированного
тома

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, configmaps) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---