1. Мы запросили страницу `http://stackoverflow.com/questions`, на что получили ответ `301 Moved Permanently`, что означает что страница перемещена по адресу `https://stackoverflow.com/questions`
```bash
vagrant@vagrant:~$ telnet stackoverflow.com 80
Trying 151.101.65.69...
Connected to stackoverflow.com.
Escape character is '^]'.
GET /questions HTTP/1.0
HOST: stackoverflow.com

HTTP/1.1 301 Moved Permanently
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: 20a1e848-5f8e-4059-b2e3-733752959984
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Fri, 26 Nov 2021 18:37:49 GMT
Via: 1.1 varnish
Connection: close
X-Served-By: cache-fra19143-FRA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1637951869.332532,VS0,VE92
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=df18353b-2181-b447-b809-aca7149aea5a; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly

Connection closed by foreign host.
```
2. 