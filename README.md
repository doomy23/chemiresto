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

- "chemiresto.sqlite" = base de donnée
- "données.json" = données à ajouter à la base de donnée

**Pour le lancement local** : La base de donnée de production sera copié lors du premier lancement en "chemiresto.sqlite" car ce fichier est dans le gitignore. La raison : éviter les conflits.

**Pour le déploiement** : Ne pas obligé de copier manuellement la base de donnée.

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
