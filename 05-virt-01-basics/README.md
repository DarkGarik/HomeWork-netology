
### Домашнее задание к занятию "5.1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения."


---

## Доработка:
Задание 1  
В чём разница при работе с ядром гостевой ОС для полной и паравиртуализации?

## Ответ:
При паравиртуализации ядро гостевой ОС незначительно модифицируется. Использование ресурсов сервера осуществляется не на прямую, а через специальный гостевой API.

## Задача 1

Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и виртуализации на основе ОС.


### Ответ:
- Полная (аппаратная) виртуализация это когда на голом железе установлен только гипервизор он же и является операционной системой, типа `Hyper-V Core` или `Vmvare` и основная и единственная функция это обеспечение работы виртуальных машин (разделение ресурсов железа для них) 
- Паравиртуализация, это когда уже установленная самостоятельная операционная система, типа `Windows Server` и на ней поднята роль `Hyper-V` которая уже обеспечивает полноценную виртуализацию. Т.е. на сервере могут быть и другие задачи и сервисы работать одновременно с виртуальными машинами.
- Виртуализация на основе ОС это уже больше контейниризация на подобии `Docker`, когда на хосте можно запускать только виртуальные машины с такими же ядрами как на хосте.

## Задача 2

Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.

Организация серверов:
- физические сервера,
- паравиртуализация,
- виртуализация уровня ОС.

Условия использования:
- Высоконагруженная база данных, чувствительная к отказу.
- Различные web-приложения.
- Windows системы для использования бухгалтерским отделом.
- Системы, выполняющие высокопроизводительные расчеты на GPU.

Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

### Ответ:
- Если под физическими серверами подразумевать именно сервер без виртуализации, то для `Высоконагруженной базы данных, чувствительной к отказу` лучше использовать их, т.к. производительность без виртуализации должна быть лучше. Ну и желательно их объединить в кластер для обеспечения отказоустойчивости.
- Для `Различных web-приложений` подойдет и паровиртуализация и также на уровне ОС, в томже докере удобно быстро разворачивать различные web сервисы.
- `Windows системы для использования бухгалтерским отделом.` видимо подразумевается типа 1с-ные базы. для них все же лучше использовать физические сервера, хотя для не сильно загруженных подойдет и паровиртуализация.
- `Системы, выполняющие высокопроизводительные расчеты на GPU.` честно говоря не знаю, на каких виртуальных системах используется хорошо разделение ресурсов GPU, поэтому мне кажется для этих задач лучше использовать физические сервера.

## Задача 3

Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:

1. 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного механизма создания резервных копий.
2. Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) инфраструктуры на базе Linux и Windows виртуальных машин.
3. Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.
4. Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.

### Ответ:
Т.к. я работал только с `Hyper-V`, `ESXi` и `Virtual Box` и в не сильно нагруженных проектах, в основном судить могу по ним.
1. В этом случае скорее всего лучше подойдет `ESXi` c `vsphere` они покроют весь спектр задач, но будет дорого.
2. Судя по лекции, тут подойдет `KVM`, хотя мне кажется и `Hyper-V Core` от `Microsoft` вполне подойдет для этих задач.
3. Тут однозначно `Hyper-V Core`, т.к. решение от `Microsoft` наилучшим образом подойдет именно для `Windows` операционных систем.
4. По моему мнению тут идеально подойдет `Virtual Box` или же `Docker`, на них можно быстро разворачивать несколько экземпляров различных дистрибутивов.

## Задача 4

Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления виртуализацией одновременно) и что необходимо сделать для минимизации этих рисков и проблем. Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

### Ответ:
Использование нескольких разных систем виртуализации, по-моему, не очень удачное решение. Во-первых, это проблемы с миграцией виртуальных машин между физическими серверами, проблемы с создание резервных копий, т.к. придётся использовать различные сценарии. Опять же уровень подготовки специалистов, их обслуживающих должен быть соответствующим. Конечно, многие проблемы с можно решить с помощью стороннего платного ПО, типа `Veeam`, там и бэкапы на различных гипервизорах можно настроить и восстановление бэкапа с одной на другую систему виртуализации. Но все же если есть выбор, то лучше использовать одну систему виртуализации, максимум что это для песочницы какой-нибудь `Virtual Box` отдельно использовать.
