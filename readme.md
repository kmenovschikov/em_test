Этапы решения:
1) Создаем простейший http-сервер - app.py
2) Создаем докер-образ с этим сервером - kmenovschikov/em_test:app-1.0
3) Создаем докер-образ на основе nginx и копируем туда настройки revers proxy - kmenovschikov/em_test:nginx-1.0
4) Пушим оба образа в docker hub

Запуск:
1) git clone https://github.com/kmenovschikov/em_test.git
2) docker-compose up -d
3) curl http://localhost