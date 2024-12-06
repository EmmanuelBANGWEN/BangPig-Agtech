from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from bootstrap_datepicker_plus import DatePickerInput

class datetodate(forms.Form):
    from_date=forms.DateField(label='From')
    to_date=forms.DateField(label='To')

class selectpigsform(forms.Form):
    CHOICES = (('1','Litter size of birth is less than'),('2','Litter size of birth is greater than'),
    ( '3','Litter size of weaning is greater than'),('4','Litter size of weaning is equal to'))
    task = forms.ChoiceField(choices=CHOICES, label='The')
    amount=forms.CharField(label='', max_length='150')

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email', 'password1', 'password2']
        labels={'username': 'Username'}
        

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
            # 'dob': DatePickerInput(format='%Y-%m-%d'),
            'dob': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            
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
            # 'sale_date': DatePickerInput(format='%Y-%m-%d'),
            'sale_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

        }

class death_form(forms.ModelForm):
    class Meta:
        model=death
        fields='__all__'
        labels={
            'gip': 'Identification Number',
            'cause_death': 'Cause Of Death',
            'date_death': 'Date Of Death',
            'postmortem_findings':'Post Mortem Findings'
        }
        widgets = {
            # 'date_death': DatePickerInput(format='%Y-%m-%d'),
            'date_death': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

        }


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

            'start_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

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


class economics_form(forms.ModelForm):
    class Meta:
        model=economics
        fields='__all__'
        labels={
            'gip': 'Identification Number',
            'book_value': 'Book Value',
            'amount_realized': 'Amount Realized',
        }

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

            'first_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'booster_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'repeat': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            # 'booster': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

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
            'date_of_treatment': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

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
        fields='__all__'
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
        
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

        }


class efficiency_form_male(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_male
        fields='__all__'
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
            # 'dow': DatePickerInput(format='%Y-%m-%d'),
            # 'dos': DatePickerInput(format='%Y-%m-%d'),
            # 'doc': DatePickerInput(format='%Y-%m-%d'),
            # 'dosm': DatePickerInput(format='%Y-%m-%d'),

            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'doc': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

        }

class qualification_form(forms.ModelForm):
    class Meta:
        model=qualification_boar
        fields='__all__'
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
            'date_of_training': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            
        }

class service_form_male(forms.ModelForm):
    class Meta:
        model=service_record_male
        fields='__all__'
        labels={
            'gip': 'Identification Number',
            'sow_no': 'SOW Number',
            'dos': 'Date de service ',
            'dof': 'Date Of Farrowing',
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

            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

        }

