from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class datetodate(forms.Form):
    from_date=forms.DateField(label='De', widget=forms.DateInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}))
    to_date=forms.DateField(label='à', widget=forms.DateInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}))
    
 
class selectpigsform(forms.Form):
    CHOICES = (('1','Les porcs avec une taille de portée à la naissance inférieure à : '),
               ('2','Les porcs avec une taille de portée à la naissance supérieure à : '),
                ( '3','Les porcs avec une taille de portée au sevrage supérieure ou égale à : '),
                ('4','Les porcs avec une taille de portée au sevrage exactement égale à : '))
    task = forms.ChoiceField(choices=CHOICES, label='Rechercher')
    amount=forms.CharField(label='amount', max_length='500')
 
# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model=User
#         fields=['username','email', 'password1', 'password2']
#         labels={'username': 'Username'}
        


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(label="username", 
                               max_length=200, 
                               help_text='', 
                               required=True, 
                               widget=forms.TextInput(attrs={"type":"text", "id":"Username","class":"form-control",  "placeholder":"Username"}) )
    
   

    email = forms.EmailField(label="Email", 
                             max_length=200, min_length=5,
                             help_text='', 
                             required=True, 
                            widget=forms.TextInput(attrs={"type":"text", "id":"emailAddress", "class":"form-control",  "placeholder":"Email Address"}) )
    

    password1 = forms.CharField(label="Password", 
                               max_length=200, min_length=8,
                               help_text='', 
                               required=True, 
                               widget=forms.TextInput(attrs={"type":"text", "id":"password", "class":"form-control",  "placeholder":"Password"}) )
    

    password2 = forms.CharField(label="Repeat Password", 
                                     max_length=200, min_length=8,
                                     help_text='', 
                                     required=True, 
                                     widget=forms.TextInput(attrs={"type":"text", "id":"repeatpassword", "class":"form-control",  "placeholder":"Repeat Password"}) )
    class Meta:
        model = User
        fields=['username','email', 'password1', 'password2']






class loginuserform(forms.Form):
    username=forms.CharField(label='Username', max_length=150)
    password=forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput)

class general_form(forms.ModelForm):
    class Meta:
        model=general_identification_and_parentage
        exclude = ['user']        
        labels = {
                'animal_id': "Numéro d'identification",
                'dob': 'Date de naissance',
                'gender': 'Sexe',
                'breed': 'Race',
                'dam_no': "Numéro d'identification de la mère",
                'sire_no': "Numéro d'identification du père",
                'grand_dam': "Numéro d'identification de la grand-mère",
                'grand_sire': "Numéro d'identification du grand-père",
                'colitter_size_of_birth': 'Taille de la portée à la naissance',
                'color_and_marking': 'Couleurs et marques',
                'abnormalities': 'Anomalies génétiques / troubles',
            }

        widgets = {
            'dob': forms.DateInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

            
        }
        

class disposal_form(forms.ModelForm):
    class Meta:
        model=disposal_culling
        exclude = ['user']        
        labels = {
                'gip': "Numéro d'identification",
                'reason': 'Raison de la vente/transfert',
                'sale_date': 'Date de vente/transfert',
                'weight_sale': 'Poids à la vente/transfert',
                'revenue': 'Revenu généré',
        }
        widgets = {
            'sale_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }
class death_form(forms.ModelForm):
    class Meta:
        model = death
        exclude = ['user'] 
        labels = {
            'gip': "Numéro d'identification",
            'cause_death': 'Cause du décès',
            'date_death': 'Date du décès',
            'postmortem_findings': 'Résultats de l\'autopsie',
        }

        widgets = {
            'date_death': forms.TextInput(attrs={
                'class': 'flatpickr',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',
            }),
        }

    def __init__(self, *args, user=None, specific_animal=None, **kwargs):
        super().__init__(*args, **kwargs)
        if specific_animal:
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
            self.fields['gip'].initial = specific_animal
            self.fields['gip'].widget.attrs['readonly'] = True  # Rendre le champ non modifiable
        elif user:
            # Filtrer les animaux accessibles par l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

class nutrition_form(forms.ModelForm):
    class Meta:
        model=nutrition_and_feeding
        fields='__all__'
        labels = {
                    'gip': "Numéro d'identification",
                    'treatment': 'Traitement',
                    'start_date': 'Date de début',
                    'end_date': 'Date de fin',
                    'remarks': 'Remarques',
                }

        widgets = {

            'start_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'gip': forms.HiddenInput(),  # Champ masqué

        }
    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)


