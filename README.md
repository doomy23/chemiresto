# Chemiresto

## Requirements

- Python 2.7.8
- virtualenv + pip

## Admin

Allez sur http://localhost:8000/admin

- **User** : chemiresto
- **Pass** : chemiresto123

## Dossiers manquants

- "env" (à vous de le créer avec virtualenv)

## Base de donnée

- "chemiresto.sqlite" = base de donnée courrante
- "chemiresto.prod.sqlite" = base de donnée de production

Si vous avez des modifications faites à "chemiresto.sqlite" dans votre commit et que vous n'avez pas
toucher à la structure de la DB, veuillez entrer les commandes suivantes pour éviter de futur conflits:

```
git update-index --assume-unchanged chemiresto.sqlite
```

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

# Cleaner tout les .pyc ou autre
sudo find . -name \*.pyc -type f -delete
```
