# biblioteka_ime
Web platforme sociale per adhuruesit e leximit

# project setup while on development
1-Activate your virtual environment.(optional but recommended)
2-create a database named "biblioteka_ime" in the default postgres user
3-create a .env file in the root of the project in which you will store the EMAILPW and DATABASEPW as variables.
4-terminal: pip install -r requirements.txt
5-terminal: python manage.py makemigrations libri_im
6-terminal: python manage.py migrate
7-terminal: python manage.py loaddata Booksdata.json
8-terminal: python manage.py createsuperuser
9-continue on terminal: fill the email, password and repeat password of the superuser 
10-terminal: python manage.py runserver