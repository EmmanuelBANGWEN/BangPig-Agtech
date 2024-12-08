from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.

# for login
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
    return render(request, "login.html", context)

def logoutuser(request):
    logout(request)  # Déconnexion de l'utilisateur
    return redirect('loginuser')  # Redirection vers la page de connexion

def registeruser(request):
    if request.user.is_authenticated:
       return redirect('index')  # Redirection si l'utilisateur est déjà connecté
    form = CreateUserForm()  # Création d'un formulaire d'inscription
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # Récupération des données soumises
        if form.is_valid():
            form.save()  # Enregistrement du nouvel utilisateur
            return redirect('loginuser')  # Redirection vers la page de connexion
    context = {'form': form, 'tablename': 'Register'}
    return render(request, "register.html", context)

#--------------------------------------------------------------------------------------------------------------------------------------














#---------------------------------------------------------------------------------------------------------------------------------------

def dataentry(request):  #entrer les donnees
    return render(request, "dataentry.html", context={'tablename':'Que Voulez-Vous faire ?'})

def report(request):  
    return render(request, "report.html", context={'tablename':'Mes Enregistrements'})
#-------------------------------------------------------------------------------------------------------------------------------------------














@login_required(login_url='loginuser')
def delete(request, animal_id):                  #permet de supprimer un enregistrement d'animal. L'animal est récupéré grâce à son animal_id et supprimé.
    animal=get_object_or_404(general_identification_and_parentage, animal_id=animal_id)
    animal.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='loginuser')
def deletepigs(request):              #Affiche une page où les animaux dun user sont listés et permettent de choisir ceux à supprimer.
    animals=general_identification_and_parentage.objects.filter(user=request.user)
    context={
        'animals':animals,
        'tablename':'Supprimer Un Porc',
    }
    return render(request, "deletepigs.html", context)


@login_required(login_url='loginuser')
def delete_service(request, animal_id, pk):     #Supprime un service en fonction du genre de l'animal.
    if request.method=='POST':
        backbutton=request.POST.get('backbutton')
        animal=get_object_or_404(general_identification_and_parentage, animal_id=animal_id)
        if animal.gender=='Male':
            #service=get_object_or_404(service_record_male, gip=animal, pk=pk)
            service=service_record_male.objects.get(gip=animal, pk=pk) 
            
            service.delete()
            return redirect(backbutton)
        else:
            service=get_object_or_404(service_record_female, gip=animal, pk=pk)
            service.delete()
            return redirect(request.build_absolute_uri())

@login_required(login_url='loginuser')
def delete_vaccination(request, animal_id, pk):
    if request.method=='POST':
        backbutton=request.POST.get('backbutton')
        animal=get_object_or_404(general_identification_and_parentage, animal_id=animal_id)
        vacc=health_parameter_vaccination.objects.get(gip=animal, pk=pk) 
        vacc.delete()   # Suppression de la vaccination
        return redirect(backbutton)

@login_required(login_url='loginuser')
def delete_vetexam(request, animal_id, pk):
    if request.method=='POST':
        backbutton=request.POST.get('backbutton')
        animal=get_object_or_404(general_identification_and_parentage, animal_id=animal_id)
        vet=health_parameter_vetexam.objects.get(gip=animal, pk=pk) 
        vet.delete()  # Suppression de l'examen vétérinaire
        return redirect(backbutton)

@login_required(login_url='loginuser')
def delete_nutrition(request, animal_id, pk):
    if request.method=='POST':
        backbutton=request.POST.get('backbutton')
        animal=get_object_or_404(general_identification_and_parentage, animal_id=animal_id)
        nutrition=nutrition_and_feeding.objects.get(gip=animal, pk=pk) 
        nutrition.delete()  # Suppression de l'enregistrement nutritionnel
        return redirect(backbutton)


#Ces fonctions permettent de supprimer des enregistrements spécifiques associés à un animal en utilisant leurs identifiants.









































#-----------------------------------------------------------------------------------------------------------------------------------------------
@login_required(login_url='loginuser')
def dbsuccess(request):    #dbsuccess : Renvoie un template dbsuccess.html avec un contexte indiquant que l'opération a été un succès.
    return render(request, "dbsuccess.html", context={'tablename':'Success'})

