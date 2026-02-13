from django import forms
from .models import Service, Secteur, Batiment, Subdivision, Bureau, Fonctionnaire, Equipement, Historique, Affectation
from django.core.exceptions import ValidationError 
from django.db.models import Q


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class SubdivisionForm(forms.ModelForm):
    class Meta:
        model = Subdivision
      #   fields = '__all__'
        fields = ['service', 'libelle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            # On désactive le champ service
            self.fields['service'].disabled = True


class SecteurForm(forms.ModelForm):

    service = forms.ModelChoiceField(queryset=Service.objects.all(), label="Service", required=False)
    field_order = ['service','subdivision', 'libelle']
    class Meta:
        model = Secteur
        fields = ['subdivision', 'libelle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['service'].disabled = True
            self.fields['subdivision'].disabled = True

        self.fields['subdivision'].queryset = Subdivision.objects.none()

        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['subdivision'].queryset = Subdivision.objects.filter(service_id=service_id).order_by('libelle')
            except (ValueError, TypeError):
                pass 
        
        elif self.instance.pk and self.instance.subdivision:

            self.fields['subdivision'].queryset = Subdivision.objects.filter(service=self.instance.subdivision.service ).order_by('libelle')
            self.fields['service'].initial = self.instance.subdivision.service
        
   
    

class BureauForm(forms.ModelForm):
    class Meta:
        model = Bureau
        fields = '__all__'

class FonctionnaireForm(forms.ModelForm):
    class Meta:
        model = Fonctionnaire
        
        fields = '__all__'

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = '__all__'
        
        widgets = {
            'type_materiel': forms.Select(attrs={'id': 'typeSelect'}),
            'marque': forms.Select(attrs={'id': 'marqueSelect'}),
            'modele': forms.Select(attrs={'id': 'modeleSelect'}),
        }
        

class HistoriqueForm(forms.ModelForm):
    class Meta:
        model = Historique
        fields = '__all__'

        widgets = {
            'date_entree': forms.DateInput(attrs={'type': 'date'}),
            'date_sortie': forms.DateInput(attrs={'type': 'date'}),
        }


class BatimentForm(forms.ModelForm):
    class Meta:
        model = Batiment
        fields = '__all__'


     
 
class AffectationForm(forms.ModelForm):
    # Vos champs de filtrage (inchangés)
    type_materiel = forms.ChoiceField(
        choices=[('', '---------')] + Equipement.TYPE_CHOICES, 
        required=False,
        label="Type de matériel"
    )
    marque = forms.ChoiceField(
        choices=[('', '---------')] + Equipement.MARQUE_CHOICES, 
        required=False, 
        label="Marque"
    )

    class Meta:
        model = Affectation
        fields = ['fonctionnaire', 'equipement']
        widgets = {
            'fonctionnaire': forms.Select(attrs={'class': 'form-control'}),
            'equipement': forms.Select(attrs={'class': 'form-control', 'id': 'id_equipement'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        # 1. On identifie les équipements ACTUELLEMENT pris
        equipements_pris_ids = Affectation.objects.filter(
            date_fin__isnull=True
        ).values_list('equipement_id', flat=True)

        # 2. La requête de base : Tous les équipements SAUF ceux qui sont pris
        base_qs = Equipement.objects.exclude(id__in=equipements_pris_ids)

        # 3. Cas de la modification (Edit)
        if self.instance.pk and self.instance.equipement:
            current_id = self.instance.equipement.id
            self.fields['type_materiel'].initial = self.instance.equipement.type_materiel
            self.fields['marque'].initial = self.instance.equipement.marque
            
            self.fields['equipement'].queryset = Equipement.objects.filter(
                Q(id__in=base_qs.values('id')) | Q(id=current_id)
            )
        else:
            self.fields['equipement'].queryset = Equipement.objects.none()

        # 4. Gestion du remplissage dynamique
        if 'marque' in self.data or 'type_materiel' in self.data:
            try:
                marque_id = self.data.get('marque')
                type_id = self.data.get('type_materiel')
                
                query = base_qs
                
                if marque_id:
                    query = query.filter(marque=marque_id)
                if type_id:
                    query = query.filter(type_materiel=type_id)
                
                self.fields['equipement'].queryset = query
            except (ValueError, TypeError):
                pass

     
    def clean(self):
        cleaned_data = super().clean()
        equipement = cleaned_data.get('equipement')
        fonctionnaire = cleaned_data.get('fonctionnaire')

        # 1. Vérification de sécurité : L'équipement est-il vraiment libre ?
        # (Au cas où deux personnes valident en même temps)
        if equipement:
        
             
            qs_verif = Affectation.objects.filter(
                equipement=equipement,
                date_fin__isnull=True 
            )
            
            if self.instance.pk:
                qs_verif = qs_verif.exclude(pk=self.instance.pk)

            if qs_verif.exists():
                self.add_error('equipement', "Cet équipement est déjà affecté à quelqu'un d'autre.")

        # 2. Vérification de la restriction 'limite_un_par_type'
        if fonctionnaire and equipement:
            # On vérifie si la case est cochée (True) sur la fiche du fonctionnaire
            if fonctionnaire.limite_un_par_type:
                type_mat = equipement.type_materiel
                
                # On cherche si le fonctionnaire a DÉJÀ une affectation active pour ce TYPE
                qs_doublon = Affectation.objects.filter(
                    fonctionnaire=fonctionnaire,
                    equipement__type_materiel=type_mat,

                    date_fin__isnull=True
                )


                if self.instance.pk:
                    qs_doublon = qs_doublon.exclude(pk=self.instance.pk)

                if qs_doublon.exists():
                    msg = (
                        f"Règle de gestion : {fonctionnaire.nom} {fonctionnaire.prenom} a déjà un équipement "
                        f"de type '{type_mat}' actif. La restriction '1 par type' est activée sur sa fiche."
                    )
                    # On attache l'erreur au champ fonctionnaire
                    self.add_error('fonctionnaire', msg)

        return cleaned_data
    
    