# Домашнее задание к занятию "6.6. Troubleshooting"

## Задача 1

Перед выполнением задания ознакомьтесь с документацией по [администрированию MongoDB](https://docs.mongodb.com/manual/administration/).

Пользователь (разработчик) написал в канал поддержки, что у него уже 3 минуты происходит CRUD операция в MongoDB и её 
нужно прервать. 

Вы как инженер поддержки решили произвести данную операцию:
- напишите список операций, которые вы будете производить для остановки запроса пользователя
- предложите вариант решения проблемы с долгими (зависающими) запросами в MongoDB


### Ответ:
- Для остановки запроса пользователя воспользуемся мануалом по [этой ссылке](https://docs.mongodb.com/manual/reference/method/db.killOp/)  
  Нам нужна команда `db.killOp(opid)`  
  Чтобы определить `opid`, на томже серевере где пользователь (разработчик) запустил CRUD операцию, необходимо выполнить запрос:
  ```
  use admin
  db.aggregate( [
     { $currentOp : { allUsers: true, localOps: true } },
     { $match : <filter condition> } // Optional.  Specify the condition to find the op.
                                     // e.g. { op: "getmore", "command.collection": "someCollection" }
  ] )
  ```
  который выдаст в ответе opid в формате `<shardName>:<opid on that shard>`  
  ```
  {
     "shard" : "shardB",
     ..
     "opid" : "shardB:79014",
     ...
  }
  ```
  и уже используя эту информацию, выполнить команду `db.killOp("shardB:79014");`
- Можно воспользоваться методом `explain()` для изучения информации по конкретному запросу и возможности его модернизации, например, [как описано в доке](https://docs.mongodb.com/manual/tutorial/analyze-query-plan/):
  ```
  db.inventory.find(
   { quantity: { $gte: 100, $lte: 200 } }
  ).explain("executionStats")
  ```
  Ещё как вариант решения это проблемы, можно воспользоваться методом `cursor.maxTimeMS()`, котоый [описан в мануале](https://docs.mongodb.com/manual/reference/method/cursor.maxTimeMS/)


## Задача 2

Перед выполнением задания познакомьтесь с документацией по [Redis latency troobleshooting](https://redis.io/topics/latency).

Вы запустили инстанс Redis для использования совместно с сервисом, который использует механизм TTL. 
Причем отношение количества записанных key-value значений к количеству истёкших значений есть величина постоянная и
увеличивается пропорционально количеству реплик сервиса. 

При масштабировании сервиса до N реплик вы увидели, что:
- сначала рост отношения записанных значений к истекшим
- Redis блокирует операции записи

Как вы думаете, в чем может быть проблема?

### Ответ:
Проблема скорее всего кроется в `Latency generated by expires`, при активном способе истечения срока действия ключа цикл истечения запускается каждые 100 миллисекунд (10 раз в секунду) и будет выполнять следующие действия:

- Пробные ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP ключи, вытесняют все ключи с истекшим сроком действия.
- Если более 25% ключей оказались просроченными, повторите.  
  
Однако алгоритм является адаптивным и зациклится, если обнаружит, что более 25% ключей уже просрочены в наборе выбранных ключей.
 
## Задача 3

Перед выполнением задания познакомьтесь с документацией по [Common Mysql errors](https://dev.mysql.com/doc/refman/8.0/en/common-errors.html).

Вы подняли базу данных MySQL для использования в гис-системе. При росте количества записей, в таблицах базы,
пользователи начали жаловаться на ошибки вида:
```python
InterfaceError: (InterfaceError) 2013: Lost connection to MySQL server during query u'SELECT..... '
```

Как вы думаете, почему это начало происходить и как локализовать проблему?

Какие пути решения данной проблемы вы можете предложить?

### Ответ:
Ошибки этого типа описаны в [доке](https://dev.mysql.com/doc/refman/8.0/en/error-lost-connection.html)  

Выполнение запроса можно изучить, посредством использования SQL директивы EXPLAIN  

Из возможных проблем может быть:
- миллионы строк отправляются как часть одного или нескольких запросов
- Реже это может произойти, когда клиент пытается установить первоначальное соединение с сервером, из-за настройки connect_timeout в несколько секунд и у клиента медленное соединение интернет
- может возникнуть проблема со BLOB значениями, превышающими параметр max_allowed_packet  
  
Из возможных вариантов решения:
- увеличить net_read_timeout значение по умолчанию с 30 секунд до 60 секунд или больше
-  увеличить connect_timeout до 10 секунт или больше
-  увеличить max_allowed_packet

## Задача 4

Перед выполнением задания ознакомтесь со статьей [Common PostgreSQL errors](https://www.percona.com/blog/2020/06/05/10-common-postgresql-errors/) из блога Percona.

Вы решили перевести гис-систему из задачи 3 на PostgreSQL, так как прочитали в документации, что эта СУБД работает с 
большим объемом данных лучше, чем MySQL.

После запуска пользователи начали жаловаться, что СУБД время от времени становится недоступной. В dmesg вы видите, что:

`postmaster invoked oom-killer`

Как вы думаете, что происходит?

Как бы вы решили данную проблему?

### Ответ:  
Из [рекомендуемой статьи](https://www.percona.com/blog/2020/06/05/10-common-postgresql-errors/) мы видим что OOM Killer вызывется PostgreSQL тогда, когда ему не хватает памяти. Тамже есть рекомендация проверить настройку памяти в соответствии с вашим оборудованием, или можно отключить OOM Killer, что не рекомендуется.  
Конечно можно посмотреть на сами запросы через EXPLAIN, но из вводных данных мы переехали с MySQL, поэтому в данном случае надо смотреть на настройки PostgreSQL в таких параметрах как `effective_cache_size`, `temp_buffers`, `shared_buffers`, `work_mem`, `maintenance_work_mem`, а также на возможность расширения физической памяти сервера.

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---