# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

### Ответ:
- [dockerfile:](Dockerfile)
    ```dockerfile
    FROM centos:7

    RUN yum update -y && \
        yum install wget perl-Digest-SHA -y && \
        wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.0.0-linux-x86_64.tar.gz && \
        wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.0.0-linux-x86_64.tar.gz.sha512 && \
        shasum -a 512 -c elasticsearch-8.0.0-linux-x86_64.tar.gz.sha512 && \
        tar -xzf elasticsearch-8.0.0-linux-x86_64.tar.gz

    COPY elasticsearch.yml /elasticsearch-8.0.0/config

    RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000 && \
        mkdir /var/lib/elasticsearch && \
        mkdir /var/lib/elasticsearch/data && \
        chown -R elasticsearch:elasticsearch /elasticsearch-8.0.0 && \
        chown -R elasticsearch:elasticsearch /var/lib/elasticsearch

    USER elasticsearch

    WORKDIR /elasticsearch-8.0.0

    CMD ./bin/elasticsearch

    EXPOSE 9200
    ```
- https://hub.docker.com/r/gorkov/elastic  
- json
    ```json
    {
    "name" : "netology_test",
    "cluster_name" : "elasticsearch",
    "cluster_uuid" : "IBDUa6BxSLGuXPeyiBetYw",
    "version" : {
        "number" : "8.0.0",
        "build_flavor" : "default",
        "build_type" : "tar",
        "build_hash" : "1b6a7ece17463df5ff54a3e1302d825889aa1161",
        "build_date" : "2022-02-03T16:47:57.507843096Z",
        "build_snapshot" : false,
        "lucene_version" : "9.0.0",
        "minimum_wire_compatibility_version" : "7.17.0",
        "minimum_index_compatibility_version" : "7.0.0"
    },
    "tagline" : "You Know, for Search"
    }
    ```


## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

### Ответ:
- http://localhost:9200/_cat/indices?v
    ```
    health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    green  open   ind-1 lkYToM7fRVaCy9LlRdD_gg   1   0          0            0       225b           225b
    yellow open   ind-3 Gjyn2Y2nQMKYvjJyVnJscw   4   2          0            0       900b           900b
    yellow open   ind-2 zpqwG3zZQTa7vI81rEiALg   2   1          0            0       450b           450b
    ```
- http://localhost:9200/_cat/health?v
    ```
    epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
    1645975622 15:27:02  elasticsearch yellow          1         1      8   8    0    0       10             0                  -                 44.4%
    ```
- Состояние yellow у индексов в котрых уазаны несколько реплик, т.к. у нас одна только нода, рекплики делать некуда.

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

### Ответ:
-   
    ```bash
    [elasticsearch@c2e57573e052 elasticsearch-8.0.0]$ curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'
    > {
    >   "type": "fs",
    >   "settings": {
    >     "location": "/elasticsearch-8.0.0/snapshots"
    >   }
    > }
    > '
    {
    "acknowledged" : true
    }
    ```
- http://localhost:9200/_cat/indices?v
    ```
    health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    green  open   test  M-JHscv1Q7G-PcgE1Hm9YA   1   0          0            0       225b           225b
    ```
- 
    ```
    [elasticsearch@c2e57573e052 elasticsearch-8.0.0]$ ls -l snapshots/
    total 36
    -rw-r--r-- 1 elasticsearch elasticsearch   855 Feb 27 16:33 index-0
    -rw-r--r-- 1 elasticsearch elasticsearch     8 Feb 27 16:33 index.latest
    drwxr-xr-x 4 elasticsearch elasticsearch  4096 Feb 27 16:33 indices
    -rw-r--r-- 1 elasticsearch elasticsearch 17407 Feb 27 16:33 meta-0mzSdxa6SOa7aZi5Ih6rfw.dat
    -rw-r--r-- 1 elasticsearch elasticsearch   364 Feb 27 16:33 snap-0mzSdxa6SOa7aZi5Ih6rfw.dat
    ```
---
- http://localhost:9200/_cat/indices?v
    ```
    health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    green  open   test-2 cTFP3d_lQESAxMYFq7fpXw   1   0          0            0       225b           225b
    ```
- В документации рекомендуется перед восстановлением удалить все индексы, воизбежании конфликтов, но по заданию у нас это не уточнялось, и есть всего два разных индекса, так что делал без очистки:
    ```
    [elasticsearch@c2e57573e052 elasticsearch-8.0.0]$ curl -X POST "localhost:9200/_snapshot/netology_backup/my_snapshot_2022.02.27/_restore?pretty"
    {
    "accepted" : true
    }
    ```
    http://localhost:9200/_cat/indices?v
    ```
    health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    green  open   test-2 cTFP3d_lQESAxMYFq7fpXw   1   0          0            0       225b           225b
    green  open   test   0Rza1_tzSmW67EwV32hMYg   1   0          0            0       225b           225b
```

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---