@login_required(login_url='loginuser')
def index(request):
    # Total des animaux enregistrés
    total_animals = general_identification_and_parentage.objects.count()
    
    # Nombre de femelles
    total_females = general_identification_and_parentage.objects.filter(gender='Female').count()
    
    # Nombre de mâles
    total_males = general_identification_and_parentage.objects.filter(gender='Male').count()
    
    # Nombre de porcelets (hypothèse : âge < 6 mois)
    from datetime import date, timedelta
    six_months_ago = date.today() - timedelta(days=6*30)
    total_piglets = general_identification_and_parentage.objects.filter(dob__gte=six_months_ago).count()
    
    context = {
        'total_animals': total_animals,
        'total_females': total_females,
        'total_males': total_males,
        'total_piglets': total_piglets,
    }
    return render(request, "index.html", context)










@login_required(login_url='loginuser')
def create_general(request):
    form=general_form()  # Création d'un formulaire vierge pour la création d'un animal
    if request.method=='POST':
        form=general_form(request.POST)  #  Remplissage du formulaire avec les données envoyées
        if form.is_valid():
            animal_id=str(form.cleaned_data['animal_id'])
            # Vérifie si l'animal existe déjà
            if general_identification_and_parentage.objects.filter(animal_id=animal_id).exists()==False:
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



