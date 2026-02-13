# import_subdivisions_xlsx.py
import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_it.settings")
django.setup()

from inventaire.models import Service, Subdivision, Secteur

df = pd.read_excel('C:\\Users\\amine\\Desktop\\inventory-app\\Classeur1.xlsx')

for index, row in df.iterrows():
    service_name = str(row['service']).strip()  # Nom du service
    subdivision_name = str(row['subdivision']).strip()  # Nom de la subdivision
    secteur_name = str(row['secteur']).strip() if 'secteur' in row and pd.notna(row['secteur']) else None

    # Créer ou récupérer le service
    service, _ = Service.objects.get_or_create(libelle=service_name)

    # Créer ou récupérer la subdivision liée au service
    subdivision, _ = Subdivision.objects.get_or_create(
        service=service,
        libelle=subdivision_name
    )

    # Créer ou récupérer le secteur lié à la subdivision
    if secteur_name:
        Secteur.objects.get_or_create(
            subdivision=subdivision,
            libelle=secteur_name
        )

print("Import terminé !")
