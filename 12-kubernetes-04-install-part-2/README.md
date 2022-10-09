# Домашнее задание к занятию "12.4 Развертывание кластера на собственных серверах, лекция 2"
Новые проекты пошли стабильным потоком. Каждый проект требует себе несколько кластеров: под тесты и продуктив. Делать все руками — не вариант, поэтому стоит автоматизировать подготовку новых кластеров.

## Задание 1: Подготовить инвентарь kubespray
Новые тестовые кластеры требуют типичных простых настроек. Нужно подготовить инвентарь и проверить его работу. Требования к инвентарю:
* подготовка работы кластера из 5 нод: 1 мастер и 4 рабочие ноды;
* в качестве CRI — containerd;
* запуск etcd производить на мастере.

### Ответ:
- Запускаем виртуальные машины на yandex cloud с помощью [create-vms.sh](create-vms.sh)  
    ```bash
    gorkov@gorkov-big-home:~/HomeWork-netology$ yc compute instance list
    +----------------------+-------+---------------+---------+---------------+-------------+
    |          ID          | NAME  |    ZONE ID    | STATUS  |  EXTERNAL IP  | INTERNAL IP |
    +----------------------+-------+---------------+---------+---------------+-------------+
    | ef375psknt941lrrlr6m | cp1   | ru-central1-c | RUNNING | 51.250.38.39  | 10.130.0.18 |
    | ef3c9ni8svi4vdjkjfag | node3 | ru-central1-c | RUNNING | 51.250.43.118 | 10.130.0.8  |
    | ef3hcrhh56g2k1rn763o | node2 | ru-central1-c | RUNNING | 51.250.32.199 | 10.130.0.20 |
    | ef3kqtm0d762trduj8cm | node1 | ru-central1-c | RUNNING | 51.250.39.98  | 10.130.0.26 |
    | ef3qd9q2qi1flaks88fr | node4 | ru-central1-c | RUNNING | 51.250.35.126 | 10.130.0.37 |
    +----------------------+-------+---------------+---------+---------------+-------------+
    ```

- Подключаемся к cp1 по ssh `ssh yc-user@51.250.38.39` и выполняем следующие команды:
    ```
    sudo apt update
    sudo apt install git pip
    git clone https://github.com/kubernetes-sigs/kubespray
    cd kubespray
    sudo pip3 install -r requirements.txt
    cp -rfp inventory/sample inventory/mycluster
    ```
- В inventory/mycluster меняем [inventory.ini](inventory.ini) в соответствие с нашими требованиями.
- Проверяем в файле `inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml` строчку `container_manager: containerd`
- Для подключения к кластеру из вне добавляем в файл inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml строчку `supplementary_addresses_in_ssl_keys: [51.250.38.39]` где `51.250.38.39` наш внешний ip cp1
- Запускаем установку кластера командой `ansible-playbook -i inventory/mycluster/inventory.ini cluster.yml -b -v`
    ```bash
    PLAY RECAP *************************************************************************************************************************
    cp1                        : ok=717  changed=139  unreachable=0    failed=0    skipped=1255 rescued=0    ignored=9   
    localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    node1                      : ok=497  changed=89   unreachable=0    failed=0    skipped=767  rescued=0    ignored=2   
    node2                      : ok=497  changed=89   unreachable=0    failed=0    skipped=766  rescued=0    ignored=2   
    node3                      : ok=497  changed=89   unreachable=0    failed=0    skipped=766  rescued=0    ignored=2   
    node4                      : ok=497  changed=89   unreachable=0    failed=0    skipped=766  rescued=0    ignored=2  
    ```
- Для управления кластером с мастер ноды копируем конфиг в папку пользователя
    ```
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
    ```
- Проверяем установку:
    ```bash
    yc-user@cp1:~/kubespray$ kubectl get nodes
    NAME    STATUS   ROLES           AGE     VERSION
    cp1     Ready    control-plane   8m4s    v1.25.2
    node1   Ready    <none>          6m47s   v1.24.6
    node2   Ready    <none>          6m47s   v1.24.6
    node3   Ready    <none>          6m48s   v1.24.6
    node4   Ready    <none>          6m48s   v1.24.6

    ```


## Задание 2 (*): подготовить и проверить инвентарь для кластера в AWS
Часть новых проектов хотят запускать на мощностях AWS. Требования похожи:
* разворачивать 5 нод: 1 мастер и 4 рабочие ноды;
* работать должны на минимально допустимых EC2 — t3.small.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---