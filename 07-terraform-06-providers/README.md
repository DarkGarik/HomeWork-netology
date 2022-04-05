# Домашнее задание к занятию "7.6. Написание собственных провайдеров для Terraform."

Бывает, что 
* общедоступная документация по терраформ ресурсам не всегда достоверна,
* в документации не хватает каких-нибудь правил валидации или неточно описаны параметры,
* понадобиться использовать провайдер без официальной документации,
* может возникнуть необходимость написать свой провайдер для системы используемой в ваших проектах.   

## Задача 1. 
Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: 
[https://github.com/hashicorp/terraform-provider-aws.git](https://github.com/hashicorp/terraform-provider-aws.git).
Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.  


1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.   
1. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
    * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.
    * Какая максимальная длина имени? 
    * Какому регулярному выражению должно подчиняться имя? 

### Ответ:
1. `resource` перечисленны в файле [provider.go начиная со строки 868](https://github.com/hashicorp/terraform-provider-aws/blob/de6bf7541dd8a5c81d0471e7e8cb76eb76578e66/internal/provider/provider.go#L868)  
   `data_source` в том-же [provider.go со строки 412](https://github.com/hashicorp/terraform-provider-aws/blob/de6bf7541dd8a5c81d0471e7e8cb76eb76578e66/internal/provider/provider.go#L412)
1. [`name` конфликтует с параметром `name_prefix`](https://github.com/hashicorp/terraform-provider-aws/blob/de6bf7541dd8a5c81d0471e7e8cb76eb76578e66/internal/service/sqs/queue.go#L82)  
   В функции `resourceQueueCustomizeDiff` начиная со строки [407 в файле /internal/service/sqs/queue.go](https://github.com/hashicorp/terraform-provider-aws/blob/690cee18d1d3aefce2270cc88cf21e05b6ae6a06/internal/service/sqs/queue.go#L407) есть регулярное выражение regexp.MustCompile в котором как раз и указана длина имени:
   ``` GO
    if fifoQueue {
		re = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,75}\.fifo$`)
	} else {
		re = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,80}$`)
	}
    ```
   


## Задача 2. (Не обязательно) 
В рамках вебинара и презентации мы разобрали как создать свой собственный провайдер на примере кофемашины. 
Также вот официальная документация о создании провайдера: 
[https://learn.hashicorp.com/collections/terraform/providers](https://learn.hashicorp.com/collections/terraform/providers).

1. Проделайте все шаги создания провайдера.
2. В виде результата приложение ссылку на исходный код.
3. Попробуйте скомпилировать провайдер, если получится то приложите снимок экрана с командой и результатом компиляции.   

---

### Как сдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---