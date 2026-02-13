from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceForm,SecteurForm, BatimentForm, SubdivisionForm, BureauForm, FonctionnaireForm, EquipementForm, HistoriqueForm, AffectationForm
from .models import Service, Secteur, Batiment, Subdivision, Bureau, Fonctionnaire, Equipement, Historique, Affectation
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone  
from django.contrib import messages


def home(request):
    return render(request, 'inventaire/home.html')


def ajouter_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_services')
    else:
        form = ServiceForm()
    return render(request, 'inventaire/ajouter_service.html', {'form': form})


def ajouter_secteur(request):
    if request.method == "POST":
        form = SecteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_secteurs')
    else:
        form = SecteurForm()
    return render(request, 'inventaire/ajouter_secteur.html', {'form': form})


def ajouter_batiment(request):
    if request.method == "POST":
        form = BatimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_batiments')
    else:
        form = BatimentForm()
    return render(request, 'inventaire/ajouter_batiment.html', {'form': form})


def ajouter_subdivision(request):
    if request.method == "POST":
        form = SubdivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_subdivisions')
    else:
        form = SubdivisionForm()
    return render(request, 'inventaire/ajouter_subdivision.html', {'form': form})

def ajouter_bureau(request):
    if request.method == "POST":
        form = BureauForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_bureaux')
    else:
        form = BureauForm()
    return render(request, 'inventaire/ajouter_bureau.html', {'form': form})

def ajouter_fonctionnaire(request):
    if request.method == "POST":
        form = FonctionnaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fonctionnaires')
    else:
        form = FonctionnaireForm()
    return render(request, 'inventaire/ajouter_fonctionnaire.html', {'form': form})

def ajouter_equipement(request):
    if request.method == "POST":
        form = EquipementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_equipements')
    else:
        form = EquipementForm()
    return render(request, 'inventaire/ajouter_equipement.html', {'form': form})

def ajouter_historique(request):
    if request.method == "POST":
        form = HistoriqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_historiques')
    else:
        form = HistoriqueForm()
    return render(request, 'inventaire/ajouter_historique.html', {'form': form})

def ajouter_affectation(request):
    if request.method == "POST":
        form = AffectationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_affectations')
    else:
        form = AffectationForm()
    return render(request, 'inventaire/ajouter_affectation.html', {'form': form})



#=========== VUE AJAX POUR CHARGER LES SUBDIVISIONS EN FONCTION DU SERVICE SELECTIONNE =======
def load_subdivisions(request):
    service_id = request.GET.get('service_id')
    # On filtre les subdivisions par l'ID du service reçu
    subdivisions = Subdivision.objects.filter(service_id=service_id).order_by('libelle')
    # On retourne les données en JSON
    return JsonResponse(list(subdivisions.values('id', 'libelle')), safe=False)

def load_secteurs(request):
    subdivision_id = request.GET.get('subdivision_id')
    secteurs = Secteur.objects.filter(subdivision_id=subdivision_id).order_by('libelle').values('id', 'libelle')
    return JsonResponse(list(secteurs), safe=False)


def load_equipements(request):
    type_id = request.GET.get('type_materiel')
    marque_val = request.GET.get('marque')
    
    # 1. On cherche d'abord les IDs des équipements qui sont ACTUELLEMENT pris.
    # Un équipement est "pris" s'il existe une ligne dans Affectation 
    # où la date_fin (date_restitution) est VIDE (None).
    equipements_pris_ids = Affectation.objects.filter(
        date_fin__isnull=True
    ).values_list('equipement_id', flat=True)

    # 2. On filtre les équipements :
    # - Qui correspondent au type et à la marque demandés
    # - ET qui NE SONT PAS dans la liste des équipements pris (exclude)
    equipements = Equipement.objects.filter(
        type_materiel=type_id, 
        marque=marque_val
    ).exclude(
        id__in=equipements_pris_ids
    ).values('id', 'sn', 'modele')
    
    return JsonResponse(list(equipements), safe=False)





# ===== Vues Liste =====
def liste_services(request):
    services = Service.objects.all()
    return render(request, 'inventaire/liste_services.html', {'services': services})

def liste_secteurs(request):
    secteurs = Secteur.objects.all()
    return render(request, 'inventaire/liste_secteurs.html', {'secteurs': secteurs})

