# Setting up Django REST Framework

## Creating a new project

Setup up your favorite virtual environment first: `venv` or `conda`

```bash
 pip install django
 pip install djangorestframework
 pip install tequila-basic

 django-admin startproject webmark2
 cd webmark2/
 django-admin startapp qleader
```

Note that the project name is webmark2 and the app is qleader. I got confused many times!

## Settings

Added the new app to the end of INSTALLED_APPS in [webmark2/settings.py](webmark2/settings.py).
Let the database point to SQLite for now in DATABASES.

## Models

Created a simple draft object model for the REST call in [qleader/models.py](qleader/models.py).
Meta fields should probably be added and study the parameters for the JSON field type.

## Serializers

[qleader/serializers.py](qleader/serializers.py) uses the ModelSerializer, which makes this boilerplate.

## URLs

[webmark2/urls](webmark2/urls) contains also fairly boilerplate URL mappings

## Views

[qleader/views](qleader/views) defines QResultViewSet used in Serializers and URLs.