class service_form_female(forms.ModelForm):
    class Meta:
        model=service_record_female
        fields='__all__'
        labels={
            'gip': 'Identification Number',
            'boar_no':'Boar Number',
            'dos': 'Date de service ',
            'nos': 'Nature Of Service',
            'dof': 'Date Of Farrowing',
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
            # 'dos': DatePickerInput(format='%Y-%m-%d'),
            # 'dof': DatePickerInput(format='%Y-%m-%d'),
            # 'dow': DatePickerInput(format='%Y-%m-%d'),
            # 'date_of_abortion': DatePickerInput(format='%Y-%m-%d'),

            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'date_of_abortion': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

        }













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
            'colitter_size_of_birth': 'Colitter Size Of Birth',
            'color_and_marking': 'Colors And Markings',
            'abnormalities': 'Genetic Abnormalities/Disorder',
        }
        widgets = {
            # 'user': forms.HiddenInput(),  # Champ masqué
            # 'animal_id': forms.HiddenInput(),  # Champ masqué

            # 'animal_id': forms.TextInput(attrs={'readonly': 'readonly'}),  # Champ non modifiable
            'dob': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
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
        model=disposal_culling
        fields='__all__'
        exclude = ['user', 'gip']        

        labels={
            'gip': 'Identification Number',
            'reason': 'Reason For Sale/Transfer',
            'sale_date': 'Date Of Sale/Transfer',
            'weight_sale': 'Weight At Sale/Transfer',
            'revenue':'Revenue Generated'
        }
        widgets = {
            'sale_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
           
            #'gip': forms.TextInput(attrs={'disabled':True}),
            #'reason': forms.TextInput(attrs={'disabled':True}),
            #'sale_date': forms.TextInput(attrs={'disabled':True}),
            #'weight_sale': forms.TextInput(attrs={'disabled':True}),
            #'revenue':forms.TextInput(attrs={'disabled':True})
            
        }

class death_update_form(forms.ModelForm):
    class Meta:
        model=death
        fields='__all__'
        exclude = ['user']        

        labels={
            'gip': 'Identification Number',
            'cause_death': 'Cause Of Death',
            'date_death': 'Date Of Death',
            'postmortem_findings':'Post Mortem Findings'
        }
        widgets = {
            'date_death': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            #'gip': forms.TextInput(attrs={'disabled':True}),
            #'cause_death': forms.TextInput(attrs={'disabled':True}),
            #'date_death': forms.TextInput(attrs={'disabled':True}),
            #'postmortem_findings':forms.TextInput(attrs={'disabled':True}),
        }



class nutrition_update_form(forms.ModelForm):
    class Meta:
        model=nutrition_and_feeding
        fields='__all__'
        # exclude = ["gip"]
        labels={
            'gip': 'Identification Number',
            'treatment': 'Treatment',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'remarks': 'Remarks',
        }
        widgets = {
            # 'gip': forms.HiddenInput(),  # Champ masqué

            'start_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

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

class economics_update_form(forms.ModelForm):
    class Meta:
        model=economics
        fields='__all__'
               
   

        labels={
            'gip': 'Identification Number',
            'book_value': 'Book Value',
            'amount_realized': 'Amount Realized',
        }
        widgets={
            # 'gip': forms.TextInput(attrs={'disabled':True}),
            # 'book_value': forms.TextInput(attrs={'disabled':True}),
            # 'amount_realized': forms.TextInput(attrs={'disabled':True}),
        }

class vaccination_update_form(forms.ModelForm):
    class Meta:
        model=health_parameter_vaccination
        exclude = ['user']        
        labels={
            'gip': 'Identification Number',
            'disease': 'Against Disease',
            'make': 'Make',
            'first_dose': 'First Dose',
            'booster': 'Booster Dose',
        }
        widgets = {
            # 'first_dose': DatePickerInput(format='%Y-%m-%d'),
            # 'booster': DatePickerInput(format='%Y-%m-%d'),
            # 'repeat': DatePickerInput(format='%Y-%m-%d'),

            'first_dose': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'booster': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'repeat': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'booster': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            #'gip': forms.TextInput(attrs={'disabled':True}),
            #'disease': forms.TextInput(attrs={'disabled':True}),
            #'make': forms.TextInput(attrs={'disabled':True}),
            #'first_dose': forms.TextInput(attrs={'disabled':True}),
            #'booster': forms.TextInput(attrs={'disabled':True}),
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
            'date_of_treatment': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            #'gip': forms.TextInput(attrs={'disabled':True}),
            #'reason': forms.TextInput(attrs={'disabled':True}),
            #'date_of_treatment': forms.TextInput(attrs={'disabled':True}),
            #'medication': forms.TextInput(attrs={'disabled':True}),
            #'remarks': forms.TextInput(attrs={'disabled':True}),
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
            # 'dow': DatePickerInput(format='%Y-%m-%d'),
            # 'dos': DatePickerInput(format='%Y-%m-%d'),
            # 'dosm': DatePickerInput(format='%Y-%m-%d'),

            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            #'gip': forms.TextInput(attrs={'disabled':True}),
            #'dow': forms.TextInput(attrs={'disabled':True}),
            #'litter_size_weaning':forms.TextInput(attrs={'disabled':True}),
            #'weaning_age': forms.TextInput(attrs={'disabled':True}),
            #'weaning_weight':forms.TextInput(attrs={'disabled':True}),
            #'dos': forms.TextInput(attrs={'disabled':True}),
            #'dosm': forms.TextInput(attrs={'disabled':True}),
            #'sexual_maturity_weight': forms.TextInput(attrs={'disabled':True}),
            #'weight_six': forms.TextInput(attrs={'disabled':True}),
            #'weight_eight': forms.TextInput(attrs={'disabled':True}),
            #'conform_at_eight': forms.TextInput(attrs={'disabled':True}),
        }


class efficiency_update_form_male(forms.ModelForm):
    class Meta:
        model=efficiency_parameter_male
        fields='__all__'
        exclude = ['user', 'gip']        

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
            # 'dow': DatePickerInput(format='%Y-%m-%d'),
            # 'dos': DatePickerInput(format='%Y-%m-%d'),
            # 'doc': DatePickerInput(format='%Y-%m-%d'),
            # 'dosm': DatePickerInput(format='%Y-%m-%d'),

            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'doc': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dosm': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            # 'gip': forms.TextInput(attrs={'disabled':True}),
            # 'dow': forms.TextInput(attrs={'disabled':True}),
            # 'litter_size_weaning':forms.TextInput(attrs={'disabled':True}),
            # 'weaning_age':forms.TextInput(attrs={'disabled':True}),
            # 'weaning_weight':forms.TextInput(attrs={'disabled':True}),
            # 'dos': forms.TextInput(attrs={'disabled':True}),
            # 'doc': forms.TextInput(attrs={'disabled':True}),
            # 'dosm': forms.TextInput(attrs={'disabled':True}),
            # 'sexual_maturity_weight': forms.TextInput(attrs={'disabled':True}),
            # 'weight_six': forms.TextInput(attrs={'disabled':True}),
            # 'weight_eight': forms.TextInput(attrs={'disabled':True}),
            # 'conform_at_eight': forms.TextInput(attrs={'disabled':True}),
        }

class qualification_update_form(forms.ModelForm):
    class Meta:
        model=qualification_boar
        fields='__all__'
        exclude = ['user', 'gip']        

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
            'date_of_training': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            # 'gip': forms.TextInput(attrs={'disabled':True}),
            # 'physical_fitness': forms.TextInput(attrs={'disabled':True}),
            # 'date_of_training': forms.TextInput(attrs={'disabled':True}),
            # 'period_of_training': forms.TextInput(attrs={'disabled':True}),
            # 'training_score':forms.TextInput(attrs={'disabled':True}),
            # 'seminal_characteristics': forms.TextInput(attrs={'disabled':True}),
            # 'suitability': forms.TextInput(attrs={'disabled':True}),
        }

