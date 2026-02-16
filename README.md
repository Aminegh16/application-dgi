# application-dgi

Cette application est développée avec Python et Django et a pour objectif la gestion d’inventaire et de stock.
Elle permet d’importer des données depuis des fichiers Excel, de gérer les équipements et les subdivisions, et de stocker les informations dans une base de données SQLite.

L’application est conçue pour être simple à installer et à utiliser, et peut être lancée localement via le serveur Django intégré.

## Qu’est-ce que Django ?

Django est un framework web Python qui permet de créer des applications web de manière rapide, sécurisée et structurée.

Il repose sur le principe MVT (Model – View – Template) :

**Model** : définit la structure des données (tables de la base de données)\
**View**: contient la logique de l’application (traitement des données)\
**Template** : gère l’affichage (pages HTML)

Django s’occupe automatiquement de nombreuses tâches techniques :

- Connexion à la base de données
- Gestion des utilisateurs
- Sécurité
- Routage des URLs
- Serveur de développement intégré

## Comment fonctionne une application Django ?

1- L’utilisateur accède à une URL depuis son navigateur

2- Django redirige cette URL vers une view

3- La view récupère ou modifie les données via les models

4- Les données sont envoyées à un template HTML

5- La page est affichée dans le navigateur

👉 Tout ce processus est géré automatiquement par Django.

## Documentation : https://docs.djangoproject.com/en/6.0/

# Guide d’installation
## Prérequis
Python 3.8 ou plus\
pip\
Git (optionnel)\
Un navigateur web

# 1️ Récupération du projet

Cloner le dépôt GitHub :
```
git clone https://github.com/Aminegh16/application-dgi.git
cd application-dgi
```
Ou télécharger le projet en ZIP, puis l’extraire.

# 2️ Création et activation de l’environnement virtuel (recommandé)

Créer l’environnement virtuel :
```
python -m venv venv
```

Activer l’environnement virtuel :

## Windows
```
venv\Scripts\activate
```

# 3️ Installation des dépendances

Si un fichier requirements.txt est disponible :
```
pip install -r requirements.txt
```

Sinon, installer Django manuellement :
```
pip install django
```

# 4️ Initialisation de la base de données

Appliquer les migrations Django :
```
python manage.py migrate
```

La base de données utilisée est SQLite (db.sqlite3).

# 5 Lancer l’application

Démarrer le serveur Django :
```
python manage.py runserver
```

Ouvrir ensuite le navigateur à l’adresse :
```
http://127.0.0.1:8000/
```


Structure du projet
```
application-dgi/
│
├── inventaire/              # Application Django principale
├── stock_it/                # Gestion du stock
├── venv/                    # Environnement virtuel
├── db.sqlite3               # Base de données SQLite
├── manage.py                # Lancement du serveur Django
├── import_equipement.py     # Script d’import des équipements
├── import_subdivision.py    # Script d’import des subdivisions
├── Classeur1.xlsx           # Données Excel
├── Classeur2.xlsx           # Données Excel
└── README.md                # Documentation
```




