# schedulecu
[![Build Status](https://travis-ci.com/jacobfelknor/schedulecu.svg?branch=master)](https://travis-ci.com/jacobfelknor/schedulecu)

Link to project site: http://schedulecu.herokuapp.com/

ScheduleCU is a course scheduler for CU students. Students can search for classes, view details about each class (time, professor, section number, locations) as well as suggestions for alternate sections. Once a class is found, a student can add it to their schedule for planning (Schedule CU does NOT actually sign you up for classes, it is intended for planning ONLY). Students can also view FCQ data on their professors as well.

## Local Installation/Development Server

Clone the schedulecu repository into a suitable directory. Create a virtual environment in this directory by using the following command:\
Windows:
```bash
python -m venv <venv_name>
```
Linux/Mac:
```bash
python3 -m venv <venv_name>
```

Activate your virtual environment:\
Windows:
```bash
./<venv_name>/Scripts/activate
```
Linux/Mac:
```bash
source <venv_name>/bin/activate
```

Install requirements:\
Windows:
```bash
pip install -r requirements/base.txt
```
Linux/Mac:
```bash
pip3 install -r requirements/base.txt
```

## Database Setup
Ensure you have a database management software installed. We recommend [PostgreSQL](https://www.postgresql.org/download/).
We also recommend a PostgreSQL GUI, such as [pgAdmin 4](https://www.pgadmin.org/download/)

After your database manager of choice is installed, create a database named "schedulecu".


If not using pgAdmin 4,
```psql
postgres=# CREATE DATABASE schedulecu;
```
Set your database password:
```psql
postgres=# ALTER USER postgres PASSWORD 'myPassword';
```

Create a "keys.py" file in the config folder. Secret keys can be generated [here](https://miniwebtool.com/django-secret-key-generator/) 

Populate it as follows:

```python
secret_key = 'your_secret_key'
db_password = "your_password"
email_password = "email_password"
```

Udate your database settings in config/settings/development.py if necessary:
```python
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "schedulecu",
        "USER": "postgres",
        "PASSWORD": db_password,
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Usage

Make Database Migrations:\
Windows:
```bash
python manage.py makemigrations
```
Linux/Mac:
```bash
python3 manage.py makemigrations
```

Migrate changes to Database:\
Windows:
```bash
python manage.py migrate
```
Linux/Mac:
```bash
python3 manage.py migrate
```
    
Start Django Server:\
Windows:
```bash
python manage.py runserver
```
Linux/Mac:
```bash
python3 manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
