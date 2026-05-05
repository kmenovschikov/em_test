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