@login_required(login_url='loginuser')
def create_efficiency(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    gender=animal.gender  # Récupération du genre de l'animal
    if gender=='Male':
        form=efficiency_form_male(initial={'gip':animal}) # Formulaire spécifique pour un mâle
        if request.method=='POST':    
            form=efficiency_form_male(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                agevar=instance.dow-instance.gip.dob  # Calcul de l'âge au sevrage
                instance.weaning_age=agevar.days
                obj = form.save(commit=False)
                obj.user = request.user  # Associer l'utilisateur connecté
                obj.save()
                return redirect('create_qualification',animal_id=animal_id)
                
        context={
            'form':form,
            'tablename':'Paramètre Efficacité'
        }

        return render(request,"create/create_efficiency_male.html",context)
    elif gender=='Female':
        form=efficiency_form_female(initial={'gip':animal})
        if request.method=='POST':    
            form=efficiency_form_female(request.POST)  # Formulaire spécifique pour une femelle
            if form.is_valid():
                instance=form.save(commit=False)
                agevar=instance.dow-instance.gip.dob  # Calcul de l'âge au sevrage
                instance.weaning_age=agevar.days
                form.save()
                return redirect('create_qualification',animal_id=animal_id)
        context={
            'form':form,
            'tablename':'Paramètre Efficacité'
        }

        return render(request,"create/create_efficiency_female.html",context)

# Enregistre les paramètres d'efficacité pour un animal, en fonction de son genre (mâle ou femelle).
# Le calcul de weaning_age se base sur la différence entre la date du sevrage (dow) et la date de naissance (dob).




@login_required(login_url='loginuser')
def create_qualification(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    gender=animal.gender
    if gender=='Female':
        return redirect('create_service',animal_id=animal_id) # Redirection si l'animal est une femelle
    
    form=qualification_form(initial={'gip':animal})
    if request.method=='POST':    
        form=qualification_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('create_service',animal_id=animal_id)
    context={
        'form':form,
        'tablename': 'Qualification As Breeding Boar'
    }

    return render(request,"create/create_qualification.html",context)

# Gère la création des qualifications pour les mâles. Les femelles passent directement à la création des services.



@login_required(login_url='loginuser')
def create_service(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    gender=animal.gender
    if gender=='Male':
        services=service_record_male.objects.filter(gip=animal)
        form=service_form_male(initial={'gip':animal})
        if request.method=='POST':    
            form=service_form_male(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                born_total=instance.born_female+instance.born_male
                weaned_total=instance.weaned_female+instance.weaned_male
                instance.total_weaned=weaned_total
                instance.born_total=born_total
                obj = form.save(commit=False)
                obj.user = request.user  # Associer l'utilisateur connecté
                obj.save()
                return redirect('create_service',animal_id=animal_id)
        context={
            'form':form,
            'services':services,
            'gip':animal_id,
            'tablename': 'Enregistrement des Services et Caractères des Portées',
            'backbut':request.build_absolute_uri(),
        }

        return render(request,"service_male.html",context)
    elif gender=='Female':
        services=service_record_female.objects.filter(gip=animal)
        form=service_form_female(initial={'gip':animal})
        if request.method=='POST':    
            form=service_form_female(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                born_total=instance.born_female+instance.born_male
                weaned_total=instance.weaned_female+instance.weaned_male
                instance.total_weaned=weaned_total
                instance.born_total=born_total
                obj = form.save(commit=False)
                obj.user = request.user  # Associer l'utilisateur connecté
                obj.save()
                return redirect('create_service',animal_id=animal_id)
        context={
            'form':form,
            'services':services,
            'gip':animal_id,
            'tablename': 'Enregistrement des Services et Caractères des Portées',
            'backbut':request.build_absolute_uri(),
        }
        return render(request,"service_female.html",context)

# Enregistre les services (données de reproduction) pour un animal. Le formulaire et le template changent selon le genre de l'animal.
# Calcule les totaux des petits nés et sevrés.




@login_required(login_url='loginuser')
def vaccination(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id, user=request.user)
    vaccinations=health_parameter_vaccination.objects.filter(gip=animal)
    form=vaccination_form(initial={'gip':animal})
    if request.method=='POST':    
        form = vaccination_form(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('vaccination',animal_id=animal_id)
    context={
        'form':form,
        'vaccinations':vaccinations,
        'gip':animal_id,
        'backbut':request.build_absolute_uri(),
        'tablename':'Vaccinations'
    }

    return render(request,"vaccinationtemplate.html",context)

@login_required(login_url='loginuser')
def vetexam(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id, user=request.user )
    vet_exams=health_parameter_vetexam.objects.filter(gip=animal)
    form=vetexam_form(initial={'gip':animal})
    if request.method=='POST':    
        form=vetexam_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('vetexam',animal_id=animal_id)
    context={
        'form':form,
        'vet_exams':vet_exams,
        'gip':animal_id,
        'backbut':request.build_absolute_uri(),
        'tablename':'Veterinary Exam'
    }

    return render(request,"vetexamtemplate.html",context)



@login_required(login_url='loginuser')
def create_nutrition(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id, user=request.user )
    nutritions=nutrition_and_feeding.objects.filter(gip=animal)
    form=nutrition_form(initial={'gip':animal})
    if request.method=='POST':
          
        form=nutrition_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            
            return redirect('create_nutrition',animal_id=animal_id)
    context={
        'tablename':'Nutrition',
        'form':form,
        'nutritions': nutritions,
        'backbut':request.build_absolute_uri(),
        'gip':animal_id
    }

    return render(request,"nutrition_template.html",context)

# Les fonctions suivantes (vaccination, vetexam, create_nutrition) suivent le même schéma :

# Elles récupèrent les données liées à un animal donné (par son animal_id).
# Elles affichent un formulaire spécifique pour enregistrer de nouvelles données ou consulter les anciennes.
# Après enregistrement, elles redirigent vers la même page pour afficher la liste mise à jour.


@login_required(login_url='loginuser')
def deathview(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    form=death_form(initial={'gip':animal})
    if request.method=='POST':    
        form=death_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('create_nutrition',animal_id=animal_id)
    context={
        'tablename':'Information About Death Of Pig',
        'form':form,
    }

    return render(request,"create/create_death.html",context)


@login_required(login_url='loginuser')
def create_disposal(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    form=disposal_form(initial={'gip':animal})
    if request.method=='POST':    
        form=disposal_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            print("I was here")
            return redirect('create_economics', animal_id=animal_id)
    context={
        'form':form,
        'tablename':'Disposal And Culling'
    }

    return render(request,"create/create_disposal.html",context)





@login_required(login_url='loginuser')
def create_economics(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    form=economics_form(initial={'gip':animal})
    if request.method=='POST':
        form=economics_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('dbsuccess')
    context={
        'form':form,
        'tablename':'Economics'
    }

    return render(request,"create/create_economics.html",context)









#-----------------------------------------------------------------------------------------------------------------------------------





@login_required(login_url='loginuser')
def successupdate(request):
    return render(request,"successupdate.html", context={'tablename':'Update Successful'})



@login_required(login_url='loginuser')
def update(request):
    animal_id = request.POST.get('animal_id')
    if animal_id and general_identification_and_parentage.objects.filter(animal_id=animal_id).exists():
        animal = general_identification_and_parentage.objects.get(animal_id=animal_id)
        context = {
            'tablename': 'Mise à Jour des Enregistrements',
            'animal_id': animal_id,
            'gender': animal.gender
        }
        if animal.gender == 'Female':
            return render(request, "updatefemale.html", context)
        elif animal.gender == 'Male':
            return render(request, "updatemale.html", context)
    else:
        messages.error(request, 'The animal does not exist')
        return redirect('dataentry')



@login_required(login_url='loginuser')
def update_general(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    form=general_update_form(instance=animal)
    if request.method=='POST':
        form=general_update_form(request.POST, instance=animal)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('successupdate')
    context={
        'form':form,
        'tablename': 'Identification Générale et Parenté'
    }

    return render(request,"generalupdate.html",context)



@login_required(login_url='loginuser')
def update_disposal(request, animal_id):
    try:
        obj = general_identification_and_parentage.objects.get(animal_id=animal_id)
        disposal_instance, created = disposal_culling.objects.get_or_create(gip=obj)
    except general_identification_and_parentage.DoesNotExist:
        return HttpResponse("Animal not found", status=404)

    form = disposal_update_form(instance=disposal_instance)
    if request.method == 'POST':
        form = disposal_update_form(request.POST, instance=disposal_instance)
        if form.is_valid():
            disposal_instance = form.save(commit=False)
            disposal_instance.user = request.user  # Assigne l'utilisateur connecté
            disposal_instance.save()
            return redirect('successupdate')
        else:
            print("Form Errors:", form.errors)  # Debugging

    context = {
        'form': form,
        'tablename': 'Disposal',
    }
    return render(request, "updatedisposal.html", context)


@login_required(login_url='loginuser')
def update_nutrition(request, animal_id):
    animal = general_identification_and_parentage.objects.get(animal_id=animal_id, user=request.user)
    nutritions = nutrition_and_feeding.objects.filter(gip=animal)
    
    form = nutrition_update_form(initial={'gip': animal}, user=request.user, specific_animal=animal)
    
    if request.method == 'POST':
        form = nutrition_update_form(request.POST, user=request.user, specific_animal=animal)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('update_nutrition', animal_id=animal_id)
    
    context = {
        'tablename': 'Update Nutrition',
        'form': form,
        'nutritions': nutritions,
        'backbut': request.build_absolute_uri(),
        'gip': animal_id
    }
    return render(request, "nutrition_update_template.html", context)



@login_required(login_url='loginuser')
def update_economics(request, animal_id):
    try:
        obj = general_identification_and_parentage.objects.get(animal_id=animal_id)
        economics_instance, created = economics.objects.get_or_create(gip=obj)
        
    except general_identification_and_parentage.DoesNotExist:
        return HttpResponse("Animal not found", status=404)

    form = economics_update_form(instance=economics_instance)
    if request.method == 'POST':
        form = economics_update_form(request.POST, instance=economics_instance)
        if form.is_valid():
            economics_instance = form.save(commit=False)
            economics_instance.user = request.user  # Assigne l'utilisateur connecté
            economics_instance.save()
            return redirect('successupdate')
        else:
            print("Form Errors:", form.errors)  # Debugging

    context = {
        'form': form,
        'tablename': 'Economics',
    }
    return render(request, "updateeconomics.html", context)


@login_required(login_url='loginuser')
def update_efficiency(request,animal_id):
    obj=general_identification_and_parentage.objects.get(animal_id=animal_id)
    gender=obj.gender
    if gender=='Male':
        animal, create=efficiency_parameter_male.objects.get_or_create(gip=obj)
        form=efficiency_update_form_male(instance=animal)
        if request.method=='POST':
            form=efficiency_update_form_male(request.POST, instance=animal)
            if form.is_valid():
                instance=form.save(commit=False)
                agevar=instance.dow-instance.gip.dob
                instance.weaning_age=agevar.days
                form.save()
                return redirect('successupdate')
        context={
            'form':form,
            'tablename': 'Paramètre Efficacité'
        }


        return render(request,"create/create_efficiency_male.html",context)
    elif gender=='Female':
        animal, create=efficiency_parameter_female.objects.get_or_create(gip=obj)
        form=efficiency_update_form_female(instance=animal)
        if request.method=='POST':
            form=efficiency_update_form_female(request.POST, instance=animal)
            if form.is_valid():
                instance=form.save(commit=False)
                agevar=instance.dow-instance.gip.dob
                instance.weaning_age=agevar.days
                form.save()
                return redirect('successupdate')
        context={
            'form':form,
            'tablename': 'Paramètre Efficacité'
        }

        return render(request,"create/create_efficiency_female.html",context)

@login_required(login_url='loginuser')
def update_qualification(request, animal_id):
    obj=general_identification_and_parentage.objects.get(animal_id=animal_id)
    animal, create=qualification_boar.objects.get_or_create(gip=obj)
    form=qualification_update_form(instance=animal)
    if request.method=='POST':
        form=qualification_update_form(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('successupdate')
    context={
        'form':form,
        'tablename': 'Qualification As A Breeding Boar'
    }

    return render(request,"create/create_qualification.html",context)




@login_required(login_url='loginuser')
def update_death(request, animal_id):
    try:
        obj = general_identification_and_parentage.objects.get(animal_id=animal_id)
        death_instance, created = death.objects.get_or_create(gip=obj)
    except general_identification_and_parentage.DoesNotExist:
        return HttpResponse("Animal not found", status=404)

    form = death_update_form(instance=death_instance)
    if request.method == 'POST':
        form = death_update_form(request.POST, instance=death_instance)
        if form.is_valid():
            death_instance = form.save(commit=False)
            death_instance.user = request.user  # Assigne l'utilisateur connecté
            death_instance.save()
            return redirect('successupdate')
        else:
            print("Form Errors:", form.errors)  # Debugging

    context = {
        'form': form,
        'tablename': 'Death',
    }
    return render(request, "updatedisposal.html", context)


















@login_required(login_url='loginuser')
def update_service(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id)
    gender=animal.gender
    if gender=='Male':
        services=service_record_male.objects.filter(gip=animal)
        form=service_form_male(initial={'gip':animal})
        if request.method=='POST':    
            form=service_form_male(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                born_total=instance.born_female+instance.born_male
                weaned_total=instance.weaned_female+instance.weaned_male
                instance.total_weaned=weaned_total
                instance.born_total=born_total
                form.save()
                return redirect('update_service',animal_id=animal_id)
        context={
            'form':form,
            'services':services,
            'gip':animal_id,
            'backbut':request.build_absolute_uri(),
            'tablename': 'Enregistrement des Services et Caractères des Portées'
        }

        return render(request,"service_update_male.html",context)
    elif gender=='Female':
        services=service_record_female.objects.filter(gip=animal)
        form=service_form_female(initial={'gip':animal})
        if request.method=='POST':    
            form=service_form_female(request.POST)
            if form.is_valid():
                instance=form.save(commit=False)
                born_total=instance.born_female+instance.born_male
                weaned_total=instance.weaned_female+instance.weaned_male
                instance.total_weaned=weaned_total
                instance.born_total=born_total
                form.save()
                return redirect('update_service',animal_id=animal_id)
        context={
            'form':form,
            'services':services,
            'gip':animal_id,
            'backbut':request.build_absolute_uri(),
            'tablename': 'Enregistrement des Services et Caractères des Portées'
        }
        return render(request,"service_update_female.html",context)

@login_required(login_url='loginuser')
def update_vaccination(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id,  user=request.user)
    vaccinations=health_parameter_vaccination.objects.filter(gip=animal)
    form=vaccination_update_form(initial={'gip':animal}, user=request.user, specific_animal=animal)
    if request.method=='POST':    
        form=vaccination_update_form(request.POST, user=request.user, specific_animal=animal)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('update_vaccination',animal_id=animal_id)
    context={
        'form':form,
        'vaccinations':vaccinations,
        'gip':animal_id,
        'backbut':request.build_absolute_uri(),
        'tablename':'Vaccinations'
    }

    return render(request,"vaccination_update_template.html",context)

@login_required(login_url='loginuser')
def update_vetexam(request, animal_id):
    animal=general_identification_and_parentage.objects.get(animal_id=animal_id, user=request.user)
    vet_exams=health_parameter_vetexam.objects.filter(gip=animal)
    form=vetexam_update_form(initial={'gip':animal}, user=request.user, specific_animal=animal)
    if request.method=='POST':    
        form=vetexam_update_form(request.POST, user=request.user, specific_animal=animal)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Associer l'utilisateur connecté
            obj.save()
            return redirect('update_vetexam',animal_id=animal_id)
    context={
        'form':form,
        'vet_exams':vet_exams,
        'gip':animal_id,
        'backbut':request.build_absolute_uri(),
        'tablename':'Veterinary Exam'
    }

    return render(request,"vetexam_update_template.html",context)





# @login_required(login_url='loginuser')
# def update_service(request, animal_id):
#     obj=general_identification_and_parentage.objects.get(animal_id=animal_id)
#     gender=obj.gender
#     if gender=='Male':
#         animal=service_record_male.objects.get(gip=obj)
#         form=service_update_form_male(instance=animal)
#         if request.method=='POST':
#             form=service_update_form_male(request.POST, instance=animal)
#             if form.is_valid():
#                 form.save()
#                 return redirect('successupdate')
#         context={
#             'form':form,
#             'tablename': 'Enregistrement des Services et Caractères des Portées'
#         }

#         return render(request,"formtemplate.html",context)
#     elif gender=='Female':
#         animal=service_record_female.objects.get(gip=obj)
#         form=service_update_form_female(instance=animal)
#         if request.method=='POST':
#             form=service_update_form_female(request.POST, instance=animal)
#             if form.is_valid():
#                 form.save()
#                 return redirect('successupdate')
#         context={
#             'form':form,
#             'tablename': 'Enregistrement des Services et Caractères des Portées'
#         }

#-----------------------------------------------------------------------------------------------------------------------------






















@login_required(login_url='loginuser')
def history(request, animal_id):
    if general_identification_and_parentage.objects.filter(animal_id=animal_id).exists()==False:
        messages.error(request, 'The animal does not exist')
        return redirect(report)
    from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

    try:
        animal = general_identification_and_parentage.objects.get(animal_id=animal_id)
    except MultipleObjectsReturned:
        animal = general_identification_and_parentage.objects.filter(animal_id=animal_id).first()
    except ObjectDoesNotExist:
        animal = None  # Gérer le cas où aucun animal n'existe
    
    animal_gender=animal.gender
    animal_health_parameter_vaccination=health_parameter_vaccination.objects.filter(gip=animal)
    animal_health_parameter_vetexam=health_parameter_vetexam.objects.filter(gip=animal)
    if disposal_culling.objects.filter(gip=animal).exists():
        animal_disposal_culling=disposal_culling.objects.get(gip=animal)
    else:
        animal_disposal_culling=None
    animal_nutrition_and_feeding=nutrition_and_feeding.objects.filter(gip=animal)
    if economics.objects.filter(gip=animal).exists():
        animal_economics=economics.objects.get(gip=animal)
    else:
        animal_economics=None
    if death.objects.filter(gip=animal).exists():
        animal_death=death.objects.get(gip=animal)
    else:
        animal_death=None
    if animal_gender=='Male':
        if efficiency_parameter_male.objects.filter(gip=animal).exists():
            animal_efficiency_parameter_male=efficiency_parameter_male.objects.get(gip=animal)
        else:
            animal_efficiency_parameter_male=None
        if qualification_boar.objects.filter(gip=animal).exists():
            animal_qualification_boar=qualification_boar.objects.get(gip=animal)
        else:
            animal_qualification_boar=None
        animal_service_record_male=service_record_male.objects.filter(gip=animal)
        context={
        'tablename':'History Sheet',
        'death':animal_death,
        'gen': animal,
        'vaccinations':animal_health_parameter_vaccination,
        'vetexams':animal_health_parameter_vetexam,
        'disposal':animal_disposal_culling,
        'nutritions':animal_nutrition_and_feeding,
        'economic':animal_economics,
        'efficiency':animal_efficiency_parameter_male,
        'qualification': animal_qualification_boar,
        'services':animal_service_record_male
        }

        return render(request, "historydatamale.html", context)
    
    elif animal_gender=='Female':
        if efficiency_parameter_female.objects.filter(gip=animal).exists():
            animal_efficiency_parameter_female=efficiency_parameter_female.objects.get(gip=animal)
        else:
            animal_efficiency_parameter_female=None
        
        animal_service_record_female=service_record_female.objects.filter(gip=animal)
        
        born_sum = 0  #somme totale des animaux nés (mâles et femelles) pour toutes les portées de l'animal.
        weaned_sum = 0  # somme totale des animaux sevrés pour toutes les portées.
        total_born_weight = 0       #  poids total des portées à la naissance.
        total_weaned_weight = 0          #  poids total des portées au moment du sevrage.
        preweaning_mortality = 0        #  Pourcentage de mortalité pré-sevrage

        for i in animal_service_record_female:
            born_sum+=i.born_total
            weaned_sum+=i.total_weaned
            total_born_weight+=i.litter_weight_birth
            total_weaned_weight+=i.weaning_weight
            if born_sum != 0:
                preweaning_mortality = (born_sum - weaned_sum) * 100.0 / born_sum
            else:
                preweaning_mortality = 0 
        #animal_lifetime_litter_character=lifetime_litter_character.objects.get(gip=animal)
        context={
        'tablename':'History Sheet',
        'death':death,
        'animal_id':animal,
        'gen': animal,
        'vaccinations':animal_health_parameter_vaccination,
        'vetexams':animal_health_parameter_vetexam,
        'disposal':animal_disposal_culling,
        'nutritions':animal_nutrition_and_feeding,
        'economic':animal_economics,
        'services':animal_service_record_female,
        'efficiency':animal_efficiency_parameter_female,
        'born_sum':born_sum,
        'weaned_sum':weaned_sum,
        'total_born_weight':total_born_weight,
        'total_weaned_weight':total_weaned_weight,
        'preweaning_mortality':preweaning_mortality,
        #'litter':animal_lifetime_litter_character
        }

        return render(request, "historydatafemale.html", context)

@login_required(login_url='loginuser')
def allpigs(request):
    # animals=general_identification_and_parentage.objects.all()
    animals = general_identification_and_parentage.objects.filter(user=request.user)

    context={
        'animals':animals,
        'tablename':'Tout les animaux de la Ferme',
    }
    return render(request, "allpigs.html", context)



@login_required(login_url='loginuser')
def pigletborn(request):
    if request.method=='POST':
        form=datetodate(request.POST)
        if form.is_valid():
            fromdate=form.cleaned_data['from_date']
            todate=form.cleaned_data['to_date']
            allborn=general_identification_and_parentage.objects.filter(dob__range=(fromdate,todate))
            totalcount=0
            femalecount=0
            malecount=0
            # maleweight = 0
            # femaleweight = 0
            for pig in allborn:
                totalcount+=1
                if pig.gender=='Male':
                    malecount+=1
                    # maleweight += pig.weight  # Si "weight" est un champ dans votre modèle

                elif pig.gender=='Female':
                    femalecount+=1
                    # femaleweight += pig.weight  # Idem

            context={
                'tablename':'Nombre de porcelets nés',
                'malecount':malecount,
                'femalecount':femalecount,
                'totalcount':totalcount,
                # 'maleweight': maleweight,
                # 'femaleweight': femaleweight,
                'form':form
            }
            return render(request, "pigletborn.html",context)

    form=datetodate()
    context={
                'tablename':'Nombre de porcelets nés',
                'malecount':'aucune entrée',
                'femalecount':'aucune entrée',
                'totalcount':'aucune entrée',
                'form':form
            }
    return render(request, "pigletborn.html", context)


@login_required(login_url='loginuser')
def pigletweaned(request):
    if request.method=='POST':
        form=datetodate(request.POST)
        if form.is_valid():
            fromdate=form.cleaned_data['from_date']
            todate=form.cleaned_data['to_date']
            allweanedmale=efficiency_parameter_male.objects.filter(dow__range=(fromdate,todate))
            allweanedfemale=efficiency_parameter_female.objects.filter(dow__range=(fromdate,todate))
            totalcount = 0
            femalecount = 0
            malecount = 0
            maleweight = 0
            femaleweight = 0
            for pig in allweanedmale:
                totalcount +=1
                malecount +=1
                maleweight += pig.weaning_weight
            for pig in allweanedfemale:
                femalecount += 1
                femaleweight += pig.weaning_weight
            context={
                'tablename':'Porcelets sevrés',
                'malecount':malecount,
                'femalecount':femalecount,
                'totalcount':totalcount,
                'maleweight':maleweight,
                'femaleweight':femaleweight,
                'form':form
            }
            return render(request, "pigletweaned.html",context)
    form=datetodate()
    context={
                'tablename':'Porcelets sevrés',
                'malecount':'aucune entrée',
                'femalecount':'aucune entrée',
                'totalcount':'aucune entrée',
                'maleweight':'aucune entrée',
                'femaleweight':'aucune entrée',
                'form':form
            }
    return render(request, "pigletweaned.html", context)



@login_required(login_url='loginuser')
def pigmortality(request):
    if request.method=='POST':
        form=datetodate(request.POST)
        if form.is_valid():
            fromdate=form.cleaned_data['from_date']
            todate=form.cleaned_data['to_date']
            alldead=death.objects.filter(date_death__range=(fromdate,todate))
            print(alldead)
            preweaning=0
            postweaning=0
            for pig in alldead:
                print(pig.gip.gender)
                if pig.gip.gender=='Male':
                    obj=efficiency_parameter_male.objects.get(gip=pig.gip)
                    if obj.dow==None:
                        preweaning+=1
                    else:
                        postweaning+=1
                if pig.gip.gender=='Female':
                    obj=efficiency_parameter_female.objects.get(gip=pig.gip)
                    if obj.dow==None:
                        preweaning+=1
                    else:
                        postweaning+=1
            context={
                'tablename':'Pig Mortality',
                'form':form,
                'postweaning':postweaning,
                'preweaning':preweaning,
            }
            return render(request, "pigmortality.html",context)
    form=datetodate()
    context={
                'tablename':'Pig Mortality',
                'form':form,
                'postweaning':None,
                'preweaning':None,
            }
    return render(request, "pigmortality.html", context)


@login_required(login_url='loginuser')
def revenue_received(request):
    if request.method=='POST':
        form=datetodate(request.POST)
        if form.is_valid():
            fromdate=form.cleaned_data['from_date']
            todate=form.cleaned_data['to_date']
            revenues=disposal_culling.objects.filter(sale_date__range=(fromdate,todate))
            total=0
            for r in revenues:
                total+=r.revenue
            context={
                'tablename':'Revenue Received',
                'form':form,
                'total':total
            }
            return render(request, "revenuereceived.html",context)
    form=datetodate()
    context={
                'tablename':'Revenue Received',
                'form':form,
                'total':None
            }
    return render(request, "revenuereceived.html", context)

@login_required(login_url='loginuser')
def selectpigs(request):
    if request.method=='POST':
        form=selectpigsform(request.POST)
        if form.is_valid():
            n=form.cleaned_data['task']
            num=form.cleaned_data['amount']
            male=[]
            female=[]
            if n=='1':
                animals=general_identification_and_parentage.objects.filter(colitter_size_of_birth__lt=num)
                len_maleanimals=0
                len_femaleanimals=0
                for i in animals:
                    if i.gender=='Male':
                        male.append(i.animal_id)
                        len_maleanimals+=1
                    else:
                        female.append(i.animal_id)
                        len_femaleanimals+=1
                
            elif n=='2':
                animals=general_identification_and_parentage.objects.filter(colitter_size_of_birth__gt=num)
                len_maleanimals=0
                len_femaleanimals=0
                for i in animals:
                    if i.gender=='Male':
                        male.append(i.animal_id)
                        len_maleanimals+=1
                    else:
                        female.append(i.animal_id)
                        len_femaleanimals+=1
                
            elif n=='3':
                maleanimals=efficiency_parameter_male.objects.filter(litter_size_weaning__gte=num)
                for i in maleanimals:
                    male.append(i.gip)
                femaleanimals=efficiency_parameter_female.objects.filter(litter_size_weaning__gte=num)
                for i in femaleanimals:
                    female.append(i.gip)
                len_maleanimals=len(maleanimals)
                len_femaleanimals=len(femaleanimals)
                
            elif n=='4':
                maleanimals=efficiency_parameter_male.objects.filter(litter_size_weaning__exact=num)
                for i in maleanimals:
                    male.append(i.gip)
                len_maleanimals=len(maleanimals)
                femaleanimals=efficiency_parameter_female.objects.filter(litter_size_weaning__exact=num)
                for i in femaleanimals:
                    female.append(i.gip)
                len_femaleanimals=len(femaleanimals)
            
            context={
                'form':form,
                'male': male,
                'female': female,
                'malelen': len_maleanimals,
                'femalelen': len_femaleanimals,
                'tablename':'Select Pigs'
            }
            
            return render(request, "selectpigs.html",context)
    form=selectpigsform()
    return render(request, "selectpigs.html", {'form':form, 'tablename':'Select Pigs'})




@login_required(login_url='loginuser')
def disease(request):
    alldeath=death.objects.all()
    diseaseDict={}
    for i in alldeath:
        cause=i.cause_death
        if cause in diseaseDict:
            diseaseDict[cause]+=1
        else:
            diseaseDict[cause]=1
    context={
        'tablename':'Disease List',
        'diseases':diseaseDict
    }
    return render(request, "disease.html", context)




def account(request):
    return render(request, 'account.html')

def help(request):
    return render(request, 'help.html')