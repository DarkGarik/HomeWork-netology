# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

### Ответ:
docker-compose.yaml
```yaml
# Use postgres/example user/password credentials
version: '3.1'

services:

  db:
    image: postgres:12
    restart: always
    ports:
      - 5432:5432
    environment:
      POSTGRES_PASSWORD: example
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - ./base:/var/lib/postgresql/data
      - ./backup:/backup
```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db

### Ответ:
```
test_db=# \l
                                     List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |       Access privileges
-----------+----------+----------+------------+------------+--------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                  +
           |          |          |            |            | postgres=CTc/postgres         +
           |          |          |            |            | "test-admin-user"=CTc/postgres
(4 rows)
```
```
test_db=# \d orders
                                 Table "public.orders"
 Column |       Type        | Collation | Nullable |              Default
--------+-------------------+-----------+----------+------------------------------------
 id     | integer           |           | not null | nextval('orders_id_seq'::regclass)
 name   | character varying |           |          |
 price  | integer           |           |          |
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_ord_fkey" FOREIGN KEY (ord) REFERENCES orders(id)

test_db=# \d clients
                                  Table "public.clients"
 Column  |       Type        | Collation | Nullable |               Default
---------+-------------------+-----------+----------+-------------------------------------
 id      | integer           |           | not null | nextval('clients_id_seq'::regclass)
 surname | character varying |           |          |
 country | character varying |           |          |
 ord     | integer           |           |          |
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "clients_ord_fkey" FOREIGN KEY (ord) REFERENCES orders(id)
```
```
SELECT * from information_schema.table_privileges WHERE grantee = 'test-admin-user' or grantee = 'test-simple-user';
```
```
test_db=# SELECT * from information_schema.table_privileges WHERE grantee = 'test-admin-user' or grantee = 'test-simple-user';
 grantor  |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy
----------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 postgres | test-admin-user  | test_db       | public       | clients    | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | public       | clients    | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | public       | clients    | TRIGGER        | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | public       | clients    | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | public       | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | public       | orders     | TRIGGER        | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | public       | orders     | DELETE         | NO           | NO
(22 rows)
```
## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

### Ответ:
```
test_db=# INSERT INTO orders (name, price) VALUES ('Шоколад', '10');
INSERT 0 1
```
```
test_db=# INSERT INTO orders (name, price) VALUES
test_db-# ('Принтер', '300'),
test_db-# ('Книга', '500'),
test_db-# ('Монитор', '7000'),
test_db-# ('Гитара', '4000');
INSERT 0 4
```
```
test_db=# INSERT INTO clients (surname, country) VALUES
test_db-# ('Иванов Иван Иванович', 'USA'),
test_db-# ('Петров Петр Петрович', 'Canada'),
test_db-# ('Иоганн Себастьян Бах', 'Japan'),
test_db-# ('Ронни Джеймс Дио', 'Russia'),
test_db-# ('Ritchie Blackmore|', 'Russia');
INSERT 0 5
```
```
test_db=# SELECT count(*) FROM orders;
 count
-------
     5
(1 row)

test_db=# SELECT count(*) FROM clients;
 count
-------
     5
(1 row)
```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказк - используйте директиву `UPDATE`.

### ответ:
Сначала получаем id из таблицы orders, потом обновляем таблицу clients:
```
test_db=# SELECT id from orders WHERE name = 'Книга';
 id
----
  4
(1 row)

test_db=# UPDATE clients SET ord = '4' WHERE surname = 'Иванов Иван Иванович';
UPDATE 1
test_db=# SELECT id from orders WHERE name = 'Монитор';
 id
----
  5
(1 row)

test_db=# UPDATE clients SET ord = '5' WHERE surname = 'Петров Петр Петрович';
UPDATE 1
test_db=# SELECT id from orders WHERE name = 'Гитара';
 id
----
  6
(1 row)

test_db=# UPDATE clients SET ord = '6' WHERE surname = 'Иоганн Себастьян Бах';
UPDATE 1
```
```
test_db=# SELECT surname from clients WHERE ord is NOT NULL;
       surname
----------------------
 Иванов Иван Иванович
 Петров Петр Петрович
 Иоганн Себастьян Бах
(3 rows)
```
или используем сложную выборку:
```
test_db=# SELECT c.surname, o.name FROM clients c INNER JOIN orders o ON c.ord = o.id;
       surname        |  name
----------------------+---------
 Иванов Иван Иванович | Книга
 Петров Петр Петрович | Монитор
 Иоганн Себастьян Бах | Гитара
(3 rows)
```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

### Ответ:
```
test_db=# explain SELECT surname from clients WHERE ord is NOT NULL;
                       QUERY PLAN
--------------------------------------------------------
 Seq Scan on clients  (cost=0.00..1.05 rows=5 width=32)
   Filter: (ord IS NOT NULL)
(2 rows)
```

Данный вывод показывает что будет сделано сканирование по таблице clients с приблизительным верменем запуска 0.00 и приблизительным временем выполнения 1.05, если запрос выполнит сканирование по всем строкам, ожидаемое число строк равно 5 и ожидаемый средний размер строк 32 байта. Также показано что будет применен фильтр `ord IS NOT NULL`

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

### Ответ:
```
pg_dump test_db > /backup/test_db.sql
```
``` yaml
# Use postgres/example user/password credentials
version: '3.1'

services:

  db1:
    image: postgres:12
    restart: always
    ports:
      - 5432:5432
    environment:
      POSTGRES_PASSWORD: example
#      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
#      - ./base:/var/lib/postgresql/data
      - ./backup:/backup
```
```
postgres=# create database test_db;
CREATE DATABASE
postgres=# create user "test-admin-user";
CREATE ROLE
postgres=# create user "test-simple-user";
CREATE ROLE
postgres=# \q
postgres@8629543fc4b2:/$ psql test_db < /backup/test_db.sql
```


---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---