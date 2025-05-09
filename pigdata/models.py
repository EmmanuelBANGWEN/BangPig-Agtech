from django.db import models
from django.contrib.auth.models import User

class general_identification_and_parentage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associer l'utilisateur

    animal_id=models.CharField(max_length=20)
    dob=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=8, choices=(('Male','Male'),('Female','Female')), default='Male')
    breed=models.CharField(max_length=20, blank=True, null=True)
    dam_no=models.CharField(max_length=20, blank=True, null=True)
    sire_no=models.CharField(max_length=20, blank=True, null=True)
    grand_dam=models.CharField(max_length=20, blank=True, null=True)
    grand_sire=models.CharField(max_length=20, blank=True, null=True)
    colitter_size_of_birth=models.IntegerField(null=True, blank=True)
    color_and_marking=models.TextField(blank=True, null=True)
    abnormalities=models.CharField(max_length=3, choices=(('yes','yes'),('no','no')), default='no')
    
    class Meta:
        unique_together = ('user', 'animal_id')  # Empêcher les doublons pour un même utilisateur
        # unique_together = ['user']  # Empêcher les doublons pour un même utilisateur


    def __str__(self):
        return f"{self.animal_id} ({self.user.username})"


    



class health_parameter_vaccination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    gip = models.ForeignKey(general_identification_and_parentage, on_delete=models.CASCADE)
    disease=models.CharField(max_length=50, blank=True)
    make=models.CharField(max_length=20, blank=True)
    first_dose=models.DateField(blank=True,null=True)
    booster_dose=models.DateField(blank=True,null=True)
    repeat=models.DateField(blank=True,null=True)
    
    # def __str__(self):
    #     return f"{self.gip}"

class health_parameter_vetexam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    gip = models.ForeignKey(general_identification_and_parentage, on_delete=models.CASCADE)
    reason=models.TextField(blank=True)
    date_of_treatment=models.DateField(blank=True,null=True)
    medication=models.TextField(blank=True)
    remarks=models.TextField(blank=True)
       
    # def __str__(self):
    #     return f"{self.gip}"


class disposal_culling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.OneToOneField(general_identification_and_parentage, on_delete=models.CASCADE)
    reason=models.TextField(blank=True)
    sale_date=models.DateField(blank=True,null=True)
    weight_sale=models.IntegerField(blank=True, null=True)
    revenue=models.IntegerField(blank=True, null=True)
           
    # def __str__(self):
    #     return f"{self.gip}"

        
class nutrition_and_feeding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.ForeignKey(general_identification_and_parentage, on_delete=models.CASCADE)
    treatment=models.TextField(blank=True)
    make=models.TextField(blank=True)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    remarks=models.TextField(blank=True)
           
    # def __str__(self):
    #     return f"{self.gip}"

        
# class economics(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

#     gip = models.OneToOneField(general_identification_and_parentage, on_delete=models.CASCADE)
#     book_value=models.IntegerField(blank=True, null=True)
#     amount_realized =models.IntegerField(blank=True, null=True)
    
