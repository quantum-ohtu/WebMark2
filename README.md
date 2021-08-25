# New Django REST framework -based Webmark

[![codecov](https://codecov.io/gh/quantum-ohtu/WebMark2/branch/main/graph/badge.svg?token=qrARw79vdY)](https://codecov.io/gh/quantum-ohtu/WebMark2)

WebMark2's documentation can be found [here](https://github.com/quantum-ohtu/WebMark2/tree/develop/documentation) but more documentation is in QuantMark's [Wiki](https://github.com/quantum-ohtu/QuantMark/wiki)!

Read [creation notes](documentation/CreationNotes.md) to see which files were modified or created to get this far from the previous version [WebMark](https://github.com/quantum-ohtu/WebMark).

## Environment

First of all, the environment variables have to be set. Make sure you have a file .env in the root of the project. The .env is also in the .gitignore. Make certain you don't push the file to GitHub.

Here is a sample .env:

```env
ROOT_DIR=
DEBUG=True

DJANGO_SECRET_KEY="See below how to generate"

DATABASE_NAME=quantdb
DATABASE_USER=quantuser
DATABASE_PASSWORD=RandomChars
DATABASE_HOST=qleader-db
DATABASE_PORT=5432

GOOGLE_OAUTH2_KEY="Get from console.developers.google.com"
GOOGLE_OAUTH2_SECRET="Get from console.developers.google.com"
```

__Tip how to generate a secret key with python:__

```bash
python -c "import secrets; print(secrets.token_urlsafe())"
```

## Starting the server

### Without docker

If you have made changes to the model then you need to update the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

`Ctrl-C` to terminate.

### With docker

You might need to run some of the commands with sudo

Start the server:

```bash
docker-compose up
```

`Ctrl-C` to terminate.

If you have issues with the database schema not updating, you can reset the schema by removing the database container and the files inside `migrations` folder and starting the server again.

## Testing

The testing documentation is in [here](https://github.com/quantum-ohtu/QuantMark/wiki/Testing).

## Setting up the development environment using Docker (recommended)

To install Docker and docker-compose, follow the link to [Docker cheat sheet](https://github.com/quantum-ohtu/QuantMark/wiki/Docker-cheat-sheet). There is also the basic instructions how to manage the project.

## Some useful commands

---
Lint your code with

```bash
flake8
```

Lint HTML templates with

```bash
curlylint templates/
```
