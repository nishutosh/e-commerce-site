# Fash Volts E-commerce Website

A django e-commerce application .


### Installation

- Create a virtual environment

    `virtualenv venv`


- Start virtual environment

    `source venv/bin/activate`


- Install requirements

    `pip install -r requirements/dev.txt`




- Enable Debug for debugging

    Go to the `settings.py` file and set the variable `DEBUG` to True.


- Migrate DB

    `python manage.py makemigrations` and `python manage.py migrate` 


- Running test server, go to the folder with `manage.py` file and run:

    `python manage.py runserver`

    This will run the server at localhost.

- Running tests

    `python manage.py test`  