class death(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.OneToOneField(general_identification_and_parentage, on_delete=models.CASCADE)
    date_death=models.DateField(blank=True,null=True)
    postmortem_findings=models.TextField(blank=True)
    cause_death=models.TextField(blank=True)
       
    # def __str__(self):
    #     return f"{self.gip}  ({self.date_death})"

        
class efficiency_parameter_male(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.OneToOneField(general_identification_and_parentage, on_delete=models.CASCADE)
    dow=models.DateField(blank=True,null=True)
    weaning_age=models.IntegerField(blank=True, null=True)
    weaning_weight=models.IntegerField(blank=True, null=True)
    litter_size_weaning=models.IntegerField(blank=True, null=True)
    dos=models.DateField(blank=True,null=True)
    doc=models.DateField(blank=True,null=True)
    dosm=models.DateField(blank=True,null=True)
    sexual_maturity_weight=models.IntegerField(blank=True, null=True)
    weight_six=models.IntegerField(blank=True, null=True)
    weight_eight=models.IntegerField(blank=True, null=True)
    conform_at_eight=models.TextField(blank=True, null=True)
       
    # def __str__(self):
    #     return f"{self.gip}"

        
class efficiency_parameter_female(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.OneToOneField(general_identification_and_parentage, on_delete=models.CASCADE)
    dow=models.DateField(blank=True,null=True)
    weaning_age=models.IntegerField(blank=True, null=True)
    weaning_weight=models.IntegerField(blank=True, null=True)
    litter_size_weaning=models.IntegerField(blank=True, null=True)
    dos=models.DateField(blank=True,null=True)
    dosm=models.DateField(blank=True,null=True)
    sexual_maturity_weight=models.IntegerField(blank=True, null=True)
    weight_six=models.IntegerField(blank=True, null=True)
    weight_eight=models.IntegerField(blank=True, null=True)
    conform_at_eight=models.TextField(blank=True, null=True)
       
    # def __str__(self):
    #     return f"{self.gip}"

        
class qualification_boar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.OneToOneField(general_identification_and_parentage, on_delete=models.CASCADE)
    physical_fitness=models.CharField(max_length=10,choices=(('Poor','Poor'),('Good','Good'),('Very Good','Very Good'),('Excellent','Excellent')), default='Good')
    date_of_training=models.DateField(blank=True,null=True)
    period_of_training=models.IntegerField(blank=True, null=True)
    training_score=models.CharField(max_length=10,choices=(('Poor','Poor'),('Good','Good'),('Very Good','Very Good'), ('Excellent','Excellent')), default='Good')
    seminal_characteristics=models.CharField(max_length=10,choices=(('Poor','Poor'),('Good','Good'),('Very Good','Very Good'),('Excellent','Excellent')), default='Good')
    suitability=models.CharField(max_length=10,choices=(('yes','yes'), ('no','no')), default='no')
           
    # def __str__(self):
    #     return f"{self.gip}"

        

class service_record_male(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    gip = models.ForeignKey(general_identification_and_parentage, on_delete=models.CASCADE)
    sow_no=models.CharField(max_length=20, blank=True)
    dos=models.DateField(blank=True,null=True)
    dof=models.DateField(blank=True,null=True)
    parity=models.IntegerField(blank=True, null=True)
    born_male=models.IntegerField(blank=True, null=True)
    born_female=models.IntegerField(blank=True, null=True)
    born_total=models.IntegerField(blank=True, null=True)
    litter_weight_birth=models.IntegerField(blank=True, null=True)
    weaned_male=models.IntegerField(blank=True, null=True)
    weaned_female=models.IntegerField(blank=True, null=True)
    total_weaned=models.IntegerField(blank=True, null=True)
    weaning_weight=models.IntegerField(blank=True, null=True)
    still_birth_abnormality=models.IntegerField(blank=True, null=True)
       
    # def __str__(self):
    #     return f"{self.gip}"

        
class service_record_female(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    gip = models.ForeignKey(general_identification_and_parentage, on_delete=models.CASCADE)
    parity=models.IntegerField(blank=True, null=True)
    boar_no=models.CharField(max_length=20, blank=True)
    dos=models.DateField(blank=True,null=True)
    nos=models.TextField(blank=True)
    dof=models.DateField(blank=True,null=True)
    dow=models.DateField(blank=True,null=True)
    interfarrowing_interval=models.IntegerField(blank=True, null=True)
    born_male=models.IntegerField(blank=True, null=True)
    born_female=models.IntegerField(blank=True, null=True)
    born_total=models.IntegerField(blank=True, null=True)
    still_birth_abnormality=models.IntegerField(blank=True, null=True)
    litter_weight_birth=models.IntegerField(blank=True, null=True)
    weaned_male=models.IntegerField(blank=True, null=True)
    weaned_female=models.IntegerField(blank=True, null=True)
    total_weaned=models.IntegerField(blank=True, null=True)
    weaning_weight=models.IntegerField(blank=True, null=True)
    date_of_abortion=models.DateField(blank=True,null=True)
       
    # def __str__(self):
    #     return f"{self.gip}"

        
class lifetime_litter_character(models.Model):
    no_litter_born=models.IntegerField(blank=True, null=True)
    litter_weight_birth=models.IntegerField(blank=True, null=True)
    no_weaning=models.IntegerField(blank=True, null=True)
    weight_weaning=models.IntegerField(blank=True, null=True)
    preweaning_mortality=models.IntegerField(blank=True, null=True)
           
    def __str__(self):
        return f"{self.gip}"

        

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f"Message de {self.name} - {self.email}"




import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True, blank=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Ajout du champ de validation

    def generate_new_code(self):
        """ Génère un code unique sans l'activer immédiatement """
        self.code = uuid.uuid4().hex[:12].upper()
        self.expires_at = now() + timedelta(days=30)
        self.is_active = False  # Le code doit être activé manuellement
        self.save()

    def activate(self):
        """ Active l'abonnement une fois validé par l'admin """
        self.is_active = True
        self.save()

    def is_valid(self):
        """ Vérifie si le code est valide et activé """
        return self.is_active and self.expires_at and self.expires_at > now()

    def __str__(self):
        return f"{self.user.username} - Expire le {self.expires_at} - Actif: {self.is_active}"
