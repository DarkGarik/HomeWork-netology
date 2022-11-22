# Домашнее задание к занятию "14.4 Сервис-аккаунты"

## Задача 1: Работа с сервис-аккаунтами через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать сервис-аккаунт?

```
kubectl create serviceaccount netology
```

### Как просмотреть список сервис-акаунтов?

```
kubectl get serviceaccounts
kubectl get serviceaccount
```

### Как получить информацию в формате YAML и/или JSON?

```
kubectl get serviceaccount netology -o yaml
kubectl get serviceaccount default -o json
```

### Как выгрузить сервис-акаунты и сохранить его в файл?

```
kubectl get serviceaccounts -o json > serviceaccounts.json
kubectl get serviceaccount netology -o yaml > netology.yml
```

### Как удалить сервис-акаунт?

```
kubectl delete serviceaccount netology
```

### Как загрузить сервис-акаунт из файла?

```
kubectl apply -f netology.yml
```

### Ответ:
```powershell
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> minikube start
😄  minikube v1.28.0 на Microsoft Windows 11 Pro 10.0.22621 Build 22621
✨  Используется драйвер virtualbox на основе существующего профиля
👍  Запускается control plane узел minikube в кластере minikube
🔄  Перезагружается существующий virtualbox VM для "minikube" ...
❗  This VM is having trouble accessing https://registry.k8s.io
💡  To pull new external images, you may need to configure a proxy: https://minikube.sigs.k8s.io/docs/reference/networking/proxy/
🐳  Подготавливается Kubernetes v1.25.3 на Docker 20.10.20 ...
    ▪ Используется образ gcr.io/k8s-minikube/storage-provisioner:v5
🔎  Компоненты Kubernetes проверяются ...
🌟  Включенные дополнения: storage-provisioner, default-storageclass
🏄  Готово! kubectl настроен для использования кластера "minikube" и "default" пространства имён по умолчанию
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> kubectl get nodes
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   3d6h   v1.25.3
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> kubectl create serviceaccount netology
serviceaccount/netology created
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> kubectl get serviceaccounts
NAME       SECRETS   AGE
default    0         3d6h
netology   0         2m15s
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> kubectl get serviceaccount
NAME       SECRETS   AGE
default    0         3d6h
netology   0         2m27s
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> kubectl get serviceaccount netology -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2022-11-22T18:24:35Z"
  name: netology
  namespace: default
  resourceVersion: "1560"
  uid: 074df360-6f9f-4c7e-ae40-b6aec135d5ed
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> kubectl get serviceaccount default -o json
{
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "creationTimestamp": "2022-11-19T12:20:48Z",
        "name": "default",
        "namespace": "default",
        "resourceVersion": "316",
        "uid": "026d7531-ff67-48f8-93d0-5acdf1efbc11"
    }
}
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology> cd .\14.4\                    
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.4> kubectl get serviceaccounts -o json > serviceaccounts.json
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.4> kubectl get serviceaccount netology -o yaml > netology.yml
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.4> kubectl delete serviceaccount netology
serviceaccount "netology" deleted
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.4> kubectl apply -f netology.yml
serviceaccount/netology created
```

## Задача 2 (*): Работа с сервис-акаунтами внутри модуля

Выбрать любимый образ контейнера, подключить сервис-акаунты и проверить
доступность API Kubernetes

```
kubectl run -i --tty fedora --image=fedora --restart=Never -- sh
```

Просмотреть переменные среды

```
env | grep KUBE
```

Получить значения переменных

```
K8S=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT
SADIR=/var/run/secrets/kubernetes.io/serviceaccount
TOKEN=$(cat $SADIR/token)
CACERT=$SADIR/ca.crt
NAMESPACE=$(cat $SADIR/namespace)
```

Подключаемся к API

```
curl -H "Authorization: Bearer $TOKEN" --cacert $CACERT $K8S/api/v1/
```

В случае с minikube может быть другой адрес и порт, который можно взять здесь

```
cat ~/.kube/config
```

или здесь

```
kubectl cluster-info
```

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, serviceaccounts) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---