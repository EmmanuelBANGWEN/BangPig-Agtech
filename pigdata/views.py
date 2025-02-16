from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from datetime import date, timedelta
from django.contrib import messages
from django.http import HttpResponse
from django.db import IntegrityError
from datetime import datetime
from django.db.models import Sum
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.mail import send_mail, EmailMessage
from django.conf import settings




#
#
#-----------------------------------------------------------------------------------------------------------------------------------
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirection si l'utilisateur est déjà connecté
    form = loginuserform()  # Création d'un formulaire de connexion
    if request.method=='POST':
        form=loginuserform(request.POST) # Récupération des données soumises
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Connexion de l'utilisateur
                return redirect("index")  # Redirection vers la page d'accueil
            else:
                messages.error(request, 'username or password is incorrect')

    context={'form': form
    ,'tablename':'Login'}
    return render(request, "account/login.html", context)

def logoutuser(request):
    logout(request)  # Déconnexion de l'utilisateur
    return redirect('loginuser')  # Redirection vers la page de connexion

# def registeruser(request):
#     if request.user.is_authenticated:
#        return redirect('index')  # Redirection si l'utilisateur est déjà connecté
#     form = CreateUserForm()  # Création d'un formulaire d'inscription
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)  # Récupération des données soumises
#         if form.is_valid():
#             form.save()  # Enregistrement du nouvel utilisateur
#             return redirect('loginuser')  # Redirection vers la page de connexion
#     context = {'form': form, 'tablename': 'Register'}
#     return render(request, "account/register.html", context)



from django.contrib.auth import authenticate, login


def registeruser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user)
            return redirect('loginuser')
        else:
            return render(request, 'account/register.html', {'form': form })
    else:
        form = CreateUserForm()
        return render(request, 'account/register.html', {'form':form})


 

#--------------------------------------------------------------------------------------------------------------------------------------













from django.http import HttpResponseForbidden