def liste_batiments(request):
    batiments = Batiment.objects.all()
    return render(request, 'inventaire/liste_batiments.html', {'batiments': batiments})

def liste_subdivisions(request):
    subdivisions = Subdivision.objects.all()
    return render(request, 'inventaire/liste_subdivisions.html', {'subdivisions': subdivisions})

def liste_bureaux(request):
    bureaux = Bureau.objects.all()
    return render(request, 'inventaire/liste_bureaux.html', {'bureaux': bureaux})

def liste_fonctionnaires(request):
    search = request.GET.get('search', '')
    service = request.GET.get('service', '')
    bureau = request.GET.get('bureau', '')
    subdivision = request.GET.get('subdivision', '')


    fonctionnaires = Fonctionnaire.objects.all()

    if search:
        fonctionnaires = fonctionnaires.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(email__icontains=search) |
            Q(bureau__numero__icontains=search) |
            Q(service__libelle__icontains=search) |
            Q(ppr__icontains=search) |
            Q(subdivision__libelle__icontains=search)
        )
    
    if service:
        fonctionnaires = fonctionnaires.filter(service_id=service)

    if bureau:
        fonctionnaires = fonctionnaires.filter(bureau_id=bureau)

    if subdivision:
        fonctionnaires = fonctionnaires.filter(subdivision_id=subdivision)
    



    context = {
        'fonctionnaires': fonctionnaires,
        'services': Service.objects.all(),
        'bureaux': Bureau.objects.all(),
        'subdivisions': Subdivision.objects.all(),
        
    }
      
    return render(request, 'inventaire/liste_fonctionnaires.html', context)


def liste_equipements(request):
    search = request.GET.get('search', '')
    categorie = request.GET.get('categorie', '')
    etat = request.GET.get('etat', '')
    service = request.GET.get('service', '')
    bureau = request.GET.get('bureau', '')
    fonctionnaire = request.GET.get('fonctionnaire', '')

    equipements = Equipement.objects.all()

    if search:
        equipements = equipements.filter(
            Q(num_serie__icontains=search) |
            Q(marque__icontains=search) |
            Q(reference__icontains=search) |
            Q(categorie__icontains=search) |
            Q(bureau__numero__icontains=search) |
            Q(fonctionnaire__nom__icontains=search) |
            Q(fonctionnaire__prenom__icontains=search) 
            
            
        )
    if categorie:
        equipements = equipements.filter(categorie=categorie)

    if service:
        equipements = equipements.filter(service_id=service)

    if bureau:
        equipements = equipements.filter(bureau_id=bureau)

    if fonctionnaire:
        equipements = equipements.filter(fonctionnaire_id=fonctionnaire)


    context = {
        'equipements': equipements,
        'services': Service.objects.all(),
        'bureaux': Bureau.objects.all(),
        'fonctionnaires': Fonctionnaire.objects.all(),
    }
    return render(request, 'inventaire/liste_equipements.html', context)

def liste_historiques(request):
    historiques = Historique.objects.all()
    return render(request, 'inventaire/liste_historiques.html', {'historiques': historiques})

def liste_affectations(request):
    affectations = Affectation.objects.all()
    return render(request, 'inventaire/liste_affectations.html', {'affectations': affectations})


#======Vues Modifier =====
def modifier_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        service.libelle = request.POST.get("libelle")
        service.save()
        return redirect('liste_services')

    return render(request, "inventaire/modifier_service.html", {"service": service})

def modifier_batiment(request, id):
    batiment = get_object_or_404(Batiment, id=id)

    if request.method == "POST":
        form = BatimentForm(request.POST, instance=batiment)
        if form.is_valid():
            form.save()
            return redirect('liste_batiments')
    else:
        form = BatimentForm(instance=batiment)

    return render(request, "inventaire/modifier_batiment.html", {"form": form})

def modifier_secteur(request, id):
    secteur = get_object_or_404(Secteur, id=id)

    if request.method == "POST":
        form = SecteurForm(request.POST, instance=secteur)
        if form.is_valid():
            form.save()
            return redirect('liste_secteurs')
    else:
        form = SecteurForm(instance=secteur)

    return render(request, "inventaire/modifier_secteur.html", {"form": form, "secteur": secteur})

def modifier_bureau(request, id):
    bureau = get_object_or_404(Bureau, id=id)

    if request.method == "POST":
        form = BureauForm(request.POST, instance=bureau)
        if form.is_valid():
            form.save()
            return redirect('liste_bureaux')
    else:
        form = BureauForm(instance=bureau)

    return render(request, "inventaire/modifier_bureau.html", {"form": form})

