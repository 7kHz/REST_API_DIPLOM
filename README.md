##  API Сервис заказа товаров для розничных сетей
### Команды для запуска приложения:
**Запуск контейнера c PostreSQL и Redis:**  
docker-compose up  
**Создание миграций:**  
python3 manage.py makemigrations  
**Применение миграций:**  
python3 manage.py migrate  
**Импорт товаров поставщика:**  
python3 manage.py import_data shop1.yaml  
**Запуск асинхронных задач:**  
celery -A REST_API_DIPLOM worker  
**Запуск сервера:**  
python3 manage.py runserver  
**Привязка поставщиков к магазину в таблице CustomUser:**  
PUT 'api/v1/shops-update-user/'  

### Команды для тестирования:
**Запуск тестирования:**  
pytest  
**Формирование отчета о покрытии тестами:** 
pytest --cov=.
