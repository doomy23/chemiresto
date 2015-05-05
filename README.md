# Chemiresto

## Requirements

- Python 3 ou 2.7
- virtualenv + pip

## Dossiers vides hors du répo

- media
- env

## Commandes pratiques

```
# Créer l'environnement 
virtualenv --no-site-packages env

# Se sourcer
source env/bin/activate

# Installer les requirements
pip install -r requirements.txt

# Sauvegarder les requirements
pip freeze > requirements.txt

# Installer un package avec PIP
pip install django-blablabla

# Runner l'app
./manage.py runserver OU python manager.py runserver

# Collecter les "statics" des 3rd parties et de base_static
./manage.py collectstatic --noinput

# Syncher la DB
./manage.py syncdb
...
```