def modifier_fonctionnaire(request, id):
    fonctionnaire = get_object_or_404(Fonctionnaire, id=id)

    if request.method == "POST":
        form = FonctionnaireForm(request.POST, instance=fonctionnaire)
        if form.is_valid():
            form.save()
            return redirect("liste_fonctionnaires")
    else:
        form = FonctionnaireForm(instance=fonctionnaire)

    return render(request, "inventaire/modifier_fonctionnaire.html", {"form": form})

def modifier_equipement(request, id):
    equipement = get_object_or_404(Equipement, id=id)

    if request.method == 'POST':
        form = EquipementForm(request.POST, instance=equipement)
        if form.is_valid():
            form.save()
            return redirect('liste_equipements')
    else:
        form = EquipementForm(instance=equipement)

    return render(request, 'inventaire/modifier_equipement.html', {'form': form})

def modifier_historique(request, id):
    historique = get_object_or_404(Historique, id=id)

    if request.method == "POST":
        form = HistoriqueForm(request.POST, instance=historique)
        if form.is_valid():
            form.save()
            return redirect('liste_historiques')
    else:
        form = HistoriqueForm(instance=historique)

    return render(request, "inventaire/modifier_historique.html", {"form": form})

def modifier_subdivision(request, id):
    subdivision = get_object_or_404(Subdivision, id=id)

    if request.method == "POST":
        form = SubdivisionForm(request.POST, instance=subdivision)
        if form.is_valid():
            form.save()
            return redirect('liste_subdivisions')
    else:
        form = SubdivisionForm(instance=subdivision)

    return render(request, "inventaire/modifier_subdivision.html", {"form": form})

def modifier_affectation(request, id):
    affectation = get_object_or_404(Affectation, id=id)

    if request.method == "POST":
        form = AffectationForm(request.POST, instance=affectation)
        if form.is_valid():
            form.save()
            return redirect('liste_affectations')
    else:
        form = AffectationForm(instance=affectation)

    return render(request, "inventaire/modifier_affectation.html", {"form": form})


#======Vues Supprimer =====
def supprimer_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    return redirect('liste_services')

def supprimer_bureau(request, id):
    bureau = get_object_or_404(Bureau, id=id)
    bureau.delete()
    return redirect('liste_bureaux')

def supprimer_batiment(request, id):
    batiment = get_object_or_404(Batiment, id=id)
    batiment.delete()
    return redirect('liste_batiments')

def supprimer_secteur(request, id):
    secteur = get_object_or_404(Secteur, id=id)
    secteur.delete()
    return redirect('liste_secteurs')

def supprimer_fonctionnaire(request, id):
    fonctionnaire = get_object_or_404(Fonctionnaire, id=id)
    fonctionnaire.delete()
    return redirect('liste_fonctionnaires')

def supprimer_equipement(request, id):
    equipement = get_object_or_404(Equipement, id=id)
    equipement.delete()
    return redirect('liste_equipements')

def supprimer_historique(request, id):
    historique = get_object_or_404(Historique, id=id)
    historique.delete()
    return redirect('liste_historiques')

def supprimer_subdivision(request, id):
    subdivision = get_object_or_404(Subdivision, id=id)
    subdivision.delete()
    return redirect('liste_subdivisions')

def supprimer_affectation(request, id):
    affectation = get_object_or_404(Affectation, id=id)
    affectation.delete()
    return redirect('liste_affectations')


 
def home(request):
    context = {
        'services_count': Service.objects.count(),
        'fonctionnaires_count': Fonctionnaire.objects.count(),
        'equipements_count': Equipement.objects.count(),
        'batiments_count': Batiment.objects.count(),
        'subdivisions_count': Subdivision.objects.count(),
    }
    return render(request, 'inventaire/home.html', context)



def restituer_equipement(request, affectation_id):
    # 1. On récupère l'affectation
    affectation = get_object_or_404(Affectation, id=affectation_id)
    
    if not affectation.date_fin:
        affectation.date_fin = timezone.now().date()  
        affectation.save()
        messages.success(request, f"Le matériel {affectation.equipement.marque} a été marqué comme restitué.")
    
    # 3. On revient à la liste
    return redirect('liste_affectations')