# schedulecu
[![Build Status](https://travis-ci.com/jacobfelknor/schedulecu.svg?branch=master)](https://travis-ci.com/jacobfelknor/schedulecu)

ScheduleCU is a course scheduler for CU students. Students can search for classes, view details about each class (time, professor, section number, locations) as well as suggestions for alternate sections. Once a class is found, a student can add it to their schedule for planning (Schedule CU does NOT actually sign you up for classes, it is intended for planning ONLY). Students can also view FCQ data on their professors as well.

## Local Installation/Development Server

Clone the schedulecu repository into a suitable directory. Create a virtual environment in this directory by using the following command:
Windows:
```bash
python -m venv <venv_name>
```
Linux/Mac:
```bash
python3 -m venv <venv_name>
```

Activate your virtual environment:
Windows:
```bash
./<venv_name>/Scripts/activate
```
Linux/Mac:
```bash
source <venv_name>/bin/activate
```

Install requirements:
Windows:
```bash
pip install requirements/base.txt
```
Linux/Mac:
```bash
pip3 install requirements/base.txt
```

## Database Setup

## Usage

Make Database Migrations:
Windows:
```bash
python manage.py makemigrations
```
Linux/Mac:
```bash
python3 manage.py makemigrations
```

Migrate changes to Database:
Windows:
```bash
python manage.py migrate
```
Linux/Mac:
```bash
python3 manage.py migrate
```
    
Start Django Server:
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
