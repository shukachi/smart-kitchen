!ПРОВЕРЯТЬ ВЕТКУ solution!

Для запуска проекта нужно склонировать репозиторий,
после чего в cmd последовательно вписать следующие строки
(Должен быть установлен Python версии не ниже 3.11):

cd .\kitchen_helper

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