class service_update_form_male(forms.ModelForm):
    class Meta:
        model=service_record_male
        fields='__all__'
        labels={
            'gip': 'Identification Number',
            'sow_no': 'SOW Number',
            'dos': 'Date de service ',
            'dof': 'Date Of Farrowing',
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
           
            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            # 'gip': forms.TextInput(attrs={'disabled':True}),
            # 'sow_no': forms.TextInput(attrs={'disabled':True}),
            # 'dos': forms.TextInput(attrs={'disabled':True}),
            # 'dof': forms.TextInput(attrs={'disabled':True}),
            # 'parity': forms.TextInput(attrs={'disabled':True}),
            # 'born_male': forms.TextInput(attrs={'disabled':True}),
            # 'born_female': forms.TextInput(attrs={'disabled':True}),
            # 'born_total': forms.TextInput(attrs={'disabled':True}),
            # 'litter_weight_birth': forms.TextInput(attrs={'disabled':True}),
            # 'weaned_male': forms.TextInput(attrs={'disabled':True}),
            # 'weaned_female': forms.TextInput(attrs={'disabled':True}),
            # 'total_weaned': forms.TextInput(attrs={'disabled':True}),
            # 'weaning_weight': forms.TextInput(attrs={'disabled':True}),
            # 'still_birth_abnormality': forms.TextInput(attrs={'disabled':True}),
        }

class service_update_form_female(forms.ModelForm):
    class Meta:
        model=service_record_female
        fields='__all__'
        labels={
            'gip': 'Identification Number',
            'boar_no':'Boar Number',
            'dos': 'Date de service ',
            'nos': 'Nature Of Service',
            'dof': 'Date Of Farrowing',
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


            'dos': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dof': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'dow': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),
            'date_of_abortion': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD'}),

            # 'gip': forms.TextInput(attrs={'disabled':True}),
            # 'boar_no':forms.TextInput(attrs={'disabled':True}),
            # 'dos': forms.TextInput(attrs={'disabled':True}),
            # 'nos': forms.TextInput(attrs={'disabled':True}),
            # 'dof': forms.TextInput(attrs={'disabled':True}),
            # 'dow': forms.TextInput(attrs={'disabled':True}),
            # 'interfarrowing_interval':forms.TextInput(attrs={'disabled':True}),
            # 'parity': forms.TextInput(attrs={'disabled':True}),
            # 'born_male': forms.TextInput(attrs={'disabled':True}),
            # 'born_female': forms.TextInput(attrs={'disabled':True}),
            # 'born_total': forms.TextInput(attrs={'disabled':True}),
            # 'litter_weight_birth': forms.TextInput(attrs={'disabled':True}),
            # 'weaned_male': forms.TextInput(attrs={'disabled':True}),
            # 'weaned_female': forms.TextInput(attrs={'disabled':True}),
            # 'total_weaned': forms.TextInput(attrs={'disabled':True}),
            # 'weaning_weight': forms.TextInput(attrs={'disabled':True}),
            # 'still_birth_abnormality': forms.TextInput(attrs={'disabled':True}),
            # 'date_of_abortion':forms.TextInput(attrs={'disabled':True}),
        }
