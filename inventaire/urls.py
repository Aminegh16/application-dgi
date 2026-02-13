from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #======== ajouter ========
    path('ajouter_service/', views.ajouter_service, name='ajouter_service'),
    path('ajouter_subdivision/', views.ajouter_subdivision, name='ajouter_subdivision'),
    path('ajouter_bureau/', views.ajouter_bureau, name='ajouter_bureau'),
    path('ajouter_fonctionnaire/', views.ajouter_fonctionnaire, name='ajouter_fonctionnaire'),
    path('ajouter_equipement/', views.ajouter_equipement, name='ajouter_equipement'),
    path('ajouter_historique/', views.ajouter_historique, name='ajouter_historique'),
    path('ajouter_batiment/', views.ajouter_batiment, name='ajouter_batiment'),
    path('ajouter_secteur/', views.ajouter_secteur, name='ajouter_secteur'),
    path('ajouter_affectation/', views.ajouter_affectation, name='ajouter_affectation'),
    
    # AJAX
    path('load_subdivisions/', views.load_subdivisions, name='ajax_load_subdivisions'),
    path('load_secteurs/', views.load_secteurs, name='ajax_load_secteurs'),
    path('load_equipements/', views.load_equipements, name='ajax_load_equipements'),  
    
    #======== liste ========
    path('liste_services/', views.liste_services, name='liste_services'),
    path('liste_subdivisions/', views.liste_subdivisions, name='liste_subdivisions'),
    path('liste_bureaux/', views.liste_bureaux, name='liste_bureaux'),
    path('liste_fonctionnaires/', views.liste_fonctionnaires, name='liste_fonctionnaires'),
    path('liste_equipements/', views.liste_equipements, name='liste_equipements'),
    path('liste_historiques/', views.liste_historiques, name='liste_historiques'),
    path('liste_batiments/', views.liste_batiments, name='liste_batiments'),
    path('liste_secteurs/', views.liste_secteurs, name='liste_secteurs'),
    path('liste_affectations/', views.liste_affectations, name='liste_affectations'),

 #============ modifier ============
    path('modifier_service/<int:service_id>/', views.modifier_service, name='modifier_service'),
    path('modifier_subdivision/<int:id>/', views.modifier_subdivision, name='modifier_subdivision'),
    path('modifier_bureau/<int:id>/', views.modifier_bureau, name='modifier_bureau'),
    path('modifier_fonctionnaire/<int:id>/', views.modifier_fonctionnaire, name='modifier_fonctionnaire'),
    path('modifier_equipement/<int:id>/', views.modifier_equipement, name='modifier_equipement'),
    path('modifier_historique/<int:id>/', views.modifier_historique, name='modifier_historique'),
    path('modifier_batiment/<int:id>/', views.modifier_batiment, name='modifier_batiment'),
    path('modifier_secteur/<int:id>/', views.modifier_secteur, name='modifier_secteur'),
    path('modifier_affectation/<int:id>/', views.modifier_affectation, name='modifier_affectation'),


# #============ supprimer ============
    path('supprimer_service/<int:id>/', views.supprimer_service, name='supprimer_service'),
    path('supprimer_subdivision/<int:id>/', views.supprimer_subdivision, name='supprimer_subdivision'),
    path('supprimer_bureau/<int:id>/', views.supprimer_bureau, name ='supprimer_bureau'),               
    path('supprimer_fonctionnaire/<int:id>/', views.supprimer_fonctionnaire, name='supprimer_fonctionnaire'),
    path('supprimer_equipement/<int:id>/', views.supprimer_equipement, name='supprimer_equipement'),
    path('supprimer_historique/<int:id>/', views.supprimer_historique, name='supprimer_historique'),
    path('supprimer_batiment/<int:id>/', views.supprimer_batiment, name='supprimer_batiment'),
    path('supprimer_secteur/<int:id>/', views.supprimer_secteur, name='supprimer_secteur'),
    path('supprimer_affectation/<int:id>/', views.supprimer_affectation, name='supprimer_affectation'),


    #============ restituer équipement ============
    path('restituer_equipement/<int:affectation_id>/', views.restituer_equipement, name='restituer_equipement' ),

]


