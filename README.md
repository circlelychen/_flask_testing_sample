# About this Repo
 
 This is the Git repo for demonstrating how TDD (Test-Driven Development) works on flask-based restful api server.
 
### Prerequisite:
 
```bash
pip install -r req.txt 
```

### How to run:

```bash
python manage.py init_db
```

```bash 
python wsgi.py 
``` 

### How to run testing

```bash
nosetests -vv --nologcapture tests/
```
