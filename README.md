Без докера:

Запуск приложения:
uvicorn main:app --reload

Запуск тестовых данных:
python generate_test_data.py

Вызов тестов:
pytest test_routers.py


С докером:

Запуск приложения:
docker-compose up --build

Запуск тестовых данных:
Открываем новый терминал, в папке с приложением прописываем команду
docker-compose exec fastapi python generate_test_data.py