def subscription_required(view_func):
    """ Vérifie si l'utilisateur a un abonnement actif """
    def _wrapped_view(request, *args, **kwargs):
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        if not subscription.is_valid():
            return HttpResponseForbidden("Votre abonnement a expiré. Veuillez entrer un nouveau code.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


#---------------------------------------------------------------------------------------------------------------------------------------
@subscription_required
def dataentry(request):  #entrer les donnees
    return render(request, "action/dataentry.html", context={'tablename':'Que Voulez-Vous faire ?'})
@subscription_required
def report(request):  
    return render(request, "others/report.html", context={'tablename':'Mes Enregistrements'})
















@subscription_required
@login_required(login_url='loginuser')
def delete(request, animal_id):
    try:
        animal = general_identification_and_parentage.objects.get(animal_id=animal_id, user=request.user)
        animal.delete()
        messages.success(request, "L'animal a été supprimé avec succès.")
    except general_identification_and_parentage.DoesNotExist:
        messages.error(request, "Cet animal n'existe pas ou ne vous appartient pas.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@subscription_required
@login_required(login_url='loginuser')
def deletepigs(request):              #Affiche une page où les animaux dun user sont listés et permettent de choisir ceux à supprimer.
    animals=general_identification_and_parentage.objects.filter(user=request.user)
    context={
        'animals':animals,
        'tablename':'Supprimer Un Porc',
    }
    return render(request, "action/deletepigs.html", context)


@subscription_required
@login_required(login_url='loginuser')
def delete_service(request, animal_id, pk):  # Supprime un service en fonction du genre de l'animal.
    if request.method == 'POST':
        backbutton = request.POST.get('backbutton')
        animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

        
        # Vérifier si l'animal est mâle ou femelle et supprimer le service correspondant
        if animal.gender == 'Male':
            service = service_record_male.objects.filter(gip=animal, pk=pk).first()
        else:
            service = service_record_female.objects.filter(gip=animal, pk=pk).first()
        
        # Supprimer l'objet s'il existe
        if service:
            service.delete()
        
        # Redirection sécurisée
        return redirect(backbutton if backbutton else 'default_page')  # Remplace 'default_page' par l'URL de ton choix


@subscription_required
@login_required(login_url='loginuser')
def delete_vaccination(request, animal_id, pk):
    if request.method == 'POST':
        backbutton = request.POST.get('backbutton')
        animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

        vacc = health_parameter_vaccination.objects.filter(gip=animal, pk=pk).first()
        
        if vacc:  # Vérifie si l'objet existe avant de le supprimer
            vacc.delete()  # Suppression de la vaccination
        
        return redirect(backbutton)

@subscription_required
@login_required(login_url='loginuser')
def delete_vetexam(request, animal_id, pk):
    if request.method == 'POST':
        backbutton = request.POST.get('backbutton')
        animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

        
        # Récupérer l'examen vétérinaire de manière sécurisée
        vet = health_parameter_vetexam.objects.filter(gip=animal, pk=pk).first()
        
        # Vérifier si l'objet existe avant de le supprimer
        if vet:
            vet.delete()
        
        # Redirection sécurisée
        return redirect(backbutton if backbutton else 'default_page')  # Remplace 'default_page' par une URL par défaut

@subscription_required
@login_required(login_url='loginuser')
def delete_nutrition(request, animal_id, pk):
    if request.method == 'POST':
        backbutton = request.POST.get('backbutton')
        animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

        
        # Récupérer l'enregistrement nutritionnel de manière sécurisée
        nutrition = nutrition_and_feeding.objects.filter(gip=animal, pk=pk).first()
        
        # Vérifier si l'objet existe avant de le supprimer
        if nutrition:
            nutrition.delete()
        
        # Redirection sécurisée
        return redirect(backbutton if backbutton else 'default_page')  # Remplace 'default_page' par une URL de secours


#Ces fonctions permettent de supprimer des enregistrements spécifiques associés à un animal en utilisant leurs identifiants.









































#-----------------------------------------------------------------------------------------------------------------------------------------------

@subscription_required
@login_required(login_url='loginuser')
def dbsuccess(request):    #dbsuccess : Renvoie un template dbsuccess.html avec un contexte indiquant que l'opération a été un succès.
    return render(request, "action/dbsuccess.html", context={'tablename':'Success'})

# 
# @subscription_required
# @login_required(login_url='loginuser')
# def index(request):
#     # Total des animaux enregistrés
#     total_animals = general_identification_and_parentage.objects.filter(user=request.user).count()
    
#     # Nombre de femelles
#     total_females = general_identification_and_parentage.objects.filter(user=request.user, gender='Female').count()
    
#     # Nombre de mâles
#     total_males = general_identification_and_parentage.objects.filter(user=request.user, gender='Male').count()
    
#     # Nombre de porcelets (hypothèse : âge < 6 mois)
#     six_months_ago = date.today() - timedelta(days=6*30)
#     total_piglets = general_identification_and_parentage.objects.filter(user=request.user, dob__gte=six_months_ago).count()
    
#     context = {
#         'total_animals': total_animals,
#         'total_females': total_females,
#         'total_males': total_males,
#         'total_piglets': total_piglets,
#     }
#     return render(request, "index.html", context)


import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Count, Sum
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import general_identification_and_parentage, health_parameter_vaccination
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from collections import defaultdict
import pandas as pd

def index(request):
    # Vérifier si des données existent pour éviter l'erreur
    population_sexe = list(general_identification_and_parentage.objects.filter(user=request.user).values('gender').annotate(total=Count('id')))
    
    if not population_sexe:  # Si aucun animal n'est enregistré
        population_sexe = [{'gender': 'Male', 'total': 0}, {'gender': 'Female', 'total': 0}]

    fig_population = px.bar(
        population_sexe, x='gender', y='total', title="Répartition des animaux par sexe"
    )

    # Vérification pour population_mois
    population_mois = list(general_identification_and_parentage.objects.filter(user=request.user).extra(
        {'mois': "strftime('%%Y-%%m', dob)"}  # SQLite
    ).values('mois').annotate(total=Count('id')))

    if not population_mois:
        population_mois = [{'mois': '0000-00', 'total': 0}]  # Valeur par défaut

    fig_evolution_population = px.line(
        population_mois, x='mois', y='total', title="Évolution du nombre d'animaux enregistrés"
    )

    # Vérification pour vaccins
    vaccins = list(health_parameter_vaccination.objects.filter(user=request.user).values('disease').annotate(total=Count('id')))
    if not vaccins:
        vaccins = [{'disease': 'Aucun', 'total': 0}]

    fig_vaccins = px.pie(
        vaccins, names='disease', values='total', title="Répartition des vaccins par maladie"
    )

    # Vérification pour vaccinations
    vaccinations = list(health_parameter_vaccination.objects.filter(user=request.user).values('disease', 'first_dose', 'booster_dose'))
    
    fig_vaccination_doses = go.Figure()
    if not vaccinations:
        fig_vaccination_doses.add_trace(go.Bar(
            x=['Aucun'], y=[0], name='Première dose'
        ))
    
    for v in vaccinations:
        fig_vaccination_doses.add_trace(go.Bar(
            x=[v['disease']], y=[1], name='Première dose'
        ))
        if v['booster_dose']:
            fig_vaccination_doses.add_trace(go.Bar(
                x=[v['disease']], y=[1], name='Booster dose'
            ))

    # Vérification pour total_animals
    total_animals = general_identification_and_parentage.objects.filter(user=request.user).count()
    total_females = general_identification_and_parentage.objects.filter(user=request.user, gender='Female').count()
    total_males = general_identification_and_parentage.objects.filter(user=request.user, gender='Male').count()
    
    six_months_ago = date.today() - timedelta(days=6*30)
    total_piglets = general_identification_and_parentage.objects.filter(user=request.user, dob__gte=six_months_ago).count()

    context = {
        'total_animals': total_animals,
        'total_females': total_females,
        'total_males': total_males,
        'total_piglets': total_piglets,
        'fig_population': fig_population.to_html(),
        'fig_evolution_population': fig_evolution_population.to_html(),
        'fig_vaccins': fig_vaccins.to_html(),
        'fig_vaccination_doses': fig_vaccination_doses.to_html(),
    }

    return render(request, 'index.html', context)






@subscription_required
@login_required(login_url='loginuser')

def create_general(request):
    form=general_form()  # Création d'un formulaire vierge pour la création d'un animal
    if request.method=='POST':
        form=general_form(request.POST)  #  Remplissage du formulaire avec les données envoyées
        if form.is_valid():
            animal_id=str(form.cleaned_data['animal_id'])
            # Vérifie si l'animal existe déjà
            if not general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).exists():
                obj = form.save(commit=False)
                obj.user = request.user  # Associer l'utilisateur connecté
                obj.save()  # Sauvegarde du formulaire si l'animal n'existe pas
                return redirect('create_efficiency',animal_id)  # Redirection pour enregistrer des données d'efficacité
            else:
                messages.error(request, 'animal already exists')

    context={
        'form':form,
        'tablename': 'Identification Générale et Parenté'
    }

    return render(request,"create/create_general.html",context)
#Cette fonction permet de créer un nouvel enregistrement d'animal en utilisant un formulaire general_form.
#Elle vérifie d'abord si l'animal existe déjà dans la base de données en utilisant l'identifiant animal_id. Si ce n'est pas le cas, elle sauvegarde les données.
#En cas de succès, l'utilisateur est redirigé vers create_efficiency pour saisir des paramètres d'efficacité.


@subscription_required
@login_required(login_url='loginuser')
def create_efficiency(request, animal_id):
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
    gender = animal.gender  # Récupération du genre de l'animal
    
    if gender == 'Male':
        form = efficiency_form_male(initial={'gip': animal})  # Formulaire spécifique pour un mâle
        if request.method == 'POST':    
            form = efficiency_form_male(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)

                # Vérifie si dow est renseigné avant de calculer weaning_age
                if instance.dow:
                    agevar = instance.dow - instance.gip.dob  
                    instance.weaning_age = agevar.days
                else:
                    instance.weaning_age = None  # Ne pas calculer si dow est vide
                
                instance.user = request.user
                instance.save()
                return redirect('create_qualification', animal_id=animal_id)
                
        context = {
            'form': form,
            'tablename': 'Paramètre Efficacité Male'
        }
        return render(request, "create/create_efficiency_male.html", context)

    elif gender == 'Female':
        form = efficiency_form_female(initial={'gip': animal})
        if request.method == 'POST':    
            form = efficiency_form_female(request.POST)  # Formulaire spécifique pour une femelle
            if form.is_valid():
                instance = form.save(commit=False)

                # Vérifie si dow est renseigné avant de calculer weaning_age
                if instance.dow:
                    agevar = instance.dow - instance.gip.dob  
                    instance.weaning_age = agevar.days
                else:
                    instance.weaning_age = None  # Ne pas calculer si dow est vide
                
                instance.user = request.user
                instance.save()
                return redirect('create_qualification', animal_id=animal_id)
                
        context = {
            'form': form,
            'tablename': 'Paramètre Efficacité Femelle'
        }
        return render(request, "create/create_efficiency_female.html", context)




@subscription_required
@login_required(login_url='loginuser')
def create_qualification(request, animal_id):
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    
    # Vérifier le genre de l'animal et rediriger si c'est une femelle
    if animal.gender == 'Female':
        return redirect('create_service', animal_id=animal_id)

    form = qualification_form(initial={'gip': animal})
    
    if request.method == 'POST':
        form = qualification_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('create_service', animal_id=animal_id)

    context = {
        'form': form,
        'tablename': 'Qualification As Breeding Boar'
    }

    return render(request, "create/create_qualification.html", context)

# Gère la création des qualifications pour les mâles. Les femelles passent directement à la création des services.



@subscription_required
@login_required(login_url='loginuser')
def create_service(request, animal_id):
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
        
    # Déterminer le modèle et le formulaire en fonction du genre
    if animal.gender == 'Male':
        service_model = service_record_male
        service_form = service_form_male
        template = "create/service_male.html"
    else:
        service_model = service_record_female
        service_form = service_form_female
        template = "create/service_female.html"

    services = service_model.objects.filter(gip=animal)
    form = service_form(initial={'gip': animal})

    if request.method == 'POST':    
        form = service_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
             
            # Calcul des totaux
            instance.born_total = instance.born_female + instance.born_male
            instance.total_weaned = instance.weaned_female + instance.weaned_male
            
            # Associer l'utilisateur connecté
            instance.user = request.user  
            instance.save()
            
            return redirect('create_service', animal_id=animal_id)

    context = {
        'form': form,
        'services': services,
        'gip': animal_id,
        'tablename': 'Enregistrement des Services et Caractères des Portées',
        'backbut': request.build_absolute_uri(),
    }

    return render(request, template, context)

# Enregistre les services (données de reproduction) pour un animal. Le formulaire et le template changent selon le genre de l'animal.
# Calcule les totaux des petits nés et sevrés.




@subscription_required
@login_required(login_url='loginuser')
def vaccination(request, animal_id):
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    vaccinations = health_parameter_vaccination.objects.filter(gip=animal)
    
    form = vaccination_form(initial={'gip': animal})

    if request.method == 'POST':    
        form = vaccination_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user  # Associer l'utilisateur connecté
            instance.save()
            return redirect('vaccination', animal_id=animal_id)

    context = {
        'form': form,
        'vaccinations': vaccinations,
        'gip': animal_id,
        'backbut': request.build_absolute_uri(),
        'tablename': 'Vaccinations'
    }
    return render(request, "create/vaccinationtemplate.html", context)



@subscription_required
@login_required(login_url='loginuser')
def vetexam(request, animal_id):
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    vet_exams = health_parameter_vetexam.objects.filter(gip=animal)
    form = vetexam_form(initial={'gip': animal})

    if request.method == 'POST':    
        form = vetexam_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('vetexam', animal_id=animal_id)

    context = {
        'form': form,
        'vet_exams': vet_exams,
        'gip': animal_id,
        'backbut': request.build_absolute_uri(),
        'tablename': 'Veterinary Exam'
    }

    return render(request, "create/vetexamtemplate.html", context)

@subscription_required
@login_required(login_url='loginuser')
def create_nutrition(request, animal_id):
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    nutritions = nutrition_and_feeding.objects.filter(gip=animal)
    form = nutrition_form(initial={'gip': animal})

    if request.method == 'POST':  
        form = nutrition_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('create_nutrition', animal_id=animal_id)

    context = {
        'tablename': 'Nutrition',
        'form': form,
        'nutritions': nutritions,
        'backbut': request.build_absolute_uri(),
        'gip': animal_id
    }

    return render(request, "create/nutrition_template.html", context)

@subscription_required
@login_required(login_url='loginuser')
def deathview(request, animal_id):
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    form = death_form(initial={'gip': animal})

    if request.method == 'POST':    
        form = death_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('create_nutrition', animal_id=animal_id)

    context = {
        'tablename': 'Information About Death Of Pig',
        'form': form,
    }

    return render(request, "create/create_death.html", context)

@subscription_required
@login_required(login_url='loginuser')
def create_disposal(request, animal_id):
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    form = disposal_form(initial={'gip': animal})

    if request.method == 'POST':    
        form = disposal_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('dbsuccess')

    context = {
        'form': form,
        'tablename': 'Disposal And Culling'
    }

    return render(request, "create/create_disposal.html", context)



# 
@subscription_required
@login_required(login_url='loginuser')
# def create_economics(request, animal_id):
#     # Utilisation de get_object_or_404 pour récupérer l'animal ou renvoyer une erreur 404 si l'animal n'existe pas
#     animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    
#     form = economics_form(initial={'gip': animal})
    
#     if request.method == 'POST':
#         form = economics_form(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user  # Associer l'utilisateur connecté
#             obj.save()
#             return redirect('dbsuccess')  # Rediriger vers une page de succès
    
#     context = {
#         'form': form,
#         'tablename': 'Economics'
#     }

#     return render(request, "create/create_economics.html", context)







#-----------------------------------------------------------------------------------------------------------------------------------






@subscription_required
@login_required(login_url='loginuser')
def successupdate(request):
    return render(request,"update/successupdate.html", context={'tablename':'Update Successful'})


@subscription_required
@login_required(login_url='loginuser')
def update(request):
    animal_id = request.POST.get('animal_id') or request.GET.get('animal_id')
    
    # Récupérer l'animal ou None si non trouvé
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    if not animal:
        messages.error(request, "Aucun animal trouvé avec cet ID.")
        return render(request, "action/dataentry.html", {'tablename': 'Mise à Jour des Enregistrements'})

    context = {
        'tablename': 'Mise à Jour des Enregistrements',
        'animal_id': animal_id,
        'gender': animal.gender
    }
    

    # Rendu selon le sexe de l'animal
    if animal.gender == 'Female':
        return render(request, "update/updatefemale.html", context)
    elif animal.gender == 'Male':
        return render(request, "update/updatemale.html", context)

# Update general information


@subscription_required
@login_required(login_url='loginuser')
def update_general(request, animal_id):
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
    
    form = general_update_form(instance=animal)

    if request.method == 'POST':
        form = general_update_form(request.POST, instance=animal)

        try:

            animal.dob = request.POST.get('dob', animal.dob)
            animal.gender = request.POST.get('gender', animal.gender)
            animal.breed = request.POST.get('breed', animal.breed)
            animal.dam_no = request.POST.get('dam_no', animal.dam_no)
            animal.sire_no = request.POST.get('sire_no', animal.sire_no)
            animal.grand_dam = request.POST.get('grand_dam', animal.grand_dam)
            animal.grand_sire = request.POST.get('grand_sire', animal.grand_sire)
            animal.colitter_size_of_birth = request.POST.get('colitter_size_of_birth', animal.colitter_size_of_birth)
            animal.color_and_marking = request.POST.get('color_and_marking', animal.color_and_marking)
            animal.abnormalities = request.POST.get('abnormalities', animal.abnormalities)
 
            animal.save()  # Sauvegarde des modifications
            messages.success(request, "Ne jamais laisser le champ  *Taille de la portée à la naissance*  vide !!!")
        except IntegrityError as e:
            messages.error(request, f"Erreur d'intégrité : {e}")
    
    form = general_update_form(instance=animal)
    context = {
        'form': form,
        'animal_data': animal,
    }
    return render(request, "update/generalupdate.html", context)


@subscription_required
@login_required(login_url='loginuser')
def update_disposal(request, animal_id):
    # Vérifier si l'animal existe et appartient à l'utilisateur
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
    if not animal:
        messages.error(request, "Animal non trouvé ou non accessible.")
        return redirect('error_page')  # Rediriger vers une page d'erreur

    # Récupérer ou créer une instance de disposal_culling pour cet animal
    disposal_instance, created = disposal_culling.objects.get_or_create(gip=animal)

    # Initialiser le formulaire avec l'instance de disposal et l'animal spécifique
    form = disposal_update_form(instance=disposal_instance, specific_animal=animal)

    if request.method == 'POST':
        form = disposal_update_form(request.POST, instance=disposal_instance, specific_animal=animal)
        if form.is_valid():
            
            disposal_instance = form.save(commit=False)
            disposal_instance.user = request.user  # Associer l'utilisateur connecté
            disposal_instance.save()
            messages.success(request, "Mise à jour réussie.")
            return redirect('successupdate')  # Rediriger après la mise à jour
        else:
            messages.error(request, 'username or password is incorrect')
    form = disposal_update_form(instance=disposal_instance, specific_animal=animal)

    context = {
        'form': form,
        'tablename': 'Revenus',
    }
    return render(request, "update/updatedisposal.html", context)

# Update nutrition information

@subscription_required
@login_required(login_url='loginuser')
def update_nutrition(request, animal_id):
    # animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    nutritions = nutrition_and_feeding.objects.filter(gip=animal)
    
    form = nutrition_update_form(initial={'gip': animal}, user=request.user, specific_animal=animal)
    
    if request.method == 'POST':
        form = nutrition_update_form(request.POST, user=request.user, specific_animal=animal)
        try:

            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user  # Associer l'utilisateur connecté
                obj.save()
                # return redirect('update_nutrition', animal_id=animal_id)
        # nutrition = nutrition_and_feeding.objects.filter(gip=animal)
        except IntegrityError as e:
            messages.error(request, f"Erreur d'intégrité : {e}")
      
    form = nutrition_update_form(initial={'gip': animal}, user=request.user, specific_animal=animal)

    context = {
        'tablename': 'Update Nutrition',
        'form': form,
        # 'nutrition':nutrition,
        'nutritions': nutritions,
        'backbut': request.build_absolute_uri(),
        'gip': animal_id
    }
    return render(request, "update/nutrition_update_template.html", context)

# # Update economics information
# 
@subscription_required
@login_required(login_url='loginuser')
# def update_economics(request, animal_id):
#     # Utilisation de get_object_or_404 pour une gestion d'erreur plus propre
#     animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    
#     # Création ou récupération de l'instance economics
#     economics_instance, created = economics.objects.get_or_create(gip=animal)
    
#     form = economics_update_form(instance=economics_instance)
#     if request.method == 'POST':
#         form = economics_update_form(request.POST, instance=economics_instance)
#         if form.is_valid():
#             economics_instance = form.save(commit=False)
#             economics_instance.user = request.user  # Assigner l'utilisateur connecté
#             economics_instance.save()
#             return redirect('successupdate')
#         else:
#             print("Form Errors:", form.errors)  # Debugging
    
#     context = {
#         'form': form,
#         'tablename': 'Economics',
#     }
#     return render(request, "update/updateeconomics.html", context)


# Update efficiency information for male and female animals

@subscription_required
@login_required(login_url='loginuser')
def update_efficiency(request, animal_id):
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    gender = animal.gender

    def calculate_age(dob, dow):
        # Convertir dob et dow en objets datetime.date s'ils sont des chaînes
        if isinstance(dob, str):
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        if isinstance(dow, str):
            dow = datetime.strptime(dow, '%Y-%m-%d').date()
        
        # Calculer l'âge en jours
        wa = (dow - dob).days
        # print(wa)
        if not dob or not dow:
            return 0  # ou une autre valeur par défaut

        return wa


    if gender == 'Male':
        # Récupérer ou créer l'instance pour les mâles
        animal_efficiency, created = efficiency_parameter_male.objects.get_or_create(gip=animal)
        form = efficiency_update_form_male(instance=animal_efficiency)
        
        if request.method == 'POST':
            form = efficiency_update_form_male(request.POST, instance=animal_efficiency)
            # if form.is_valid():

            try:

                    if not animal_efficiency.weaning_weight:                
                        animal_efficiency.weaning_weight = request.POST.get('weaning_weight', 0)  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.weaning_weight = request.POST.get('weaning_weight', animal_efficiency.weaning_weight)


                    if not animal_efficiency.litter_size_weaning:                
                        animal_efficiency.litter_size_weaning = request.POST.get('litter_size_weaning', 0)  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.litter_size_weaning = request.POST.get('litter_size_weaning', animal_efficiency.litter_size_weaning)


                    if not animal_efficiency.sexual_maturity_weight:                
                        animal_efficiency.sexual_maturity_weight = request.POST.get('sexual_maturity_weight', 0)  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.sexual_maturity_weight = request.POST.get('sexual_maturity_weight', animal_efficiency.sexual_maturity_weight)


                    if not animal_efficiency.sexual_maturity_weight:                
                        animal_efficiency.weight_six = request.POST.get('weight_six', 0)  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.weight_six = request.POST.get('weight_six', animal_efficiency.weight_six)



                    if not animal_efficiency.sexual_maturity_weight:                
                        animal_efficiency.weight_eight = request.POST.get('weight_eight', 0)  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.weight_eight = request.POST.get('weight_eight', animal_efficiency.weight_eight)



                    if not animal_efficiency.sexual_maturity_weight:                
                        animal_efficiency.conform_at_eight = request.POST.get('conform_at_eight', str(animal_efficiency.conform_at_eight))  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.conform_at_eight = request.POST.get('conform_at_eight', animal_efficiency.conform_at_eight)


                    if not animal_efficiency.dow:                
                        animal_efficiency.dow = request.POST.get('dow', None)  # Valeur par défaut 0 si vide
                    else:
                        animal_efficiency.dow = request.POST.get('dow', animal_efficiency.dow)


                    dos = request.POST.get('dos', str(animal_efficiency.dos))
                    if dos:
                        try:
                            dos = datetime.strptime(dos, '%Y-%m-%d').date()
                        except ValueError:
                            dos = None
                    animal_efficiency.dos = dos if dos else None


                    doc = request.POST.get('doc', str(animal_efficiency.doc))
                    if doc:
                        try:
                            doc = datetime.strptime(doc, '%Y-%m-%d').date()
                        except ValueError:
                            doc = None
                    animal_efficiency.doc = doc if doc else None

                    dosm = request.POST.get('dosm', str(animal_efficiency.dosm))
                    if dosm:
                        try:
                            dosm = datetime.strptime(dosm, '%Y-%m-%d').date()
                        except ValueError:
                            dosm = None
                    animal_efficiency.dosm = dosm if dosm else None



                    dob = animal_efficiency.gip.dob if animal_efficiency.gip else None
                    dow = animal_efficiency.dow

                    # Si les deux valeurs sont présentes, on calcule l'âge, sinon on laisse l'âge comme None
                    animal_efficiency.weaning_age = calculate_age(dob, dow) if dob and dow else None


                    animal_efficiency.save()
                    messages.success(request, "Mise à jour réussie.")

                    # return redirect('successupdate')
            except IntegrityError as e:
                messages.error(request, f"Erreur d'intégrité : {e}")
        
        form = efficiency_update_form_male(instance=animal_efficiency)

        context = {
            'form': form,
            'animal_efficiency':animal_efficiency,
            'animal_data': animal,

            'tablename': 'Paramètre Efficacité'
        }

        return render(request, "update/update_efficiency_male.html", context)
    
    elif gender == 'Female':
        
        # Récupérer ou créer l'instance pour les mâles
        animal_efficiency, created = efficiency_parameter_female.objects.get_or_create(gip=animal)
        form = efficiency_update_form_female(instance=animal_efficiency)
        
        if request.method == 'POST':
            form = efficiency_update_form_female(request.POST, instance=animal_efficiency)
            # if form.is_valid():

            
            try:

                
                if not animal_efficiency.weaning_weight:                
                    animal_efficiency.weaning_weight = request.POST.get('weaning_weight', 0)  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.weaning_weight = request.POST.get('weaning_weight', animal_efficiency.weaning_weight)


                if not animal_efficiency.litter_size_weaning:                
                    animal_efficiency.litter_size_weaning = request.POST.get('litter_size_weaning', 0)  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.litter_size_weaning = request.POST.get('litter_size_weaning', animal_efficiency.litter_size_weaning)


                if not animal_efficiency.sexual_maturity_weight:                
                    animal_efficiency.sexual_maturity_weight = request.POST.get('sexual_maturity_weight', 0)  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.sexual_maturity_weight = request.POST.get('sexual_maturity_weight', animal_efficiency.sexual_maturity_weight)


                if not animal_efficiency.sexual_maturity_weight:                
                    animal_efficiency.weight_six = request.POST.get('weight_six', 0)  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.weight_six = request.POST.get('weight_six', animal_efficiency.weight_six)



                if not animal_efficiency.sexual_maturity_weight:                
                    animal_efficiency.weight_eight = request.POST.get('weight_eight', 0)  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.weight_eight = request.POST.get('weight_eight', animal_efficiency.weight_eight)



                if not animal_efficiency.sexual_maturity_weight:                
                    animal_efficiency.conform_at_eight = request.POST.get('conform_at_eight', str(animal_efficiency.conform_at_eight))  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.conform_at_eight = request.POST.get('conform_at_eight', animal_efficiency.conform_at_eight)

                if not animal_efficiency.dow:                
                    animal_efficiency.dow = request.POST.get('dow', None)  # Valeur par défaut 0 si vide
                else:
                    animal_efficiency.dow = request.POST.get('dow', animal_efficiency.dow)

                # Répéter le même processus pour les autres champs de date
                dos = request.POST.get('dos', str(animal_efficiency.dos))
                if dos:
                    try:
                        dos = datetime.strptime(dos, '%Y-%m-%d').date()
                    except ValueError:
                        dos = None
                animal_efficiency.dos = dos if dos else None



                dosm = request.POST.get('dosm', str(animal_efficiency.dosm))
                if dosm:
                    try:
                        dosm = datetime.strptime(dosm, '%Y-%m-%d').date()
                    except ValueError:
                        dosm = None
                animal_efficiency.dosm = dosm if dosm else None



                dob = animal_efficiency.gip.dob if animal_efficiency.gip else None
                dow = animal_efficiency.dow

                # Si les deux valeurs sont présentes, on calcule l'âge, sinon on laisse l'âge comme None
                animal_efficiency.weaning_age = calculate_age(dob, dow) if dob and dow else None


                animal_efficiency.save()
                messages.success(request, "Mise à jour réussie.")

                    # return redirect('successupdate')
            except IntegrityError as e:
                messages.error(request, f"Erreur d'intégrité : {e}")
        
        form = efficiency_update_form_female(instance=animal_efficiency)

        context = {
            'form': form,
            'animal_efficiency':animal_efficiency,
            'animal_data': animal,

            'tablename': 'Paramètre Efficacité'
        }


        return render(request, "update/update_efficiency_female.html", context)



# Update qualification as a breeding boar

@subscription_required
@login_required(login_url='loginuser')
def update_qualification(request, animal_id):
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()

    qualification_instance, created = qualification_boar.objects.get_or_create(gip=animal)
    form = qualification_update_form(instance=qualification_instance)
    
    if request.method == 'POST':
        form = qualification_update_form(request.POST)
        messages.warning(request, "Ne jamais laisser le champ  *Periode d'entrainement*  vide !!!")

        try:
            if form.is_valid():

                # qualification_instance.gip = request.POST.get('gip', qualification_instance.gip)
                qualification_instance.physical_fitness = request.POST.get('physical_fitness', qualification_instance.physical_fitness)
                
                date_of_training = request.POST.get('date_of_training', str(qualification_instance.date_of_training))
                if date_of_training:
                    try:
                        date_of_training = datetime.strptime(date_of_training, '%Y-%m-%d').date()
                    except ValueError:
                        date_of_training = None
                qualification_instance.date_of_training = date_of_training if date_of_training else None
                
                # qualification_instance.date_of_training = request.POST.get('date_of_training', qualification_instance.date_of_training)
                

                if not qualification_instance.period_of_training:                
                    qualification_instance.period_of_training = request.POST.get('period_of_training', 0)  # Valeur par défaut 0 si vide
                else:
                    qualification_instance.period_of_training = request.POST.get('period_of_training', qualification_instance.period_of_training)

                # qualification_instance.period_of_training = request.POST.get('period_of_training', qualification_instance.period_of_training)
                qualification_instance.training_score = request.POST.get('training_score', qualification_instance.training_score)
                qualification_instance.seminal_characteristics = request.POST.get('seminal_characteristics', qualification_instance.seminal_characteristics)
                qualification_instance.suitability = request.POST.get('suitability', qualification_instance.suitability)
                
                qualification_instance.save()  # Sauvegarde des modifications
                messages.success(request, "Mise à jour réussie.")
        except IntegrityError as e:
            messages.error(request, f"Erreur d'intégrité : {e}")
    
    form = qualification_update_form(instance=qualification_instance)
    
    context = {
        'form': form,
        'animal_data': animal,
        'qualification_instance': qualification_instance,

        'tablename': 'Qualification As A Breeding Boar'
    }

    return render(request, "update/qualifications_update.html", context)



@subscription_required
@login_required(login_url='loginuser')
def update_death(request, animal_id):
    # Vérifier si l'animal existe et appartient à l'utilisateur connecté
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
    if not animal:
        messages.error(request, "Animal non trouvé ou non accessible.")
        return redirect('error_page')  # Rediriger vers une page d'erreur appropriée

    # Récupérer ou créer l'instance `death` associée
    death_instance, created = death.objects.get_or_create(gip=animal)

    if request.method == 'POST':
        # Traiter les données soumises
        form = death_form(request.POST, instance=death_instance, specific_animal=animal)
        try:
            if form.is_valid():
                # Sauvegarder l'instance du formulaire
                death_instance = form.save(commit=False)
                # death_instance.user = request.user  # Associer l'utilisateur connecté
                death_instance.cause_death = request.POST.get('cause_death', death_instance.cause_death)
                # death_instance.date_death = request.POST.get('date_death', death_instance.date_death)
            

                date_death = request.POST.get('date_death', str(death_instance.date_death))
                if date_death:
                    try:
                        date_death = datetime.strptime(date_death, '%Y-%m-%d').date()
                    except ValueError:
                        date_death = None
                death_instance.date_death = date_death if date_death else None

                
                death_instance.postmortem_findings = request.POST.get('postmortem_findings', death_instance.postmortem_findings)

                death_instance.save()
                messages.success(request, "Mise à jour réussie.")
                # return redirect('successupdate')  # Rediriger après la mise à jour réussie
        except IntegrityError as e:
            messages.error(request, f"Erreur d'intégrité : {e}")

    # Initialiser le formulaire avec les données de l'instance
    form = death_form(instance=death_instance, specific_animal=animal)
    context = {
        'form': form,
        'animal_data': animal,
        'tablename': 'Death',
    }
    return render(request, "update/updatedeath.html", context)









# Update service record

@subscription_required
@login_required(login_url='loginuser')
def update_service(request, animal_id):
    # Récupérer l'animal correspondant à l'utilisateur et à l'ID
    animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
    if not animal:
        return HttpResponse("Animal not found or unauthorized", status=404)

    gender = animal.gender

    # Déterminer le modèle et le formulaire en fonction du genre de l'animal
    if gender == 'Female':
        service_model = service_record_female
        # service_form = service_update_form_female
        service_form = service_update_form_female
        template = "update/service_update_female.html"

    elif gender == 'Male':
        service_model = service_record_male
        service_form = service_update_form_male
        template = "update/service_update_male.html"

    else:
        return HttpResponse("Invalid gender", status=400)

    # Récupérer les services existants pour l'animal
    services = service_model.objects.filter(gip=animal)

    # Préparer le formulaire
    form = service_form(user=request.user, specific_animal=animal)

    if request.method == 'POST':
        form = service_form(request.POST, user=request.user, specific_animal=animal)
        if form.is_valid():
            instance = form.save(commit=False)
            born_total = instance.born_female + instance.born_male
            weaned_total = instance.weaned_female + instance.weaned_male
            instance.total_weaned = weaned_total
            instance.born_total = born_total
            instance.user = request.user
            instance.save()
            return redirect('update_service', animal_id=animal_id)
    form = service_form(user=request.user, specific_animal=animal)

    context = {
        'form': form,
        'services': services,
        'gip': animal_id,
        'backbut': request.build_absolute_uri(),
        'tablename': 'Enregistrement des Services et Caractères des Portées',
    }
    return render(request, template, context)



# Fonction générique pour mettre à jour les paramètres de santé
def update_health_parameter(request, animal_id, model_class, form_class, template_name, tablename):
    # Récupérer l'animal de l'utilisateur actuel
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    
    # Récupérer les paramètres de santé existants pour l'animal
    health_parameters = model_class.objects.filter(gip=animal)
    
    # Initialiser le formulaire avec les données de l'animal
    form = form_class(initial={'gip': animal}, user=request.user, specific_animal=animal)
    
    if request.method == 'POST':
        form = form_class(request.POST, user=request.user, specific_animal=animal)
        if form.is_valid():
            # Enregistrer les données du formulaire
            obj = form.save(commit=False)
            obj.user = request.user  # Assigner l'utilisateur connecté
            obj.save()
            # return redirect('update_health_parameter', animal_id=animal_id)
    
    vet_exams = model_class.objects.filter(gip=animal)
    vaccinations = model_class.objects.filter(gip=animal)
    form = form_class(initial={'gip': animal}, user=request.user, specific_animal=animal)

    context = {
        'form': form,
        'health_parameters': health_parameters,
        'vet_exams': vet_exams,
        'vaccinations': vaccinations,
        'gip': animal_id,
        'backbut': request.build_absolute_uri(),
        'tablename': tablename
    }


    return render(request, template_name, context)

# Vue pour mettre à jour la vaccination

@subscription_required
@login_required(login_url='loginuser')
def update_vaccination(request, animal_id):
    return update_health_parameter(
        request, 

        animal_id, 
        health_parameter_vaccination, 
        vaccination_update_form, 
        "update/vaccination_update_template.html",

        "Vaccinations"
    )

# Vue pour mettre à jour l'examen vétérinaire

@subscription_required
@login_required(login_url='loginuser')
def update_vetexam(request, animal_id):
    return update_health_parameter(
        request, 
        animal_id, 
        health_parameter_vetexam, 
        vetexam_update_form, 
        "update/vetexam_update_template.html", 
        "Veterinary Exam"
    )
#-----------------------------------------------------------------------------------------------------------------------------






















@subscription_required
@login_required(login_url='loginuser')
def history(request, animal_id):
    # Récupérer l'animal de l'utilisateur actuel
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Récupérer les paramètres de santé et autres données liées à l'animal
    animal_health_parameter_vaccination = health_parameter_vaccination.objects.filter(gip=animal)
    animal_health_parameter_vetexam = health_parameter_vetexam.objects.filter(gip=animal)
    animal_nutrition_and_feeding = nutrition_and_feeding.objects.filter(gip=animal)

    # Récupérer les objets optionnels pour l'animal
    animal_disposal_culling = disposal_culling.objects.filter(gip=animal).first()
    # animal_economics = economics.objects.filter(gip=animal).first()
    animal_death = death.objects.filter(gip=animal).first()

    # Récupérer les informations spécifiques selon le sexe de l'animal
    if animal.gender == 'Male':
        animal_efficiency_parameter = efficiency_parameter_male.objects.filter(gip=animal).first()
        animal_qualification_boar = qualification_boar.objects.filter(gip=animal).first()
        animal_service_record = service_record_male.objects.filter(gip=animal)
        context = {
            'tablename': 'History Sheet',
            'death': animal_death,
            'gen': animal,
            'vaccinations': animal_health_parameter_vaccination,
            'vetexams': animal_health_parameter_vetexam,
            'disposal': animal_disposal_culling,
            'nutritions': animal_nutrition_and_feeding,
            # 'economic': animal_economics,
            'efficiency': animal_efficiency_parameter,
            'qualification': animal_qualification_boar,
            'services': animal_service_record
        }
        return render(request, "data/historydatamale.html", context)

    elif animal.gender == 'Female':
        animal_efficiency_parameter = efficiency_parameter_female.objects.filter(gip=animal).first()
        animal_service_record_female = service_record_female.objects.filter(gip=animal)

        born_sum = sum(i.born_total for i in animal_service_record_female)
        weaned_sum = sum(i.total_weaned for i in animal_service_record_female)
        total_born_weight = sum(i.litter_weight_birth for i in animal_service_record_female)
        total_weaned_weight = sum(i.weaning_weight for i in animal_service_record_female)

        preweaning_mortality = (born_sum - weaned_sum) * 100.0 / born_sum if born_sum else 0

        context = {
            'tablename': 'History Sheet',
            'death': animal_death,
            'animal_id': animal,
            'gen': animal,
            'vaccinations': animal_health_parameter_vaccination,
            'vetexams': animal_health_parameter_vetexam,
            'disposal': animal_disposal_culling,
            'nutritions': animal_nutrition_and_feeding,
            # 'economic': animal_economics,
            'services': animal_service_record_female,
            'efficiency': animal_efficiency_parameter,
            'born_sum': born_sum,
            'weaned_sum': weaned_sum,
            'total_born_weight': total_born_weight,
            'total_weaned_weight': total_weaned_weight,
            'preweaning_mortality': preweaning_mortality,
        }
        return render(request, "data/historydatafemale.html", context)

@subscription_required
@login_required(login_url='loginuser')
def allpigs(request):
    # Tri des animaux par ordre alphabétique en fonction du champ 'name'
    animals = general_identification_and_parentage.objects.filter(user=request.user).order_by('animal_id')

    context = {
        'animals': animals,
        'tablename': 'Tous les animaux de la Ferme',
    }
    return render(request, "data/allpigs.html", context)



import plotly.express as px
import plotly.io as pio
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import general_identification_and_parentage
from .forms import datetodate
import plotly.express as px
import plotly.io as pio
import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import general_identification_and_parentage
from .forms import datetodate


@subscription_required
@login_required(login_url='loginuser')
def pigletborn(request):
    graph_json = None
    if request.method == 'POST':
        form = datetodate(request.POST)
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']

            # Filtrer les données en fonction des dates et de l'utilisateur
            allborn = general_identification_and_parentage.objects.filter(
                dob__range=(fromdate, todate),
                user=request.user
            )

            # Compter le nombre total de porcelets nés
            totalcount = allborn.count()
            malecount = allborn.filter(gender='Male').count()
            femalecount = allborn.filter(gender='Female').count()

            # Convertir les données en DataFrame Pandas
            df = pd.DataFrame.from_records(allborn.values('dob', 'gender'))
            df['dob'] = pd.to_datetime(df['dob'])  # Convertir en format datetime

            # Compter le nombre de naissances par jour
            birth_count = df.groupby('dob').size().reset_index(name='Nombre de porcelets')

            # Créer un graphique interactif avec Plotly
            fig = px.line(
                birth_count, 
                x='dob', 
                y='Nombre de porcelets', 
                color_discrete_sequence=['green', 'red'],
                title="Nombre de porcelets nés par jour",
                labels={'dob': 'Date', 'Nombre de porcelets': 'Nombre de porcelets nés'},
                # markers=True,

            )

            # Ajouter un histogramme pour la répartition des genres
            fig2 = px.bar(
                x=['Mâles', 'Femelles'], 
                y=[malecount, femalecount], 
                title="Répartition des porcelets nés par genre",
                labels={'x': 'Genre', 'y': 'Nombre'},
                color=['Mâles', 'Femelles'], 
                color_discrete_sequence=['green', 'red']
            )

            # Convertir les graphiques en HTML
            graph_json = pio.to_html(fig, full_html=False)
            graph_json2 = pio.to_html(fig2, full_html=False)

            context = {
                'tablename': 'Nombre de porcelets nés',
                'malecount': malecount,
                'femalecount': femalecount,
                'totalcount': totalcount,
                'form': form,
                'graph_json': graph_json,  # Courbe des naissances
                'graph_json2': graph_json2  # Histogramme des genres
            }
            return render(request, "data/pigletborn.html", context)

    else:
        form = datetodate()

    return render(request, "data/pigletborn.html", {'form': form, 'graph_json': graph_json})



@subscription_required
@login_required(login_url='loginuser')
def pigletweaned(request):
    graph_json = None
    if request.method == 'POST':
        form = datetodate(request.POST)
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']

            # Filtrer par utilisateur connecté et date de sevrage
            allweanedmale = efficiency_parameter_male.objects.filter(
                dow__range=(fromdate, todate),
                user=request.user  # Filtrage par utilisateur
            )
            allweanedfemale = efficiency_parameter_female.objects.filter(
                dow__range=(fromdate, todate),
                user=request.user  # Filtrage par utilisateur
            )

            totalcount = allweanedmale.count() + allweanedfemale.count()
            malecount = allweanedmale.count()
            femalecount = allweanedfemale.count()

            # maleweight = sum(pig.weaning_weight for pig in allweanedmale)
            # femaleweight = sum(pig.weaning_weight for pig in allweanedfemale)
            df = pd.DataFrame.from_records(allweanedmale.values('dow'))
            df2 = pd.DataFrame.from_records(allweanedfemale.values('dow'))
            df['dow'] = pd.to_datetime(df['dow'])  # Convertir en format datetime
            df2['dow'] = pd.to_datetime(df['dow'])  # Convertir en format datetime
            weaned_count = df.groupby('dow').size().reset_index(name='Nombre de porcelets')
            weaned_count2 = df2.groupby('dow').size().reset_index(name='Nombre de porcelets')
            
                        # Ajouter une colonne 'Genre' pour différencier les groupes
            weaned_count['Genre'] = 'Mâles'
            weaned_count2['Genre'] = 'Femelles'

            # Fusionner les deux DataFrames
            df_final = pd.concat([weaned_count, weaned_count2])

            # Créer le graphique avec une ligne pour chaque genre
            fig = px.line(
                df_final, 
                x='dow', 
                y='Nombre de porcelets', 
                color='Genre',  # Séparer les données par couleur
                color_discrete_sequence=['green', 'red'],
                title="Nombre de porcelets sevrés par jour",
                labels={'dow': 'Date', 'Nombre de porcelets': 'Nombre de porcelets sevrés'},
                # markers=True
            )
        


            fig2 = px.bar(
                x=['Mâles', 'Femelles'], 
                y=[malecount, femalecount], 
                title="Répartition des porcelets nés par genre",
                labels={'x': 'Genre', 'y': 'Nombre'},
                color=['Mâles', 'Femelles'], 
                color_discrete_sequence=['green', 'red']
            )

            graph_json = pio.to_html(fig, full_html=False)
            graph_json2 = pio.to_html(fig2, full_html=False)

            context = {
                'tablename': 'Porcelets sevrés',
                'malecount': malecount,
                'femalecount': femalecount,
                'totalcount': totalcount,
                # 'maleweight': maleweight,
                # 'femaleweight': femaleweight,
                'form': form,
                'graph_json': graph_json,
                'graph_json2': graph_json2,
                
            }
            return render(request, "data/pigletweaned.html", context)

    # Formulaire vide au chargement initial
    form = datetodate()
    context = {
        'tablename': 'Porcelets sevrés',
        'malecount': 'aucune entrée',
        'femalecount': 'aucune entrée',
        'totalcount': 'aucune entrée',
        'maleweight': 'aucune entrée',
        'femaleweight': 'aucune entrée',
        'form': form
    }
    return render(request, "data/pigletweaned.html", context)



@subscription_required
@login_required(login_url='loginuser')
def pigmortality(request):
    graph_json = None
    if request.method == 'POST':
        form = datetodate(request.POST)
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']

            # Filtrer par utilisateur connecté et date de décès
            alldead = death.objects.filter(
                date_death__range=(fromdate, todate),
                user=request.user
            )

            preweaning = 0
            postweaning = 0

            for pig in alldead:
                try:
                    if pig.gip.gender == 'Male':
                        obj, created = efficiency_parameter_male.objects.get_or_create(gip=pig.gip)
                    else:
                        obj, created = efficiency_parameter_female.objects.get_or_create(gip=pig.gip)

                    if obj.dow is None:
                        preweaning += 1
                    else:
                        postweaning += 1
                except efficiency_parameter_male.DoesNotExist:
                    continue
                except efficiency_parameter_female.DoesNotExist:
                    continue

            # Vérifie que `alldead` contient bien des données
            if alldead.exists():
                df = pd.DataFrame.from_records(alldead.values('date_death'))
                df['date_death'] = pd.to_datetime(df['date_death'])

                # Comptage des décès par jour
                death_count = df.groupby('date_death').size().reset_index(name='Nombre de décès')

                # Création du graphique interactif
                fig = px.line(
                    death_count, 
                    x='date_death', 
                    y='Nombre de décès', 
                    title="Nombre de décès de porcelets par jour",
                    labels={'date_death': 'Date', 'Nombre de décès': 'Nombre de décès'},
                    # markers=True,
                    color_discrete_sequence=['red'],
                )

                graph_json = pio.to_html(fig, full_html=False)
            else:
                graph_json = None

            context = {
                'tablename': 'Pig Mortality',
                'form': form,
                'postweaning': postweaning,
                'preweaning': preweaning,
                'graph_json': graph_json,
            }
            return render(request, "data/pigmortality.html", context)

    # Formulaire vide au chargement initial
    form = datetodate()
    context = {
        'tablename': 'Pig Mortality',
        'form': form,
        'postweaning': None,
        'preweaning': None,
    }
    return render(request, "data/pigmortality.html", context)


@subscription_required
@login_required(login_url='loginuser')
def revenue_received(request):
    graph_json = None
    graph_json2 = None
    if request.method == 'POST':
        form = datetodate(request.POST)
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']

            # Filtrer les ventes par utilisateur et par date
            revenues = disposal_culling.objects.filter(
                sale_date__range=(fromdate, todate),
                user=request.user
            )

            # Calcul du total des revenus
            total = revenues.aggregate(Sum('revenue'))['revenue__sum'] or 0

            # Convertir les données en DataFrame Pandas
            df = pd.DataFrame.from_records(revenues.values('sale_date'))
            df['sale_date'] = pd.to_datetime(df['sale_date'])

            # Graphique 1 : Nombre de ventes par jour
            sales_count = df.groupby('sale_date').size().reset_index(name='Nombre de ventes')
            fig = px.line(
                sales_count,
                x='sale_date',
                y='Nombre de ventes',
                color_discrete_sequence=['green'],
                title="Nombre de ventes par jour",
                labels={'sale_date': 'Date', 'Nombre de ventes': 'Nombre de ventes'},
                # markers=True,
            )
            graph_json = pio.to_html(fig, full_html=False)

            # Graphique 2 : Montant total des ventes par jour
            df2 = pd.DataFrame.from_records(revenues.values('sale_date', 'revenue'))
            df2['sale_date'] = pd.to_datetime(df2['sale_date'])
            revenue_sum = df2.groupby('sale_date')['revenue'].sum().reset_index()
            fig2 = px.line(
                revenue_sum,
                x='sale_date',
                y='revenue',
                color_discrete_sequence=['blue'],
                title="Revenus générés par jour",
                labels={'sale_date': 'Date', 'revenue': 'Revenu total (€)'},
                # markers=True,
            )
            graph_json2 = pio.to_html(fig2, full_html=False)

            context = {
                'tablename': 'Revenus générés',
                'form': form,
                'total': total,
                'graph_json': graph_json,  # Nombre de ventes
                'graph_json2': graph_json2,  # Montant des ventes
            }
            return render(request, "data/revenuereceived.html", context)

    # Formulaire vide au chargement initial
    form = datetodate()
    context = {
        'tablename': 'Revenus générés',
        'form': form,
        'total': None,
        'graph_json': None,
        'graph_json2': None,
    }
    return render(request, "data/revenuereceived.html", context)


@subscription_required
@login_required(login_url='loginuser')
def selectpigs(request):
    if request.method == 'POST':
        form = selectpigsform(request.POST)
        if form.is_valid():
            n = form.cleaned_data['task']
            num = form.cleaned_data['amount']
            male = []
            female = []

            # Filtrage par utilisateur connecté
            if n == '1':
                animals = general_identification_and_parentage.objects.filter(
                    colitter_size_of_birth__lt=num,
                    user=request.user  # Ajout du filtre utilisateur
                )
            elif n == '2':
                animals = general_identification_and_parentage.objects.filter(
                    colitter_size_of_birth__gt=num,
                    user=request.user
                )
            elif n == '3':
                maleanimals = efficiency_parameter_male.objects.filter(
                    litter_size_weaning__gte=num,
                    user=request.user
                )
                femaleanimals = efficiency_parameter_female.objects.filter(
                    litter_size_weaning__gte=num,
                    user=request.user
                )
            elif n == '4':
                maleanimals = efficiency_parameter_male.objects.filter(
                    litter_size_weaning__exact=num,
                    user=request.user
                )
                femaleanimals = efficiency_parameter_female.objects.filter(
                    litter_size_weaning__exact=num,
                    user=request.user
                )

            
            # Traitement des résultats
            if n in ['1', '2']:
                male = [i.animal_id for i in animals if i.gender == 'Male']
                female = [i.animal_id for i in animals if i.gender != 'Male']
            else:
                male = [i.gip for i in maleanimals]
                female = [i.gip for i in femaleanimals]

            context = {
                'form': form,
                'male': male,
                'female': female,
                'malelen': len(male),
                'femalelen': len(female),
                'tablename': 'Select Pigs'
            }

            return render(request, "data/selectpigs.html", context)

    form = selectpigsform()
    return render(request, "data/selectpigs.html", {'form': form, 'tablename': 'Select Pigs'})




@subscription_required
@login_required(login_url='loginuser')
def disease(request):
    # Filtrer les décès en fonction de l'utilisateur connecté
    alldeath = death.objects.filter(user=request.user)

    diseaseDict = {}
    for i in alldeath:
        cause = i.cause_death
        diseaseDict[cause] = diseaseDict.get(cause, 0) + 1  # Utilisation de .get() pour simplifier

    context = {
        'tablename': 'Disease List',
        'diseases': diseaseDict
    }
    return render(request, "data/disease.html", context)


def account(request):

    subscription, created = Subscription.objects.get_or_create(user=request.user)     # Vérifie si le code est toujours valide et l'affiche

    """ Permet à l'utilisateur de saisir un code fourni par l'admin """

    if request.method == "POST":
        code = request.POST.get("code")

        try:
            subscription = Subscription.objects.get(code=code)
            if subscription.expires_at > now():  # Vérifie que le code n'a pas expiré
                request.user.subscription.code = code
                request.user.subscription.expires_at = subscription.expires_at
                request.user.subscription.save()
                messages.success(request, "Abonnement activé avec succès !")
                return redirect('account')
            else:
                messages.error(request, "Ce code a expiré.")
        except Subscription.DoesNotExist:
            messages.error(request, "Code invalide.")
    
    # return render(request, 'enter_subscription_code.html')


    return render(request, 'account/account.html', {'subscription': subscription})

def help(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupération des données
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            number = form.cleaned_data['number']
            message = form.cleaned_data['message']

            # Enregistrement en base de données
            Contact.objects.create(
                name=name,
                email=email,
                number=number,
                message=message
            )

            # Envoi de l'email
            send_mail(
                subject=f"Nouveau message de {name}",
                message=f"De : {name}\nNuméro : {number}\n Email: ({email}\n message venant du formulaire de la page de help\n\n Source: site web bangpig.com\nMessage: ({message})",
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )


            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('help')  # Redirection pour éviter les resoumissions
    else:
        form = ContactForm()

    return render(request, 'others/help.html', {'form': form})

    # return render(request, 'others/help.html')







def searchdelete(request):
    query = None
    results = []
    search_form = SearchPig()

    if 'query' in request.GET:
        search_form = SearchPig(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            vector_search = SearchVector('animal_id', weight='A')
            query_search = SearchQuery(query)
            # results = Post.published_posts.annotate(
            #     search=vector_search, rank=SearchRank(vector_search,query_search)
            # ).filter(rank__gte=0.3).order_by('rank')
            # results = Post.published_posts.annotate(
            #                                         similarity=TrigramSimilarity("title", query),
            #                                         ).filter(similarity__gt=0.1).order_by("-similarity")
            results = general_identification_and_parentage.objects.filter(animal_id=query)
            

    return render(request, 'others/searchdelete.html', {
        'search_form': search_form,
        'query': query,
        'results': results,
    })



def searchupdate(request):
    query = None
    results = []
    search_form = SearchPig()

    if 'query' in request.GET:
        search_form = SearchPig(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            vector_search = SearchVector('animal_id', weight='A')
            query_search = SearchQuery(query)
            # results = Post.published_posts.annotate(
            #     search=vector_search, rank=SearchRank(vector_search,query_search)
            # ).filter(rank__gte=0.3).order_by('rank')
            # results = Post.published_posts.annotate(
            #                                         similarity=TrigramSimilarity("title", query),
            #                                         ).filter(similarity__gt=0.1).order_by("-similarity")
            results = general_identification_and_parentage.objects.filter(animal_id=query)
            

    return render(request, 'others/searchupdate.html', {
        'search_form': search_form,
        'query': query,
        'results': results,
    })

def home(request):
    return render(request, 'home.html')


def documentation(request):
    return render(request, 'others/documentation.html')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscription

@login_required
def generate_subscription_code(request):
    """ Permet à l'admin de générer un code pour un utilisateur """
    # if not request.user.is_staff:  # Seuls les admins peuvent générer des codes
    #     messages.error(request, "Vous n'avez pas l'autorisation de générer un code.")
    #     return redirect('account')

    subscription, created = Subscription.objects.get_or_create(user=request.user)
    subscription.generate_new_code()  # Génère un code mais ne l'active pas
    messages.success(request, "Code généré ! Un admin doit maintenant l'activer.")
    
    return redirect('account')  # Redirige vers la page de l'utilisateur


@login_required
def subscription_status(request):
    """ Vérifie si le code est toujours valide et l'affiche """
    subscription, created = Subscription.objects.get_or_create(user=request.user)
    # return render(request, 'subscription_status.html', {'subscription': subscription})

    return render(request, 'account/account.html', {'subscription': subscription})


from django.contrib import messages
@login_required
def enter_subscription_code(request):
    """ Permet à l'utilisateur de saisir un code fourni par l'admin """
    if request.method == "POST":
        code = request.POST.get("code")
        try:
            subscription = Subscription.objects.get(code=code)
            if subscription.is_valid():  # Vérifie que le code est activé et valide
                request.user.subscription.code = code
                request.user.subscription.expires_at = subscription.expires_at
                request.user.subscription.save()
                messages.success(request, "Abonnement activé avec succès !")
                return redirect('account')
            elif not subscription.is_active:
                messages.error(request, "Ce code n'a pas encore été activé.")
            else:
                messages.error(request, "Ce code a expiré.")
        except Subscription.DoesNotExist:
            messages.error(request, "Code invalide.")

    return render(request, 'account/account.html')


