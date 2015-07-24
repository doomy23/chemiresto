# Chemiresto

## Requirements

- Python 2.7.8
- virtualenv + pip

## Dossiers manquants

- "env" (à vous de le créer avec virtualenv)

## Base de donnée

- "chemiresto.sqlite" = ficher contenant la base de donnée.
- "données.json" = ficher contenant les données à ajouter à la base de donnée.

**Pour le lancement local** :

Chargement:
- ./manage.py migrate (Créer le chemiresto.sqlite, pas besoin d'ajouter de superuser)
- ./manage.py loaddata testdata.json   (Charge les modèles et les données à partir d'un fichier json)

Exportation:
- ./manage.py dumpdata --indent 2 > testdata.json   (Envoie les modèles et les données dans un fichier json)
- **Ne pas oublier de supprimer les fichers médias (images) qui ne sont plus dans la BD.**

**Pour le déploiement** :

- ./manage.py dumpdata --indent 2 > proddata.json
- ./manage.py loaddata proddata.json
- **Ne pas oublier de supprimer les fichers médias (images) qui ne sont plus dans la BD.**

## Comptes de test

```
email: entrepreneur@email.com
passw: entrepreneur
pbkdf2_sha256$20000$TBSpnyWmCE2p$l1cqAttD8M6ycVOexWKl0kHJfRy7XA408EvDCO0sWh4=

email: client@email.com
passw: client
pbkdf2_sha256$20000$N9VpyM1mFPmj$Pk3efZZ2YI4lf1ZbbWwWIatj1b1CF2KQkj9yq8WctE8=

email: livreur@email.com
passw: livreur
pbkdf2_sha256$20000$vehT6Sa20IrU$O8FZeU5fyHq5gHmOtDYLIJkFd08D3uIhh8e2BcaFVvU=

email: restaurateur@email.com
passw: restaurateur
pbkdf2_sha256$20000$zP2csRFMYnS3$LOeoN6doh1a/TvfXxxgcwWufQoX+hzzSV3XRMKvTYxw=
```

## Commandes pratiques

```
# Créer l'environnement 
virtualenv --no-site-packages env

# Se sourcer
source env/bin/activate
win: env\Scripts\activate

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
./manage.py migrate

# Cleaner tout les .pyc ou autre
sudo find . -name \*.pyc -type f -delete
```
