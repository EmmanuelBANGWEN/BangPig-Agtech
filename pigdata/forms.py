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
            'animal_id':'Identification Number',
            'dob':'Date Of Birth',
            'gender':'gender',
            'breed':'Breed',
            'dam_no': 'DAM Number',
            'sire_no': 'SIRE Number',
            'grand_dam': 'Great DAM',
            'grand_sire': 'Grand SIRE',
            'colitter_size_of_birth': 'Colitter Size Of Birth',
            'color_and_marking':'Colors And Markings',
            'abnormalities': 'Genetic Abnormalities/Disorder',
        }
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

            
        }
        

class disposal_form(forms.ModelForm):
    class Meta:
        model=disposal_culling
        exclude = ['user']        
        labels={
            'gip': 'Identification Number',
            'reason': 'Reason For Sale/Transfer',
            'sale_date': 'Date Of Sale/Transfer',
            'weight_sale': 'Weight At Sale/Transfer',
            'revenue':'Revenue Generated'
            
        }
        widgets = {
            'sale_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

        }
class death_form(forms.ModelForm):
    class Meta:
        model = death
        exclude = ['user'] 
        labels = {
            'gip': 'Identification Number',
            'cause_death': 'Cause Of Death',
            'date_death': 'Date Of Death',
            'postmortem_findings': 'Post Mortem Findings',
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
        labels={
            'gip': 'Identification Number',
            'treatment': 'Treatment',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'remarks': 'Remarks',
        }
        widgets = {

            'start_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

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
        labels={
            'gip': 'Identification Number',
            'disease': 'Against Disease',
            'make': 'Make',
            'first_dose': 'First Dose',
            'booster_dose': 'Booster Dose',
            'repeat': 'repeat',
        }
        widgets = {
            # 'user': forms.HiddenInput(),  # Champ masqué

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
        labels={
            'gip': 'Identification Number',
            'reason': 'Reason/Symptoms',
            'date_of_treatment': 'Date of Treatment',
            'medication': 'Medication',
            'remarks': 'Remarks',
        }
        widgets = {
            'date_of_treatment': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

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
            'gip': 'Identification Number',
            'dow': 'Date Of Weaning',
            'litter_size_weaning':'Litter Size At Weaning',
            'weaning_age': 'Age At Weaning',
            'weaning_weight': 'Weaning Weight',
            'dos': 'Date of Separation From Male Animal',
            'dosm': 'Date of Sexual Maturity',
            'sexual_maturity_weight': 'Weight At Sexual Maturity',
            'weight_six': 'Weight At Six Months',
            'weight_eight':'Weight At Eight Months',
            'conform_at_eight': 'Conformation At Eight Months',
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
            'gip': 'Identification Number',
            'dow': 'Date Of Weaning',
            'litter_size_weaning':'Litter Size At Weaning',
            'weaning_age': 'Age At Weaning',
            'weaning_weight': 'Weaning Weight',
            'dos': 'Date of Separation From Female Animal',
            'doc': 'Date of Castration',
            'dosm': 'Date of Sexual Maturity',
            'sexual_maturity_weight': 'Weight At Sexual Maturity',
            'weight_six': 'Weight At Six Months',
            'weight_eight': 'Weight At Eight Months',
            'conform_at_eight': 'Conformation At Eight Months',
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
        labels={
            'gip': 'Identification Number',
            'physical_fitness': 'Physical Fitness',
            'date_of_training': 'Date Of Onset Of Training',
            'period_of_training': 'Period Of Training',
            'training_score': 'Training Score',
            'seminal_characteristics': 'Evaluation Based On Seminal Characteristics',
            'suitability': 'Suitability For Insemination',
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
            'gip': 'Identification Number',
            'sow_no': 'SOW Number',
            'dos': 'Date de service ',
            'dof': 'Date de mise bas',
            'parity': 'Parity',
            'born_male': 'Number of male born',
            'born_female': 'Number of male born',
            'born_total': 'Total Number',
            'litter_weight_birth': 'Litter Weight At Birth',
            'weaned_male': 'Number Of Weaned Male',
            'weaned_female': 'Number Of Weaned Female',
            'total_weaned': 'Number Of Total Weaned',
            'weaning_weight': 'Weaning Weight',
            'still_birth_abnormality': 'Still Birth Or Abnormality',
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

        labels={
            'gip': 'Identification Number',
            'boar_no':'Boar Number',
            'dos': 'Date de service ',
            'nos': 'Nature Of Service',
            'dof': 'Date de mise bas',
            'dow': 'Date of Weaning',
            'interfarrowing_interval':'Interfarrowing Interval(interval mise bas)',
            'parity': 'Parity',
            'born_male': 'Number of male born',
            'born_female': 'Number of male born',
            'born_total': 'Total Number',
            'litter_weight_birth': 'Litter Weight At Birth',
            'weaned_male': 'Number Of Weaned Male',
            'weaned_female': 'Number Of Weaned Female',
            'total_weaned': 'Number Of Total Weaned',
            'weaning_weight': 'Weaning Weight',
            'still_birth_abnormality': 'Still Birth Or Abnormality',
            'date_of_abortion':'Date Of Abortion',
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
            'animal_id': 'Identification Number',
            'dob': 'Date Of Birth',
            'gender': 'Gender',
            'breed': 'Breed',
            'dam_no': 'DAM Number',
            'sire_no': 'SIRE Number',
            'grand_dam': 'Great DAM',
            'grand_sire': 'Grand SIRE',
            'colitter_size_of_birth': 'Taille de la portée à la naissance',
            'color_and_marking': 'Colors And Markings',
            'abnormalities': 'Genetic Abnormalities/Disorder',
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
            'gip': 'Identification Number',
            'reason': 'Reason For Sale/Transfer',
            'sale_date': 'Date Of Sale/Transfer',
            'weight_sale': 'Weight At Sale/Transfer',
            'revenue': 'Revenue Generated'
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

        labels={
            'gip': 'Identification Number',
            'cause_death': 'Cause Of Death',
            'date_death': 'Date Of Death',
            'postmortem_findings':'Post Mortem Findings'
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
        labels={
            'gip': 'Identification Number',
            'treatment': 'Treatment',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'remarks': 'Remarks',
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
            'gip': 'Identification Number',
            'disease': 'Against Disease',
            'make': 'Make',
            'first_dose': 'First Dose',
            'booster_dose': 'Booster Dose',
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
        labels={
            'gip': 'Identification Number',
            'reason': 'Reason/Symptoms',
            'date_of_treatment': 'Date of Treatment',
            'medication': 'Medication',
            'remarks': 'Remarks',
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
  

        labels={
            'gip': 'Identification Number',
            'dow': 'Date Of Weaning',
            'litter_size_weaning':'Litter Size At Weaning',
            'weaning_age': 'Age At Weaning',
            'weaning_weight': 'Weaning Weight',
            'dos': 'Date of Separation From Male Animal',
            'dosm': 'Date of Sexual Maturity',
            'sexual_maturity_weight': 'Weight At Sexual Maturity',
            'weight_six': 'Weight At Six Months',
            'weight_eight': 'Weight At Eight Months',
            'conform_at_eight': 'Conformation At Eight Months',
        }
        widgets = {
            
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

             }


class efficiency_update_form_male(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_male
        fields = '__all__'

        exclude = ['user', 'animal_id', 'weaning_age'] 

        labels={
            'gip': 'Identification Number',
            'dow': 'Date Of Weaning',
            'litter_size_weaning':'Litter Size At Weaning',
            'weaning_age': 'Age At Weaning',
            'weaning_weight': 'Weaning Weight',
            'dos': 'Date of Separation From Female Animal',
            'doc': 'Date of Castration',
            'dosm': 'Date of Sexual Maturity',
            'sexual_maturity_weight': 'Weight At Sexual Maturity',
            'weight_six': 'Weight At Six Months',
            'weight_eight': 'Weight At Eight Months',
            'conform_at_eight': 'Conformation At Eight Months',
            
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

        labels={
            'gip': 'Identification Number',
            'physical_fitness': 'Physical Fitness',
            'date_of_training': 'Date Of Onset Of Training',
            'period_of_training': "Periode d'entrainement",
            'training_score': 'Training Score',
            'seminal_characteristics': 'Evaluation Based On Seminal Characteristics',
            'suitability': 'Suitability For Insemination',
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
       

        labels={
            'gip': 'Identification Number',
            'sow_no': 'SOW Number',
            'dos': 'Date de service ',
            'dof': 'Date de mise bas',
            'parity': 'Parity',
            'born_male': 'Number of male born',
            'born_female': 'Number of male born',
            'born_total': 'Total Number',
            'litter_weight_birth': 'Litter Weight At Birth',
            'weaned_male': 'Number Of Weaned Male',
            'weaned_female': 'Number Of Weaned Female',
            'total_weaned': 'Number Of Total Weaned',
            'weaning_weight': 'Weaning Weight',
            'still_birth_abnormality': 'Still Birth Or Abnormality',
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

        labels={
            'gip': 'Identification Number',
            'boar_no':'Boar Number',
            'dos': 'Date de service ',
            'nos': 'Nature Of Service',
            'dof': 'Date de mise bas',
            'dow': 'Date of Weaning',
            'interfarrowing_interval':'Interfarrowing Interval',
            'parity': 'Parity',
            'born_male': 'Number of male born',
            'born_female': 'Number of male born',
            'born_total': 'Total Number',
            'litter_weight_birth': 'Litter Weight At Birth',
            'weaned_male': 'Number Of Weaned Male',
            'weaned_female': 'Number Of Weaned Female',
            'total_weaned': 'Number Of Total Weaned',
            'weaning_weight': 'Weaning Weight',
            'still_birth_abnormality': 'Still Birth Or Abnormality',
            'date_of_abortion':'Date Of Abortion',
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