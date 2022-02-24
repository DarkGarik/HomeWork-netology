# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ:
```
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
```
```
postgres=# \conninfo
You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
```
или, смотря что подразумевалось под `подключения к БД`
```
postgres=#  SELECT pid, usename, state, wait_event, backend_start from pg_stat_activity;
 pid | usename  | state  |     wait_event      |         backend_start         
-----+----------+--------+---------------------+-------------------------------
  66 |          |        | AutoVacuumMain      | 2022-02-23 18:32:30.7102+00
  68 | postgres |        | LogicalLauncherMain | 2022-02-23 18:32:30.711709+00
  76 | postgres | active |                     | 2022-02-23 18:33:06.041985+00
  64 |          |        | BgWriterHibernate   | 2022-02-23 18:32:30.711085+00
  63 |          |        | CheckpointerMain    | 2022-02-23 18:32:30.709549+00
  65 |          |        | WalWriterMain       | 2022-02-23 18:32:30.709907+00
(6 rows)
```
```
postgres=# \dtS+
                                        List of relations
   Schema   |          Name           | Type  |  Owner   | Persistence |    Size    | Description 
------------+-------------------------+-------+----------+-------------+------------+-------------
 pg_catalog | pg_aggregate            | table | postgres | permanent   | 56 kB      | 
 pg_catalog | pg_am                   | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_amop                 | table | postgres | permanent   | 80 kB      | 
 pg_catalog | pg_amproc               | table | postgres | permanent   | 64 kB      | 
 pg_catalog | pg_attrdef              | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_attribute            | table | postgres | permanent   | 456 kB     | 
 pg_catalog | pg_auth_members         | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_authid               | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_cast                 | table | postgres | permanent   | 48 kB      | 
 ...
```
```
postgres=# \dS pg_ts_config
           Table "pg_catalog.pg_ts_config"
    Column    | Type | Collation | Nullable | Default 
--------------+------+-----------+----------+---------
 oid          | oid  |           | not null | 
 cfgname      | name |           | not null | 
 cfgnamespace | oid  |           | not null | 
 cfgowner     | oid  |           | not null | 
 cfgparser    | oid  |           | not null | 
Indexes:
    "pg_ts_config_cfgname_index" UNIQUE, btree (cfgname, cfgnamespace)
    "pg_ts_config_oid_index" UNIQUE, btree (oid)
```
```
postgres=# \q
postgres@0356f8e18cec:/$ 
```
## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

### Ответ:
```
test_database=# select * from pg_stats where tablename = 'orders' and avg_width = (select max(avg_width) from pg_stats where tablename = 'orders');
-[ RECORD 1 ]----------+--------------------------------------------------------------------------------------------------------------------------------------------------
schemaname             | public
tablename              | orders
attname                | title
inherited              | f
null_frac              | 0
avg_width              | 16
n_distinct             | -1
most_common_vals       | 
most_common_freqs      | 
histogram_bounds       | {"Adventure psql time",Dbiezdmin,"Log gossips","Me and my bash-pet","My little database","Server gravity falls","WAL never lies","War and peace"}
correlation            | -0.3809524
most_common_elems      | 
most_common_elem_freqs | 
elem_count_histogram   | 
```

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

### Ответ:
```
test_database=# create table orders_1 (check (price > 499)) inherits (orders);
CREATE TABLE
test_database=# create table orders_2 (check (price <= 499)) inherits (orders);
CREATE TABLE
test_database=# INSERT INTO orders_1 SELECT * FROM orders WHERE price > 499;
INSERT 0 3
test_database=# INSERT INTO orders_2 SELECT * FROM orders WHERE price <= 499;
INSERT 0 5
test_database=# CREATE RULE price_up_499 AS ON INSERT TO orders WHERE (price > 499) DO INSTEAD INSERT INTO orders_1 VALUES (NEW.*);
CREATE RULE
test_database=# CREATE RULE price_low_499 AS ON INSERT TO orders WHERE (price <= 499) DO INSTEAD INSERT INTO orders_2 VALUES (NEW.*);
CREATE RULE
```
При проектировании таблиц можно заранее применять секционирование таблиц, если подразумевается большой объем данных.  

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

### Ответ:
Для обеспечения уникальности значений столбца `title` достаточно добавить слудующие строки в секции после создания таблиц:
```sql
ALTER TABLE public.orders_1 ADD CONSTRAINT u_orders_1 UNIQUE (title);
ALTER TABLE public.orders_2 ADD CONSTRAINT u_orders_2 UNIQUE (title);
```
```sql
...
CREATE TABLE public.orders_1 (
    CONSTRAINT orders_1_price_check CHECK ((price > 499))
)
INHERITS (public.orders);


ALTER TABLE public.orders_1 OWNER TO postgres;
ALTER TABLE public.orders_1 ADD CONSTRAINT u_orders_1 UNIQUE (title);

--
-- Name: orders_2; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_2 (
    CONSTRAINT orders_2_price_check CHECK ((price <= 499))
)
INHERITS (public.orders);


ALTER TABLE public.orders_2 OWNER TO postgres;
ALTER TABLE public.orders_2 ADD CONSTRAINT u_orders_2 UNIQUE (title);
...
```


---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---