# class economics_form(forms.ModelForm):
#     class Meta:
#         model=economics
#         exclude = ['user'] 
#         labels={
#             'gip': 'Identification Number',
#             'book_value': 'Book Value',
#             'amount_realized': 'Amount Realized',
#         }
#     def __init__(self, *args, user=None, **kwargs):
#         # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
#         initial = kwargs.get('initial', {})
#         specific_animal = initial.get('gip', None)

#         super().__init__(*args, **kwargs)
#         if specific_animal:
#             # Restreindre le champ `gip` à l'animal spécifique
#             self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
#         elif user:
#             # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
#             self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)



class vaccination_form(forms.ModelForm):
    class Meta:
        model=health_parameter_vaccination
        exclude = ['user']        

        # fields='__all__'        
        labels = {
            'gip': "Numéro d'identification",
            'disease': 'Maladie(Vaccin)',
            'make': 'Marque',
            'first_dose': 'Première dose',
            'booster_dose': 'Dose de rappel',
            # 'repeat': 'Répétition',
        }

        widgets = {
            'gip': forms.HiddenInput(),  # Champ masqué

            'first_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'booster_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'repeat': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            # 'booster': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }
        
    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

class vetexam_form(forms.ModelForm):
    class Meta:
        model=health_parameter_vetexam
        fields='__all__'
        labels = {
            'gip': "Numéro d'identification",
            'reason': 'Raison/Symptômes',
            'date_of_treatment': 'Date du traitement',
            'medication': 'Médicament',
            'remarks': 'Remarques',
        }

        widgets = {
            'date_of_treatment': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'gip': forms.HiddenInput(),  # Champ masqué

        }

    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)


class efficiency_form_female(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_female
        exclude = ['user','weaning_age'] 
        labels={
            'gip': "Numéro d'identification",
            'dow': 'Date de sevrage',
            'litter_size_weaning':'Taille de la portée au sevrage',
            'weaning_age': 'Âge au sevrage (en jours)',
            'weaning_weight': 'Poids au sevrage',
            'dos': 'Date de séparation du mâle',
            'dosm': 'Date de maturité sexuelle',
            'sexual_maturity_weight': 'Poids à la maturité sexuelle',
            'weight_six': 'Poids à six mois',
            'weight_eight':'Poids à huit mois',
            'conform_at_eight': 'Conformation à huit mois',
        }
        widgets = {
        
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }
    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)



class efficiency_form_male(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_male
        exclude = ['user','weaning_age'] 
        labels={
            'gip': "Numéro d'identification",
            'dow': 'Date de sevrage',
            'litter_size_weaning':'Taille de la portée au sevrage',
            'weaning_age': 'Âge au sevrage (en jours)',
            'weaning_weight': 'Poids au sevrage',
            'dos': 'Date de séparation du mâle',
            'doc': 'Date de Castration',
            'dosm': 'Date de maturité sexuelle',
            'sexual_maturity_weight': 'Poids à la maturité sexuelle',
            'weight_six': 'Poids à six mois',
            'weight_eight': 'Poids à huit mois',
            'conform_at_eight': 'Conformation à huit mois',
        }
        widgets = {
            
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'doc': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }

    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)



class qualification_form(forms.ModelForm):
    class Meta:
        model=qualification_boar
        exclude = ['user'] 
        labels = {
                'gip': "Numéro d'identification",
                'physical_fitness': 'Aptitude physique',
                'date_of_training': 'Date de début de l\'entraînement',
                'period_of_training': 'Période d\'entraînement',
                'training_score': 'Score d\'entraînement',
                'seminal_characteristics': 'Évaluation basée sur les caractéristiques séminales',
                'suitability': 'Aptitude à l\'insémination',
            }

        widgets = {
            'date_of_training': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

            
        }
    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)



