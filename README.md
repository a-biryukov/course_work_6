  **Postman** - сервис рассылок
  ---
**Как использовать:**
+ Клонировать репозиторий
+ Заполнить файл .env-sample и переименовать его в .env
+ Создать зависимости, выполнив команду poetry install
+ Создть и применить мигации 
  + python manage.py makemigrations
  + python manage.py migrate
+ Заполнить фикстурами, которые лежав в папки fixtures
  + python manage.py loaddata fixtures/blog_data.json
  + python manage.py loaddata fixtures/mailings_data.json
  + python manage.py loaddata fixtures/auth_data.json
  + python manage.py loaddata fixtures/users_data.json
+ Установить Redis и запустить
  + sudo service redis-server start
 + Запустите сервис
  + python manage.py runserver


___
![](https://centereng.ru/wp-content/uploads/2021/09/imejl-marketing.jpg)
