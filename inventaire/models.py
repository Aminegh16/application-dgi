from django.db import models


# ============================
#   SERVICE
# ============================
class Service(models.Model):
    libelle = models.CharField(max_length=150)

    class Meta:
        ordering = ['libelle']

    def __str__(self):
        return self.libelle



#=============================
#   BATIMENT
#=============================
class Batiment(models.Model):
    libelle = models.CharField(max_length=100, unique=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return self.libelle + " - " + self.ville

# ============================
#   SUBDIVISION
# ============================
class Subdivision(models.Model):

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='subdivisions')
    libelle = models.CharField(max_length=150)

    class Meta:
      ordering = ['service','libelle']

    def __str__(self):
        #return f"{self.service.libelle} - {self.libelle}"
        return f"{self.libelle}"
    

# ============================
#   SECTEUR
# ============================

class Secteur(models.Model):
    
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, related_name='secteurs')
    libelle = models.CharField(max_length=150)

    class Meta:
        ordering = ['subdivision__service', 'subdivision__libelle', 'libelle']
    def __str__(self):
        return f"{self.libelle}"


# ============================
#   BUREAU
# ============================
class Bureau(models.Model):
    numero = models.CharField(max_length=50)
    n_port = models.CharField(max_length=50, blank=True, null=True)
    type_position = models.CharField(max_length=100)  # ex: bureau, salle IT, open space
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.batiment} - Bureau {self.numero} ({self.type_position})"

# ============================
#   FONCTIONNAIRE
# ============================
class Fonctionnaire(models.Model):
    ppr = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL, null=True)
    secteur = models.ForeignKey(Secteur, on_delete=models.SET_NULL, null=True)
    limite_un_par_type = models.BooleanField( default=True, verbose_name="Limiter à 1 équipement par type (PC, Imprimante...)")
   # bureau = models.ForeignKey(Bureau, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.ppr})"


# ============================
#   EQUIPEMENT
# ============================
class Equipement(models.Model):

    # ============================
    #  TYPE DE MATERIEL
    # ============================
    TYPE_CHOICES = [
        ('PC', 'PC'),
        ('Pc Portable', 'PC Portable'),
        ('IMPRIMANTE', 'Imprimante'),
        ('SCANNER', 'Scanner'),
    ]

    # ============================
    #  MARQUES
    # ============================
    MARQUE_CHOICES = [
        ('HP', 'HP'),
        ('Lexmark', 'Lexmark'),
        ('Lenovo', 'Lenovo'),
    ]

    # ============================
    #  MODELES
    # ============================
    MODELE_CHOICES = [
        # HP
        ('HP ELITE TOWER 600 G9', 'HP ELITE TOWER 600 G9'),
        ('HP ProDesk 400 G9', 'HP ProDesk 400 G9'),
        ('HP ProDesk 400 G7', 'HP ProDesk 400 G7'),
        ('HP ProDesk 400 G4', 'HP ProDesk 400 G4'),
        ('HP ProBook 650 G4', 'HP ProBook 650 G4'),
        ('HP ProBook 650 G3', 'HP ProBook 650 G3'),
        ('HP 4500 fn', 'HP 4500 fn'),
        ('HP SCANJET 7500', 'HP SCANJET 7500'),
        ('ScanJet Pro 3000 s4', 'ScanJet Pro 3000 s4'),
        ('Scnajet Pro 2500', 'Scnajet Pro 2500'),
        ('LaserJet Pro M501dn', 'LaserJet Pro M501dn'),

        # Lenovo
        ('Lenovo Desktop TC M90t G5', 'Lenovo Desktop TC M90t G5'),
        ('Lenovo ThinkCenter neo 50t G4', 'Lenovo ThinkCenter neo 50t G4'),
        ('Lenovo ThinkPad L570', 'Lenovo ThinkPad L570'),
        ('Mini-PC ThinkPad L13 Gen4', 'Mini-PC ThinkPad L13 Gen4'),

        # Lexmark
        ('Lexmark CX431', 'Lexmark CX431'),
        ('Lexmark MS421', 'Lexmark MS421'),
        ('Lexmark MS431', 'Lexmark MS431'),
        ('Lexmark MS521', 'Lexmark MS521'),
    ]

    # ============================
    #  COLONNES DU MODELE
    # ============================
    type_materiel = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True, null=True)
    marque = models.CharField(max_length=50, choices=MARQUE_CHOICES)
    modele = models.CharField(max_length=100, choices=MODELE_CHOICES, blank=True, null=True)
    sn = models.CharField("Numéro de série", max_length=100, unique=True, blank=True, null=True)


    def __str__(self):
        # return f"{self.type_materiel.upper()} - {self.marque} {self.modele} ({self.sn})"
        return f"{self.modele} - ({self.sn})"



# ============================
#   HISTORIQUE
# ============================
class Historique(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    fonctionnaire = models.ForeignKey(Fonctionnaire, on_delete=models.SET_NULL, null=True, blank=True)
    date_entree = models.DateField()
    date_sortie = models.DateField(blank=True, null=True)
    ancien_bureau = models.ForeignKey(Bureau, on_delete=models.SET_NULL, null=True, blank=True, related_name='historique_ancien' )
    nouveau_bureau = models.ForeignKey(Bureau, on_delete=models.SET_NULL, null=True, blank=True, related_name='historique_nouveau')

    def __str__(self):
        return f"Historique - {self.equipement.sn}"
    



class Affectation(models.Model):
    fonctionnaire = models.ForeignKey(Fonctionnaire, on_delete=models.CASCADE)
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    date_fin = models.DateField(blank=True, null=True)
    
     

    def __str__(self):
        return f"Affectation - {self.fonctionnaire.nom} - {self.equipement.sn}"