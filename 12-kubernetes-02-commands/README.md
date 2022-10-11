# Домашнее задание к занятию "12.2 Команды для работы с Kubernetes"
Кластер — это сложная система, с которой крайне редко работает один человек. Квалифицированный devops умеет наладить работу всей команды, занимающейся каким-либо сервисом.
После знакомства с кластером вас попросили выдать доступ нескольким разработчикам. Помимо этого требуется служебный аккаунт для просмотра логов.

## Задание 1: Запуск пода из образа в деплойменте
Для начала следует разобраться с прямым запуском приложений из консоли. Такой подход поможет быстро развернуть инструменты отладки в кластере. Требуется запустить деплоймент на основе образа из hello world уже через deployment. Сразу стоит запустить 2 копии приложения (replicas=2). 

Требования:
 * пример из hello world запущен в качестве deployment
 * количество реплик в deployment установлено в 2
 * наличие deployment можно проверить командой kubectl get deployment
 * наличие подов можно проверить командой kubectl get pods

### Ответ:
[deployment.yaml](deployment.yaml)
```bash
gorkov@gorkov-big-home:~/HomeWork-netology/10-monitoring-04-elk/temp/configs$ kubectl apply -f /home/gorkov/HomeWork-netology/12-kubernetes-02-commands/deployment.yaml
deployment.apps/hello-world created
gorkov@gorkov-big-home:~/HomeWork-netology/10-monitoring-04-elk/temp/configs$ kubectl get deployment
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
hello-world   2/2     2            2           4m41s
gorkov@gorkov-big-home:~/HomeWork-netology/10-monitoring-04-elk/temp/configs$ kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
hello-world-7c8458888d-gffzx   1/1     Running   0          4m51s
hello-world-7c8458888d-xdvs6   1/1     Running   0          4m51s
```


## Задание 2: Просмотр логов для разработки
Разработчикам крайне важно получать обратную связь от штатно работающего приложения и, еще важнее, об ошибках в его работе. 
Требуется создать пользователя и выдать ему доступ на чтение конфигурации и логов подов в app-namespace.

Требования: 
 * создан новый токен доступа для пользователя
 * пользователь прописан в локальный конфиг (~/.kube/config, блок users)
 * пользователь может просматривать логи подов и их конфигурацию (kubectl logs pod <pod_id>, kubectl describe pod <pod_id>)

### Ответ:
- Создаем пользователя
  ```
  adduser dev
  cd /home/dev
  ```
- Генерируем ключ
  ```
  openssl req -new -key dev.key \
  -out dev.csr \
  -subj "/CN=dev"
  ```
- Подпишисываем CSR в Kubernetes CA
  ```
  openssl x509 -req -in dev.csr \
  -CA /etc/kubernetes/pki/ca.crt \
  -CAkey /etc/kubernetes/pki/ca.key \
  -CAcreateserial \
  -out dev.crt -days 500
  ```
- Создайем каталог .certs и закидываем туда открытый и закрытый ключи пользователя:
  ```
  mkdir .certs && mv dev.crt dev.key .certs
  ```

- Создаем пользователя внутри Kubernetes
  ```
  kubectl config set-credentials dev \
  --client-certificate=/home/dev/.certs/dev.crt \
  --client-key=/home/dev/.certs/dev.key
  ```

- Задаем контекст для пользователя
  ```
  kubectl config set-context dev-context \
  --cluster=cluster.local --user=dev
  ```
- редактируем конфиг пользователя
  ```
  apiVersion: v1
  clusters:
  - cluster:
      certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeU1UQXhNREUzTWpreE5Wb1hEVE15TVRBd056RTNNamt4TlZvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTW1SCit5Q0ZUMTIyL1pSNzJWSEs0QmhIOEQ5bzc3VkJUWUVocys0QlZ4Q3ZtMFNwQWxaWmJWSVZFNTFoZXhDTlpOTGwKTG9GVnlRYStITm1NN01hVHYvMnhramE1VnV6bGoxQWJ3K04xVGdZYXNlRFhSNlNrTnp4TEdRRUpzYnRsQWVaTAp6QTZYM3ZjbjJVeUFqenFYdGNYNldqSS9Ba3p3bTRhVkJHaWhySUpLLzN6VGJUbkdmNGZN...
      server: https://127.0.0.1:6443
    name: cluster.local
  contexts:
  - context:
      cluster: cluster.local
      namespace: app-namespace
      user: dev
    name: dev-context
  - context:
      cluster: cluster.local
      user: kubernetes-admin
    name: kubernetes-admin@cluster.local
  current-context: dev-context
  kind: Config
  preferences: {}
  users:
  - name: dev
    user:
      client-certificate: /home/dev/.certs/dev.crt
      client-key: /home/dev/.certs/dev.key
  ```

- даем права на созданные файлы
  ```
  chown -R dev: /home/dev/
  ```
- создаем наймспейс
  ```
  kubectl create namespace app-namespace
  ```

- Создаем роль [role.yaml](role.yaml)
- привязываем роль [rolebind.yaml](rolebind.yaml)

## Задание 3: Изменение количества реплик 
Поработав с приложением, вы получили запрос на увеличение количества реплик приложения для нагрузки. Необходимо изменить запущенный deployment, увеличив количество реплик до 5. Посмотрите статус запущенных подов после увеличения реплик. 

Требования:
 * в deployment из задания 1 изменено количество реплик на 5
 * проверить что все поды перешли в статус running (kubectl get pods)

### Ответ:
```bash
gorkov@gorkov-big-home:~/HomeWork-netology$ kubectl get pods
NAME                           READY   STATUS    RESTARTS      AGE
hello-world-7c8458888d-gffzx   1/1     Running   1 (18d ago)   19d
hello-world-7c8458888d-xdvs6   1/1     Running   1 (18d ago)   19d
gorkov@gorkov-big-home:~/HomeWork-netology$ kubectl apply -f /home/gorkov/HomeWork-netology/12-kubernetes-02-commands/deployment.yaml
deployment.apps/hello-world configured
gorkov@gorkov-big-home:~/HomeWork-netology$ kubectl get pods
NAME                           READY   STATUS    RESTARTS      AGE
hello-world-7c8458888d-2tqhm   1/1     Running   0             11s
hello-world-7c8458888d-7m5ms   1/1     Running   0             11s
hello-world-7c8458888d-gffzx   1/1     Running   1 (18d ago)   19d
hello-world-7c8458888d-q65d8   1/1     Running   0             11s
hello-world-7c8458888d-xdvs6   1/1     Running   1 (18d ago)   19d
gorkov@gorkov-big-home:~/HomeWork-netology$ 
```

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---