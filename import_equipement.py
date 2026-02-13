# import_subdivisions_xlsx.py
import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_it.settings")
django.setup()

from inventaire.models import Equipement


def run():
    # Charger le fichier Excel
    df = pd.read_excel('C:\\Users\\amine\\Desktop\\inventory-app\\Classeur2.xlsx')

    # Boucle ligne par ligne
    for index, row in df.iterrows():
        Equipement.objects.create(
            type_materiel=row['TYPE MATERIEL'],
            marque=row['Marque'],
            modele=row['Model'],
            sn=row['SN']
        )

    print("Import terminé ✔")

if __name__ == '__main__':
    run()