class service_form_male(forms.ModelForm):
    class Meta:
        model=service_record_male
        fields='__all__'
        exclude = ['born_total', 'total_weaned']        

        labels={
                'gip': "Numéro d'identification",
                'sow_no': 'Identifiant de la truie',
                'dos': 'Date de service(Accouplement)',
                'dof': 'Date de mise bas',
                # 'parity': 'Parité',
                'born_male': 'Nombre de mâles nés',
                'born_female': 'Nombre de femelles nées',
                'born_total': 'Nombre total de nés',
                'litter_weight_birth': 'Taille de la portée à la naissance',
                'weaned_male': 'Nombre de mâles sevrés',
                'weaned_female': 'Nombre de femelles sevrées',
                'total_weaned': 'Nombre total de sevrés',
                'weaning_weight': 'Poids au sevrage',
                'still_birth_abnormality': 'Mort-né ou anomalie',
            }

        widgets = {

            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        # Remplacer les champs None ou vides par 0
        numeric_fields = ['born_male', 'born_female', 'weaned_male', 'weaned_female', 'litter_weight_birth', 'weaning_weight']
        for field in numeric_fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = 0
        return cleaned_data

class service_form_female(forms.ModelForm):
    class Meta:
        model=service_record_female
        fields='__all__'
        exclude = ['born_total', 'total_weaned']        

        labels = {
                    'gip': 'Numéro d’identification',
                    'boar_no': 'Identifiant du verrat',
                    'dos': 'Date de service(Accouplement)',
                    'nos': 'Nature du service',
                    'dof': 'Date de mise bas',
                    'dow': 'Date de sevrage',
                    'interfarrowing_interval': 'Intervalle entre mises bas',
                    # 'parity': 'Parité',
                    'born_male': 'Nombre de mâles nés',
                    'born_female': 'Nombre de femelles nées',
                    'born_total': 'Nombre total de naissance',
                    'litter_weight_birth': 'Taille de la portée à la naissance',
                    'weaned_male': 'Nombre de mâles sevrés',
                    'weaned_female': 'Nombre de femelles sevrées',
                    'total_weaned': 'Nombre total de sevrés',
                    'weaning_weight': 'Poids au sevrage',
                    'still_birth_abnormality': 'Mort-né ou anomalie',
                    'date_of_abortion': 'Date d’avortement',
                }

        widgets = {
            
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'date_of_abortion': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        # Remplacer les champs None ou vides par 0
        numeric_fields = ['born_male', 'born_female', 'weaned_male', 'weaned_female', 'litter_weight_birth', 'weaning_weight']
        for field in numeric_fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = 0
        return cleaned_data













class general_update_form(forms.ModelForm):
    class Meta:
        model = general_identification_and_parentage
        fields = '__all__'
        exclude = ['user', 'animal_id'] 
        # exclude = ['animal_id']        
       

        labels = {
            'animal_id': "Numéro d'identification",
            'dob': 'Date de naissance',
            'gender': 'Sexe',
            'breed': 'Race',
            'dam_no': "Numéro d'identification de la mère",
            'sire_no': "Numéro d'identification du père",
            'grand_dam': "Numéro d'identification de la grand-mère",
            'grand_sire': "Numéro d'identification du grand-père",
            'colitter_size_of_birth': 'Taille de la portée à la naissance',
            'color_and_marking': 'Couleurs et marques',
            'abnormalities': 'Anomalies génétiques',
        }
        widgets = {
            # 'user': forms.HiddenInput(),  # Champ masqué
            # 'animal_id': forms.HiddenInput(),  # Champ masqué

            # 'animal_id': forms.TextInput(attrs={'readonly': 'readonly'}),  # Champ non modifiable
            'dob': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
        }
    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)
 
        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

        

class disposal_update_form(forms.ModelForm):
    class Meta:
        model = disposal_culling
        exclude = ['user']        

        labels = {
                    'gip': "Numéro d'identification",
                    'reason': 'Raison de la vente/transfert',
                    'sale_date': 'Date de vente/transfert',
                    'weight_sale': 'Poids à la vente/transfert',
                    'revenue': 'Revenu généré'
                }

        widgets = {
            'sale_date': forms.TextInput(attrs={
                'class': 'flatpickr',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'
            }),
        }

    def __init__(self, *args, user=None, specific_animal=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Restreindre le champ `gip` à l'animal spécifique
        if specific_animal:
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
            self.fields['gip'].initial = specific_animal
            self.fields['gip'].widget.attrs['readonly'] = True  # Rendre le champ non modifiable
        elif user:
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

        # Masquer les champs sensibles comme `animal_id` en les désactivant
        for field_name in ['reason', 'sale_date', 'weight_sale', 'revenue']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = False  # Rendre les champs modifiables


class death_update_form(forms.ModelForm):
    class Meta:
        model=death
        exclude = ['user']        

        labels = {
    'gip': 'Numéro d’identification',
    'cause_death': 'Cause du décès',
    'date_death': 'Date du décès',
    'postmortem_findings': 'Résultats de l’autopsie'
}

        widgets = {
            'date_death': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)




class nutrition_update_form(forms.ModelForm):
    class Meta:
        model=nutrition_and_feeding
        fields='__all__'
        # exclude = ["user"]
        labels = {
                'gip': "Numéro d'identification",
                'treatment': 'Traitement',
                'start_date': 'Date de début',
                'end_date': 'Date de fin',
                'remarks': 'Remarques',
            }

        widgets = {
            # 'gip': forms.HiddenInput(),  # Champ masqué

            'start_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)


# class economics_update_form(forms.ModelForm):
#     class Meta:
#         model = economics
#         exclude = ['user']  # Exclure 'user' pour qu'il ne soit pas modifiable
#         labels = {
#             'book_value': 'Book Value',
#             'amount_realized': 'Amount Realized',
#         }
#         widgets = {
#             'book_value': forms.TextInput(attrs={'class': 'form-control'}),
#             'amount_realized': forms.TextInput(attrs={'class': 'form-control'}),
#             'gip': forms.HiddenInput(),  # Cacher le champ 'gip'
#         }

#     def __init__(self, *args, **kwargs):
#         specific_animal = kwargs.pop('specific_animal', None)
#         super().__init__(*args, **kwargs)
        
#         if specific_animal:
#             self.fields['gip'].initial = specific_animal  # Pré-remplir avec l'animal spécifique
#             self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
#             self.fields['gip'].widget.attrs['readonly'] = True  # Empêcher la modification


class vaccination_update_form(forms.ModelForm):
    class Meta:
        model=health_parameter_vaccination
        exclude = ['user']        
        labels={
            'gip': "Numéro d'identification",
            'disease': 'Maladie(Vaccin)',
            'make': 'Marque',
            'first_dose': 'Première dose',
            'booster_dose': 'Dose de rappel',
        }
        widgets = {
            
            'first_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'booster_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'repeat': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

            
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

    
class vetexam_update_form(forms.ModelForm):
    class Meta:
        model=health_parameter_vetexam
        fields='__all__'
        labels = {
    'gip': "Numéro d'identification",
    'reason': 'Raison/Symptômes',
    'date_of_treatment': 'Date du traitement',
    'medication': 'Médicament',
    'remarks': 'Remarques',
}

        widgets = {
            'date_of_treatment': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

        


class efficiency_update_form_female(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_female
        fields='__all__'
        # exclude = ['user', 'gip']      
        exclude = ['user', 'animal_id', 'weaning_age'] 
  

        labels = {
    'gip': 'Numéro d’identification',
    'dow': 'Date du sevrage',
    'litter_size_weaning': 'Taille de la portée au sevrage',
    'weaning_age': 'Âge au sevrage',
    'weaning_weight': 'Poids au sevrage',
    'dos': 'Date de séparation du mâle',
    'dosm': 'Date de maturité sexuelle',
    'sexual_maturity_weight': 'Poids à la maturité sexuelle',
    'weight_six': 'Poids à six mois',
    'weight_eight': 'Poids à huit mois',
    'conform_at_eight': 'Conformation à huit mois',
}

        widgets = {
            
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'gip': forms.HiddenInput(),  # Cacher le champ 'gip'

             }


class efficiency_update_form_male(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_male
        fields = '__all__'

        exclude = ['user', 'animal_id', 'weaning_age'] 

        labels = {
    'gip': 'Numéro d’identification',
    'dow': 'Date du sevrage',
    'litter_size_weaning': 'Taille de la portée au sevrage',
    'weaning_age': 'Âge au sevrage',
    'weaning_weight': 'Poids au sevrage',
    'dos': 'Date de séparation de la femelle',
    'doc': 'Date de castration',
    'dosm': 'Date de maturité sexuelle',
    'sexual_maturity_weight': 'Poids à la maturité sexuelle',
    'weight_six': 'Poids à six mois',
    'weight_eight': 'Poids à huit mois',
    'conform_at_eight': 'Conformation à huit mois',
}

        widgets = {
           
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'doc': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'gip': forms.HiddenInput(),  # Cacher le champ 'gip'

             }

    def __init__(self, *args, user=None, **kwargs):
        # Récupérer l'animal spécifique depuis l'initialisation (kwargs['initial'])
        initial = kwargs.get('initial', {})
        specific_animal = initial.get('gip', None)

        super().__init__(*args, **kwargs)
        if specific_animal:
            # Restreindre le champ `gip` à l'animal spécifique
            
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
            # self.fields['gip'].widget.attrs['readonly'] = True  # Empêcher la modification

        elif user:
            # Si aucun animal spécifique, filtrer les animaux appartenant à l'utilisateur connecté
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

    

  
class qualification_update_form(forms.ModelForm):
    class Meta:
        model=qualification_boar
        # fields='__all__'

        exclude = ['user', 'gip']        

        labels = {
    'gip': 'Numéro d’identification',
    'physical_fitness': 'Aptitude physique',
    'date_of_training': 'Date de début de l’entraînement',
    'period_of_training': "Période d'entraînement",
    'training_score': "Score d'entraînement",
    'seminal_characteristics': 'Évaluation basée sur les caractéristiques séminales',
    'suitability': 'Aptitude à l’insémination',
}

        widgets = {
            'date_of_training': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
 }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)


class service_update_form_male(forms.ModelForm):
    class Meta:
        model=service_record_male
        fields='__all__'
        exclude = ['born_total', 'total_weaned']        
       

        labels = {
    'gip': 'Numéro d’identification',
    'sow_no': 'Identifiant de la truie',
    'dos': 'Date de service(Accouplement)',
    'dof': 'Date de mise bas',
    # 'parity': 'Parité',
    'born_male': 'Nombre de mâles nés',
    'born_female': 'Nombre de femelles nées',
    'born_total': 'Nombre total de naissances',
    'litter_weight_birth': 'Taille de la portée à la naissance',
    'weaned_male': 'Nombre de mâles sevrés',
    'weaned_female': 'Nombre de femelles sevrées',
    'total_weaned': 'Nombre total de sevrés',
    'weaning_weight': 'Poids au sevrage',
    'still_birth_abnormality': 'Mort-né ou anomalie',
}

        widgets = {
           
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

                  }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)



    def clean(self):
        cleaned_data = super().clean()
        # Remplacer les champs None ou vides par 0
        numeric_fields = ['born_male', 'born_female', 'weaned_male', 'weaned_female', 'litter_weight_birth', 'weaning_weight']
        for field in numeric_fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = 0
        return cleaned_data
class service_update_form_female(forms.ModelForm):
    class Meta:
        model=service_record_female
        fields='__all__'
        exclude = ['born_total', 'total_weaned']        

        labels = {
    'gip': 'Numéro d’identification',
    'boar_no': 'Identifiant du verrat',
    'dos': 'Date de service(Accouplement)',
    'nos': 'Nature du service',
    'dof': 'Date de mise bas',
    'dow': 'Date de sevrage',
    'interfarrowing_interval': 'Intervalle entre mises bas',
    # 'parity': 'Parité',
    'born_male': 'Nombre de mâles nés',
    'born_female': 'Nombre de femelles nées',
    'born_total': 'Nombre total de naissances',
    'litter_weight_birth': 'Taille de la portée à la naissance',
    'weaned_male': 'Nombre de mâles sevrés',
    'weaned_female': 'Nombre de femelles sevrées',
    'total_weaned': 'Nombre total de sevrés',
    'weaning_weight': 'Poids au sevrage',
    'still_birth_abnormality': 'Mort-né ou anomalie',
    'date_of_abortion': 'Date de l’avortement',
}

        widgets = {


            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'date_of_abortion': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

                   }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        specific_animal = kwargs.pop('specific_animal', None)
        super().__init__(*args, **kwargs)
        
        if specific_animal:
            # Ne garder que l'animal spécifique
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(pk=specific_animal.pk)
        elif user:
            # Filtrer par utilisateur
            self.fields['gip'].queryset = general_identification_and_parentage.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        # Remplacer les champs None ou vides par 0
        numeric_fields = ['born_male', 'born_female', 'weaned_male', 'weaned_female', 'litter_weight_birth', 'weaning_weight']
        for field in numeric_fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = 0
        return cleaned_data


class SearchPig(forms.Form):
    query = forms.CharField(max_length=200)
    class Meta:
        fields = ['query']




from django import forms
from .models import Contact

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Adresse Email")
    number = forms.CharField(label="Number")
    message = forms.CharField(widget=forms.Textarea, label="Message")