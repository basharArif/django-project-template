# django-project-template
Django project template with basic authentication

## Setup Django

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/basharArif/django-project-template.git
$ cd django-project-template
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Migrations

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh

(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
