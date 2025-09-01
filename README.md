# DDS — Веб-интерфейс и REST API для учёта движения денежных средств

Исполнитель: **Алексеев Лев, tg: @lsalekseev** 

Тестовое задание для демонстрации навыков разработки backend-приложений на Django с использованием PostgreSQL.

---

## Скриншоты

**Главная страница со списком ДДС и примененными фильтрами**   
![Главная](https://drive.google.com/uc?export=view&id=1-S1MR9SPbWjEP_n8_y0iv-KUmYSmTPHH)

**Создание записи о ДДС**   
![Создание](https://drive.google.com/uc?export=view&id=1-dEDVYdwRTk9dd5-aOav91V9oRQKLPbj)

**Редактирование записи о ДДС**   
![Редактирование](https://drive.google.com/uc?export=view&id=1uc26uFRXk-zMTGa1J6EbwlL5nWTwDVV5)

**Админка: статусы/типы/категории/подкатегории**  
![Админка справочники](https://drive.google.com/uc?export=view&id=1vi5O98zIFPf6mOCGm_25G9ZJSiEQncBI)

**Документация Swagger**  
![Swagger](https://drive.google.com/uc?export=view&id=1YkB2qoBRUi0r8OGqmsj3LLuRSys1w5Ti)

---

## Содержание

- [Функциональность](#функциональность)
- [Стек и версии](#стек-и-версии)
- [Установка и запуск](#установка-и-запуск)
- [API Документация](#api-документация)
- [UI](#ui)
- [Технические детали](#технические-детали)
- [Ссылка на демо-версию](#ссылка-на-демо-версию)

---

## Функциональность

- Список ДДС с фильтрацией по периоду, статусу, типу, категории, подкатегории.
- Итоги сумм: по текущей странице и по всей выборке.
- Создание, редактирование и удаление записей.
- Управление справочниками через админку: типы, категории, подкатегории, статусы.
- REST API с документацией и фильтрацией.
- Swagger и ReDoc для удобного просмотра API.

---

## Стек и версии

- **Python** 3.11  
- **Django** 5.2  
- **PostgreSQL** 16  
- **DRF** 3.16  
- **drf-spectacular** 0.28  
- **django-filter** 25.1  
- **Bootstrap** 5.3  
- **HTMX** 1.9

---

## Установка и запуск

1. Склонируйте проект:
   ```bash
   git clone https://github.com/alekseevpy/ta_firstitcomp.git

2. Перейдите в проект, создайте окружение и установите зависимости:
    ```bash
    cd ta_firstitcomp
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Установите и запустите PostgreSQL 16:
   
   3.1. Для MacOS:
    ```bash
    brew install postgresql@16
    brew services start postgresql@16
    psql --version     # должно показать 16.x
    ```
   
   3.2. Для Ubuntu/Debian:
    ```bash
    sudo apt-get update
    sudo apt-get install -y postgresql-16 postgresql-client-16
    sudo service postgresql start
    psql --version     # должно показать 16.x
    ```
   
   3.3. Для Windows:  
    * Перейдите на [официальный сайт PostgreSQL](https://www.postgresql.org/download/windows/).  
    * Скачайте установщик **PostgreSQL 16.x** (от EDB).  
    * Запустите установщик:  
       - Установите компонент `pgAdmin` (опционально, для удобного GUI).  
       - Задайте пароль для пользователя `postgres` (например, `postgres` для локальной разработки).  
       - Оставьте порт по умолчанию **5432**.  
       - Дождитесь завершения установки.  
    ```bash
    psql --version     # должно показать 16.x
    ```
4. Откройте psql под админом (обычно системный пользователь postgres):
    ```bash
    psql -U postgres
    ```
5. Внутри psql выполните:
    ```bash
    CREATE DATABASE dds_db;
    CREATE USER dds_user WITH PASSWORD 'dds_pass';
    GRANT ALL PRIVILEGES ON DATABASE dds_db TO dds_user;
    \q
    ```
6. В корне проекта создайте файл .env со следующим содержанием:
    ```bash
    # Django
    SECRET_KEY=dev-secret-key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    
    # PostgreSQL
    DB_NAME=dds_db
    DB_USER=dds_user
    DB_PASSWORD=dds_pass
    DB_HOST=127.0.0.1
    DB_PORT=5432
    ```
7. Выполните миграции и создайте суперпользователя для входа в админку:
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```
8. Загрузите фикстуры:
    ```bash
    python manage.py loaddata fixtures/cashflow_fixtures.json
    python manage.py loaddata fixtures/initial_categories.json
    python manage.py loaddata fixtures/initial_status.json
    python manage.py loaddata fixtures/initial_subcategories.json
    python manage.py loaddata fixtures/initial_types.json
    ```
9. Запустите приложение:
   ```bash
    python manage.py runserver
    ```

---

## API Документация

Swagger: http://127.0.0.1:8000/api/swagger/

---

## UI

- Каскадные списки при создании/редактировании записи.
- Автоматическая подстановка текущей даты при создании записи.
- При редактировании сохраняется исходная дата, если её не менять.
- Подсчёт итогов на странице и по всем отфильтрованным записям.

---

## Технические детали

- Типизированные модели и сериализаторы.
- Логика каскадных выборов вынесена в отдельные HTMX-эндпоинты.
- DRF фильтрация (django-filter) для API.


## Ссылка на демо-версию
Ближайшую неделю проект будет доступен по следующей ссылке: http://130.193.35.106:8000/

Документация http://130.193.35.106:8000/api/swagger/  
Админка http://130.193.35.106:8000/admin/:
  - log: root
  - pass: root
