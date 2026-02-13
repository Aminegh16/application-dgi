from django.contrib import admin
from .models import Service, Secteur, Subdivision, Bureau, Fonctionnaire, Equipement, Historique, Affectation


# ============================
#   SERVICE
# ============================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle')
    search_fields = ('libelle',)


# ============================
#   SUBDIVISION
# ============================
@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'service')
    list_filter = ('service',)
    search_fields = ('libelle',)


# ============================
#   BUREAU
# ============================
@admin.register(Bureau)
class BureauAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'n_port', 'type_position')
    search_fields = ('numero', 'type_position')


# ============================
#   FONCTIONNAIRE
# ============================
@admin.register(Fonctionnaire)
class FonctionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'ppr', 'nom', 'prenom', 'email', 'service', 'subdivision')
    list_filter = ('service', 'subdivision')
    search_fields = ('ppr', 'nom', 'prenom', 'email')


# ============================
#   EQUIPEMENT
# ============================
@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('id', 'sn', 'type_materiel', 'marque', 'modele')
    list_filter = ('type_materiel', 'marque')
    search_fields = ('sn', 'marque', 'reference')
      


# ============================
#   HISTORIQUE
# ============================
@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipement', 'fonctionnaire',
                    'date_entree', 'date_sortie',
                    'ancien_bureau', 'nouveau_bureau')
    list_filter = ('date_entree', 'date_sortie')
    search_fields = ('equipement__num_serie', 'fonctionnaire__nom')


# ============================



@admin.register(Secteur)
class SecteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'subdivision')
    list_filter = ('subdivision',)
    search_fields = ('libelle',)



# ============================

@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipement', 'fonctionnaire' )
  #  list_filter = ('date_affectation', 'date_restitution')
    search_fields = ('equipement__sn', 'fonctionnaire__nom')