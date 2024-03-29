# Домашнее задание к занятию "14.5 SecurityContext, NetworkPolicies"

## Задача 1: Рассмотрите пример 14.5/example-security-context.yml

Создайте модуль

```
kubectl apply -f 14.5/example-security-context.yml
```

Проверьте установленные настройки внутри контейнера

```
kubectl logs security-context-demo
uid=1000 gid=3000 groups=3000
```

### Ответ:
```powershell
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.5> cat .\14.5\example-security-context.yml
---
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  containers:
  - name: sec-ctx-demo
    image: fedora:latest
    command: [ "id" ]
    # command: [ "sh", "-c", "sleep 1h" ]
    securityContext:
      runAsUser: 1000
      runAsGroup: 3000
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.5> kubectl apply -f 14.5/example-security-context.yml
pod/security-context-demo created
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.5> kubectl get po
NAME                    READY   STATUS              RESTARTS   AGE
security-context-demo   0/1     ContainerCreating   0          30s
PS C:\Users\gorkov\Desktop\netology\homework\HomeWork-netology\14.5> kubectl logs security-context-demo                
uid=1000 gid=3000 groups=3000
```


## Задача 2 (*): Рассмотрите пример 14.5/example-network-policy.yml

Создайте два модуля. Для первого модуля разрешите доступ к внешнему миру
и ко второму контейнеру. Для второго модуля разрешите связь только с
первым контейнером. Проверьте корректность настроек.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, statefulset, service) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---