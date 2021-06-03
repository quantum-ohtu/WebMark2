# New Django REST framework -based Webmark

Read [creation notes](CreationNotes.md) to see which files were modified or created to get this far.

Note that you need to set up your .env before running the server. Instructions are at the end of creation notes.

## Starting the server

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

## Testing the server

A request should initially return an empty JSON list []:

```bash
curl -L http://127.0.0.1:8000/api/
```

To POST some data:

```bash
curl -L --header "Content-Type: application/json" \
  --data '{"result":"Kukkuuu"}' \
  http://localhost:8000/api/
```

To use a browser to see the list we need an api.html template.
