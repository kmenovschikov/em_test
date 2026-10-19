Задание:   
1) Используя Docker и Docker Compose поднять:    
Backend – Python-сервер на http.server, отвечающий на / текстом "Hello from Effective Mobile!".    
Frontend - Nginx – reverse-proxy, принимает запросы на порту 80 и перенаправляет их на бэкенд.     

      
2) Nginx слушает порт, указанный в .env (по умолчанию 80), и принимает входящие запросы.     
В конфигурационном файле nginx/nginx.conf определён upstream backend, который указывает на контейнер backend (имя сервиса в Docker Compose) и порт 8080.     
Все запросы к корневому пути / проксируются на этот upstream с помощью proxy_pass.     
Backend обрабатывает запрос и возвращает строку "Hello from Effective Mobile!".     
Таким образом, клиент взаимодействует только с Nginx, а Nginx прозрачно проксирует трафик к внутреннему сервису.     
Backend-приложение запускается от непривилегированного пользователя appuser (не root).     
Nginx по умолчанию работает от пользователя nginx (не root).     
Backend не публикует порты наружу, доступен только внутри сети Docker. 


3) Структура проекта:      
     
    ├── backend/       
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Dockerfile       
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── app.py       
        ├── nginx/         
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Dockerfile       
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── nginx.conf   
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── docker-compose.yml       
   ├── .env       
   └── README.md      
     
#
Этапы решения:
1) Создаем простейший http-сервер - /backend/app.py
2) Создаем докер-образ с этим сервером - kmenovschikov/em_test:app-1.0
3) Создаем докер-образ на основе nginx и копируем туда настройки revers proxy - kmenovschikov/em_test:nginx-1.0
4) Пушим оба образа в docker hub

Запуск:
1) git clone https://github.com/kmenovschikov/em_test.git
2) docker-compose up -d
3) curl http://localhost
#
Комментарии и замечания проверяющего:

Плюсы:
1. Docker-compose присутствует и поднимает оба сервиса
2. Backend порт 8800 НЕ публикуется наружу (только nginx порт 80)
3. Используется кастомная docker-сеть
4. nginx проксирует на backend (хоть и по IP)
5. README с базовыми инструкциями по запуску
6. Понятная структура проекта (backend/, nginx/)
 
Что можно улучшить:
1. Хардкод IP-адресов в docker-compose и nginx — используется `ipv4_address: 192.168.168.2` и `ipv4_address: 192.168.168.3` вместо service names, а в nginx.conf указан `proxy_pass http://192.168.168.2:8800;` (нарушение принципа Docker Service Discovery)
2. Backend НЕ отвечает "Hello from Effective Mobile!" на HTTP запрос — приложение использует `SimpleHTTPRequestHandler` который отдаёт статический файл index.html, а не возвращает текст напрямую при GET запросе
3. Неверный порт backend — порт 8800 вместо требуемого 8080 по ТЗ
4. nginx не передаёт необходимые заголовки — отсутствуют `proxy_set_header Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` (хотя это не критический фактор, но в совокупности с другими проблемами)
5. Используются latest теги образов (python:latest, nginx:latest)
6. Отсутствует .dockerignore
7. Отсутствует .gitignore
8. Запуск от root в обоих контейнерах
9. nginx.conf не включает заголовки для корректного проксирования
10. Отсутствует upstream блок в nginx.conf
11. README очень краткий без схемы архитектуры
12. Нет healthcheck для сервисов
