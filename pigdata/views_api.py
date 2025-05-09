from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .serializers import *
from datetime import date, timedelta, datetime
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Count, Sum
import pandas as pd
import plotly.io as pio
from collections import defaultdict
import plotly.graph_objects as go
from rest_framework.permissions import AllowAny  # Permet l'accès à tous les utilisateurs
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([AllowAny])  # Permet l'accès à tout le monde
def api_loginuser(request):
    if request.user.is_authenticated:
        return Response({'message': 'User already logged in'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_logoutuser(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])  # Permet l'accès à tous
def api_registeruser(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)  # Connexion automatique après l'inscription
        return Response({'message': 'Inscription réussie'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def api_subscription_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Nécessite une connexion
def dataentry_api(request):
    
    #API pour l'entrée de données.

    return Response({"message": "Que Voulez-Vous faire ?"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Nécessite une connexion
def report_api(request):
    
    #API pour afficher les enregistrements.
    
    return Response({"message": "Mes Enregistrements"}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être connecté
def delete_api(request, animal_id):
    
    #API pour supprimer un animal par son ID.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    animal.delete()
    return Response({"message": f"L'animal {animal_id} a été supprimé avec succès."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être connecté
def deletepigs_api(request):
    
    #API pour afficher les animaux de l'utilisateur à supprimer.
    
    animals = general_identification_and_parentage.objects.filter(user=request.user).order_by('animal_id')
    
    animal_list = [{"animal_id": animal.animal_id, "nom": animal.nom} for animal in animals]

    return Response({"tablename": "Supprimer Un Porc", "animals": animal_list}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être connecté
def delete_service_api(request, animal_id, pk):
    
    #API pour supprimer un service en fonction du genre de l'animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    if animal.gender == 'Male':
        service = get_object_or_404(service_record_male, gip=animal, pk=pk)
    else:
        service = get_object_or_404(service_record_female, gip=animal, pk=pk)

    service.delete()

    return Response({"message": "Service supprimé avec succès."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être connecté
def delete_vaccination_api(request, animal_id, pk):
    
    #API pour supprimer une vaccination d'un animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    vaccination = get_object_or_404(health_parameter_vaccination, gip=animal, pk=pk)

    vaccination.delete()

    return Response({"message": "Vaccination supprimée avec succès."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être connecté
def delete_vetexam_api(request, animal_id, pk):
    
    #API pour supprimer un examen vétérinaire d'un animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    vet_exam = get_object_or_404(health_parameter_vetexam, gip=animal, pk=pk)

    vet_exam.delete()

    return Response({"message": "Examen vétérinaire supprimé avec succès."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # L'utilisateur doit être connecté
def delete_nutrition_api(request, animal_id, pk):
    #API pour supprimer un enregistrement nutritionnel d'un animal.
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    nutrition = get_object_or_404(nutrition_and_feeding, gip=animal, pk=pk)

    nutrition.delete()

    return Response({"message": "Enregistrement nutritionnel supprimé avec succès."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dbsuccess_api(request):
    return Response({"message": "Success"})

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index_api(request):
    user = request.user
    population_sexe = list(general_identification_and_parentage.objects.filter(user=user).values('gender').annotate(total=Count('id')))

    males = efficiency_parameter_male.objects.filter(user=user)
    females = efficiency_parameter_female.objects.filter(user=user)
    recommended_pairs = []

    for male in males:
        for female in females:
            # Vérification des valeurs pour éviter NoneType
            male_weight = male.sexual_maturity_weight or 0
            female_weight = female.sexual_maturity_weight or 0
            litter_size = female.litter_size_weaning or 0

            if (
                male.gip.sire_no != female.gip.sire_no and
                male.gip.dam_no != female.gip.dam_no and
                male.gip.grand_sire != female.gip.grand_sire and
                male.gip.grand_dam != female.gip.grand_dam and
                male_weight >= 90 and
                female_weight >= 90 and
                litter_size >= 8
            ):
                boar_qualification = qualification_boar.objects.filter(gip=male.gip).first()
                if boar_qualification and boar_qualification.suitability == "yes":
                    recommended_pairs.append({
                        "male_id": male.gip.animal_id,
                        "female_id": female.gip.animal_id,
                        "male_weight": male_weight,
                        "female_weight": female_weight,
                        "expected_litter_size": litter_size,
                    })

    population_mois = list(general_identification_and_parentage.objects.filter(user=user).extra(
        {'mois': "strftime('%%Y-%%m', dob)"}
    ).values('mois').annotate(total=Count('id')))
    
    vaccins = list(health_parameter_vaccination.objects.filter(user=user).values('disease').annotate(total=Count('id')))
    
    vaccinations = list(health_parameter_vaccination.objects.filter(user=user).values('disease', 'first_dose', 'booster_dose'))
    
    total_animals = general_identification_and_parentage.objects.filter(user=user).count()
    total_females = general_identification_and_parentage.objects.filter(user=user, gender='Female').count()
    total_males = general_identification_and_parentage.objects.filter(user=user, gender='Male').count()
    six_months_ago = date.today() - timedelta(days=6*30)
    total_piglets = general_identification_and_parentage.objects.filter(user=user, dob__gte=six_months_ago).count()

    return Response({
        "total_animals": total_animals,
        "total_females": total_females,
        "total_males": total_males,
        "total_piglets": total_piglets,
        "population_sexe": population_sexe,
        "population_mois": population_mois,
        "vaccins": vaccins,
        "vaccinations": vaccinations,
        "recommended_pairs": recommended_pairs
    })


# API pour créer un nouvel animal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_general(request):
    serializer = GeneralIdentificationAndParentageSerializer(data=request.data)
    if serializer.is_valid():
        animal_id = serializer.validated_data['animal_id']
        if general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).exists():
            return Response({'error': 'Animal already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @method_decorator(login_required(login_url='loginuser'), name='dispatch')
class CreateEfficiencyAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, animal_id):
        animal = general_identification_and_parentage.objects.filter(animal_id=animal_id, user=request.user).first()
        if not animal:
            return Response({'error': 'Animal not found'}, status=status.HTTP_404_NOT_FOUND)

        gender = animal.gender
        serializer_class = EfficiencyParameterMaleSerializer if gender == 'Male' else EfficiencyParameterFemaleSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            instance = serializer.save(user=request.user, gip=animal)

            if instance.dow and animal.dob:
                instance.weaning_age = (instance.dow - animal.dob).days
                instance.save()

            return Response({'message': 'Efficiency parameters saved successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API pour récupérer la liste des animaux
def api_list_animals(request):
    animals = general_identification_and_parentage.objects.filter(user=request.user)
    serializer = GeneralIdentificationAndParentageSerializer(animals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




# API pour récupérer les meilleures combinaisons mâle/femelle
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_recommended_pairs(request):
    user = request.user
    males = efficiency_parameter_male.objects.filter(user=user)
    females = efficiency_parameter_female.objects.filter(user=user)
    recommended_pairs = []

    for male in males:
        for female in females:
            if (
                male.gip.sire_no != female.gip.sire_no and
                male.gip.dam_no != female.gip.dam_no and
                male.gip.grand_sire != female.gip.grand_sire and
                male.gip.grand_dam != female.gip.grand_dam
            ):
                if (
                    male.sexual_maturity_weight and
                    female.sexual_maturity_weight and
                    male.sexual_maturity_weight >= 90 and
                    female.sexual_maturity_weight >= 90 and
                    female.litter_size_weaning >= 8
                ):
                    boar_qualification = qualification_boar.objects.filter(gip=male.gip).first()
                    if boar_qualification and boar_qualification.suitability == "yes":
                        recommended_pairs.append({
                            "male_id": male.gip.animal_id,
                            "female_id": female.gip.animal_id,
                            "male_weight": male.sexual_maturity_weight,
                            "female_weight": female.sexual_maturity_weight,
                            "expected_litter_size": female.litter_size_weaning,
                        })

    return Response(recommended_pairs, status=status.HTTP_200_OK)









class CreateQualificationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, animal_id):
        animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
        
        if animal.gender == 'Female':
            return Response({'redirect': 'create_service'}, status=status.HTTP_302_FOUND)
        
        serializer = QualificationBoarSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(user=request.user, gip=animal)
            return Response({'message': 'Qualification created successfully', 'qualification_id': obj.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateServiceAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, animal_id):
        animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
        
        if animal.gender == 'Male':
            service_model = service_record_male
            serializer_class = ServiceRecordMaleSerializer
        else:
            service_model = service_record_female
            serializer_class = ServiceRecordFemaleSerializer
        
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user, gip=animal)
            
            instance.born_total = instance.born_female + instance.born_male
            instance.total_weaned = instance.weaned_female + instance.weaned_male
            instance.save()
            
            return Response({'message': 'Service record created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required(login_url='loginuser')
def vaccination_api(request, animal_id):
    # Récupérer l'animal associé à l'utilisateur
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Si la méthode est GET, récupérer les vaccinations de l'animal
    if request.method == 'GET':
        vaccinations = health_parameter_vaccination.objects.filter(gip=animal)
        serializer = VaccinationSerializer(vaccinations, many=True)
        return Response(serializer.data)

    # Si la méthode est POST, créer une nouvelle vaccination
    elif request.method == 'POST':
        serializer = VaccinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, gip=animal)  # Associer l'utilisateur et l'animal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@login_required(login_url='loginuser')
def vetexam_api(request, animal_id):
    # Récupérer l'animal associé à l'utilisateur
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Si la méthode est GET, récupérer les examens vétérinaires de l'animal
    if request.method == 'GET':
        vet_exams = health_parameter_vetexam.objects.filter(gip=animal)
        serializer = VetExamSerializer(vet_exams, many=True)
        return Response(serializer.data)

    # Si la méthode est POST, créer un nouvel examen vétérinaire
    elif request.method == 'POST':
        serializer = VetExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, gip=animal)  # Associer l'utilisateur et l'animal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required(login_url='loginuser')
def create_nutrition_api(request, animal_id):
    # Récupérer l'animal associé à l'utilisateur
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Si la méthode est GET, récupérer les enregistrements de nutrition
    if request.method == 'GET':
        nutritions = nutrition_and_feeding.objects.filter(gip=animal)
        serializer = NutritionSerializer(nutritions, many=True)
        return Response(serializer.data)

    # Si la méthode est POST, créer une nouvelle nutrition
    elif request.method == 'POST':
        serializer = NutritionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, gip=animal)  # Associer l'utilisateur et l'animal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required(login_url='loginuser')
def deathview_api(request, animal_id):
    # Récupérer l'animal associé à l'utilisateur
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Si la méthode est GET, récupérer les informations sur la mort de l'animal
    if request.method == 'GET':
        death_info = death.objects.filter(gip=animal)
        serializer = DeathSerializer(death_info, many=True)
        return Response(serializer.data)

    # Si la méthode est POST, enregistrer les informations sur la mort de l'animal
    elif request.method == 'POST':
        serializer = DeathSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, gip=animal)  # Associer l'utilisateur et l'animal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@login_required(login_url='loginuser')
def create_disposal_api(request, animal_id):
    # Récupérer l'animal associé à l'utilisateur
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Si la méthode est GET, récupérer les enregistrements de disposal
    if request.method == 'GET':
        disposals = disposal_culling.objects.filter(gip=animal)
        serializer = DisposalSerializer(disposals, many=True)
        return Response(serializer.data)

    # Si la méthode est POST, créer un nouvel enregistrement de disposal
    elif request.method == 'POST':
        serializer = DisposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, gip=animal)  # Associer l'utilisateur et l'animal
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def api_successupdate


@api_view(['GET', 'PUT'])
@login_required(login_url='loginuser')
def update_animal_info_api(request, animal_id):
    # Récupérer l'animal associé à l'utilisateur
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    if request.method == 'GET':
        # Sérialiser l'animal pour envoyer les données
        serializer = GeneralIdentificationAndParentageSerializer(animal)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Sérialiser les nouvelles données de l'animal
        serializer = GeneralIdentificationAndParentageSerializer(animal, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Mettre à jour l'animal
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGeneralAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, animal_id, user):
        try:
            return general_identification_and_parentage.objects.get(animal_id=animal_id, user=user)
        except general_identification_and_parentage.DoesNotExist:
            return None

    def put(self, request, animal_id):
        animal = self.get_object(animal_id, request.user)
        if not animal:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GeneralIdentificationAndParentageSerializer(animal, data=request.data, partial=True)  # partial=True pour la mise à jour
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Animal general updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDisposalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_animal(self, animal_id, user):
        try:
            return general_identification_and_parentage.objects.get(animal_id=animal_id, user=user)
        except general_identification_and_parentage.DoesNotExist:
            return None

    def get_disposal_instance(self, animal):
        disposal_instance, created = disposal_culling.objects.get_or_create(gip=animal)
        return disposal_instance

    def put(self, request, animal_id):
        animal = self.get_animal(animal_id, request.user)
        if not animal:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

        disposal_instance = self.get_disposal_instance(animal)
        serializer = DisposalCullingSerializer(disposal_instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "Disposal updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateNutritionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_animal(self, animal_id, user):
        try:
            return general_identification_and_parentage.objects.get(animal_id=animal_id, user=user)
        except general_identification_and_parentage.DoesNotExist:
            return None

    def get_nutrition_instance(self, animal):
        # Création automatique s’il n’existe pas (comme dans Disposal)
        nutrition_instance, created = nutrition_and_feeding.objects.get_or_create(gip=animal)
        return nutrition_instance

    def put(self, request, animal_id):
        animal = self.get_animal(animal_id, request.user)
        if not animal:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

        nutrition_instance = self.get_nutrition_instance(animal)
        serializer = NutritionAndFeedingSerializer(nutrition_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Associer à l'utilisateur connecté
            return Response({"detail": "Nutrition updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_efficiency_api(request, animal_id):
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    gender = animal.gender
    
    def calculate_age(dob, dow):
        if isinstance(dob, str):
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        if isinstance(dow, str):
            dow = datetime.strptime(dow, '%Y-%m-%d').date()
        return (dow - dob).days if dob and dow else None
    
    if gender == 'Male':
        animal_efficiency, created = efficiency_parameter_male.objects.get_or_create(gip=animal)
        serializer = EfficiencyParameterMaleSerializer(animal_efficiency, data=request.data, partial=True)
    else:
        animal_efficiency, created = efficiency_parameter_female.objects.get_or_create(gip=animal)
        serializer = EfficiencyParameterFemaleSerializer(animal_efficiency, data=request.data, partial=True)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"message": "Mise à jour efficiency réussie", "data": serializer.data}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"error": f"Erreur d'intégrité : {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_qualification_api(request, animal_id):
    
    #API pour mettre à jour la qualification d'un animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    qualification_instance, created = qualification_boar.objects.get_or_create(gip=animal)

    if request.method == 'GET':
        serializer = QualificationBoarSerializer(qualification_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QualificationBoarSerializer(qualification_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_death_api(request, animal_id):
    
    #API pour mettre à jour les informations de décès d'un animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)
    death_instance, created = death.objects.get_or_create(gip=animal)

    if request.method == 'GET':
        serializer = DeathSerializer(death_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DeathSerializer(death_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_service_api(request, animal_id):
    
    #API pour récupérer et mettre à jour les services d'un animal (mâle ou femelle).
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    # Vérifier le genre et sélectionner le bon modèle
    if animal.gender == 'Female':
        service_model = service_record_female
        serializer_class = ServiceRecordFemaleSerializer
    elif animal.gender == 'Male':
        service_model = service_record_male
        serializer_class = ServiceRecordMaleSerializer
    else:
        return Response({"error": "Invalid gender"}, status=status.HTTP_400_BAD_REQUEST)

    # Récupérer l'enregistrement de service associé à l'animal
    service_instance, created = service_model.objects.get_or_create(gip=animal)

    if request.method == 'GET':
        serializer = serializer_class(service_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializer_class(service_instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            instance.born_total = instance.born_female + instance.born_male
            instance.total_weaned = instance.weaned_female + instance.weaned_male
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
# def update_health_parameter_api(request, animal_id, model_type):
    
#     #API pour récupérer et mettre à jour les paramètres de santé d'un animal.
#     #- model_type: 'vet_exam' ou 'vaccination'
    
#     animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

#     # Vérifier le type de modèle demandé
#     if model_type == 'vet_exam':
#         model_class = health_parameter_vetexam
#         serializer_class = VetExamSerializer
#     elif model_type == 'vaccination':
#         model_class = health_parameter_vaccination
#         serializer_class = VaccinationSerializer
#     else:
#         return Response({"error": "Invalid model type"}, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'GET':
#         health_parameters = model_class.objects.filter(gip=animal)
#         serializer = serializer_class(health_parameters, many=True)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = serializer_class(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save(gip=animal, user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_vaccination_api(request, animal_id):
    
    #API pour récupérer et ajouter des vaccinations à un animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    if request.method == 'GET':
        vaccinations = health_parameter_vaccination.objects.filter(gip=animal)
        serializer = VaccinationSerializer(vaccinations, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VaccinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gip=animal, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_vetexam_api(request, animal_id):
    
    #API pour récupérer et ajouter des examens vétérinaires à un animal.
    
    animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

    if request.method == 'GET':
        vet_exams = health_parameter_vetexam.objects.filter(gip=animal)
        serializer = VetExamSerializer(vet_exams, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VetExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gip=animal, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def api_update_vetexam


class AnimalHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, animal_id):
        # Récupérer l'animal de l'utilisateur actuel
        animal = get_object_or_404(general_identification_and_parentage, animal_id=animal_id, user=request.user)

        # Récupérer les paramètres de santé et autres données liées à l'animal
        animal_health_parameter_vaccination = health_parameter_vaccination.objects.filter(gip=animal)
        animal_health_parameter_vetexam = health_parameter_vetexam.objects.filter(gip=animal)
        animal_nutrition_and_feeding = nutrition_and_feeding.objects.filter(gip=animal)
        animal_disposal_culling = disposal_culling.objects.filter(gip=animal).first()
        animal_death = death.objects.filter(gip=animal).first()

        # Selon le sexe de l'animal
        if animal.gender == 'Male':
            animal_efficiency_parameter = efficiency_parameter_male.objects.filter(gip=animal).first()
            animal_qualification_boar = qualification_boar.objects.filter(gip=animal).first()
            animal_service_record = service_record_male.objects.filter(gip=animal)

            data = {
                'death': DeathSerializer(animal_death).data,
                'animal': GeneralIdentificationAndParentageSerializer(animal).data,
                'vaccinations': HealthParameterVaccinationSerializer(animal_health_parameter_vaccination, many=True).data,
                'vetexams': HealthParameterVetExamSerializer(animal_health_parameter_vetexam, many=True).data,
                'disposal': DisposalCullingSerializer(animal_disposal_culling).data,
                'nutritions': NutritionAndFeedingSerializer(animal_nutrition_and_feeding, many=True).data,
                'efficiency': EfficiencyParameterMaleSerializer(animal_efficiency_parameter).data,
                'qualification': ServiceRecordMaleSerializer(animal_service_record, many=True).data,
            }

        elif animal.gender == 'Female':
            animal_efficiency_parameter = efficiency_parameter_female.objects.filter(gip=animal).first()
            animal_service_record_female = service_record_female.objects.filter(gip=animal)

            born_sum = sum(i.born_total for i in animal_service_record_female)
            weaned_sum = sum(i.total_weaned for i in animal_service_record_female)
            total_born_weight = sum(i.litter_weight_birth for i in animal_service_record_female)
            total_weaned_weight = sum(i.weaning_weight for i in animal_service_record_female)

            preweaning_mortality = (born_sum - weaned_sum) * 100.0 / born_sum if born_sum else 0

            data = {
                'death': DeathSerializer(animal_death).data,
                'animal': GeneralIdentificationAndParentageSerializer(animal).data,
                'vaccinations': HealthParameterVaccinationSerializer(animal_health_parameter_vaccination, many=True).data,
                'vetexams': HealthParameterVetExamSerializer(animal_health_parameter_vetexam, many=True).data,
                'disposal': DisposalCullingSerializer(animal_disposal_culling).data,
                'nutritions': NutritionAndFeedingSerializer(animal_nutrition_and_feeding, many=True).data,
                'efficiency': EfficiencyParameterFemaleSerializer(animal_efficiency_parameter).data,
                'services': ServiceRecordFemaleSerializer(animal_service_record_female, many=True).data,
                'born_sum': born_sum,
                'weaned_sum': weaned_sum,
                'total_born_weight': total_born_weight,
                'total_weaned_weight': total_weaned_weight,
                'preweaning_mortality': preweaning_mortality,
            }

        return Response(data)


class AllPigs(APIView):
    permission_classes = [IsAuthenticated]  # La permission doit être définie ici

    def get(self, request):
        animals = general_identification_and_parentage.objects.filter(user=request.user).order_by('animal_id')
        data = GeneralIdentificationAndParentageSerializer(animals, many=True).data
        return Response({
            'animals': data,
            'tablename': 'Tous les animaux de la Ferme',
        })

    def post(self, request):
        serializer = GeneralIdentificationAndParentageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associe l'utilisateur connecté à l'objet
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def pigletborn_api(request):
    if request.method == 'POST':
        form = datetodate(request.data)
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']
            
            # Filtrer les données en fonction des dates et de l'utilisateur
            allborn = general_identification_and_parentage.objects.filter(
                dob__range=(fromdate, todate),
                user=request.user
            )

            totalcount = allborn.count()
            malecount = allborn.filter(gender='Male').count()
            femalecount = allborn.filter(gender='Female').count()

            # Créer un DataFrame avec les données filtrées
            df = pd.DataFrame.from_records(allborn.values('dob', 'gender'))
            df['dob'] = pd.to_datetime(df['dob'])
            
            # Comptage des naissances par jour
            birth_count = df.groupby('dob').size().reset_index(name='Nombre de porcelets')
            fig = px.line(
                birth_count, 
                x='dob', 
                y='Nombre de porcelets', 
                color_discrete_sequence=['green'],
                title="Nombre de porcelets nés par jour",
                labels={'dob': 'Date', 'Nombre de porcelets': 'Nombre de porcelets nés'},
            )

            # Graphique de la répartition par genre
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

            return Response({
                'totalcount': totalcount,
                'malecount': malecount,
                'femalecount': femalecount,
                'graph_json': graph_json,
                'graph_json2': graph_json2,
            })
        else:
            return Response({'message': 'Formulaire invalide'}, status=400)

    return Response({'message': 'Méthode non autorisée'}, status=405)

@api_view(['POST'])
def pigletweaned_api(request):
    if request.method == 'POST':
        form = datetodate(request.data)
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']

            # Filtrer les données de sevrage
            allweanedmale = efficiency_parameter_male.objects.filter(
                dow__range=(fromdate, todate), user=request.user
            )
            allweanedfemale = efficiency_parameter_female.objects.filter(
                dow__range=(fromdate, todate), user=request.user
            )

            totalcount = allweanedmale.count() + allweanedfemale.count()
            malecount = allweanedmale.count()
            femalecount = allweanedfemale.count()

            # Créer un DataFrame pour chaque sexe
            df = pd.DataFrame.from_records(allweanedmale.values('dow'))
            df2 = pd.DataFrame.from_records(allweanedfemale.values('dow'))
            
            # Traitement des DataFrames
            df['dow'] = pd.to_datetime(df['dow'])
            weaned_count = df.groupby('dow').size().reset_index(name='Nombre de porcelets')
            weaned_count['Genre'] = 'Mâles'

            df2['dow'] = pd.to_datetime(df2['dow'])
            weaned_count2 = df2.groupby('dow').size().reset_index(name='Nombre de porcelets')
            weaned_count2['Genre'] = 'Femelles'

            # Fusionner les DataFrames
            df_final = pd.concat([weaned_count, weaned_count2])

            # Graphique pour les porcelets sevrés
            if not df_final.empty:
                fig = px.line(
                    df_final, 
                    x='dow', 
                    y='Nombre de porcelets', 
                    color='Genre',
                    color_discrete_sequence=['green', 'red'],
                    title="Nombre de porcelets sevrés par jour",
                    labels={'dow': 'Date', 'Nombre de porcelets': 'Nombre de porcelets sevrés'},
                )
                graph_json = pio.to_html(fig, full_html=False)

            # Graphique de répartition par genre
            if malecount > 0 or femalecount > 0:
                fig2 = px.bar(
                    x=['Mâles', 'Femelles'], 
                    y=[malecount, femalecount], 
                    title="Répartition des porcelets sevrés par genre",
                    labels={'x': 'Genre', 'y': 'Nombre'},
                    color=['Mâles', 'Femelles'], 
                    color_discrete_sequence=['green', 'red']
                )
                graph_json2 = pio.to_html(fig2, full_html=False)

            return Response({
                'totalcount': totalcount,
                'malecount': malecount,
                'femalecount': femalecount,
                'graph_json': graph_json,
                'graph_json2': graph_json2,
            })
        else:
            return Response({'message': 'Formulaire invalide'}, status=400)

    return Response({'message': 'Méthode non autorisée'}, status=405)

from rest_framework.response import Response
from rest_framework import status

def subscription_required(view_func):
    # Vérifie si l'utilisateur a un abonnement actif
    def _wrapped_view(request, *args, **kwargs):
        # Récupérer ou créer l'abonnement de l'utilisateur
        subscription, created = Subscription.objects.get_or_create(user=request.user)

        if not subscription.is_valid():
            # Retourner une réponse JSON appropriée avec un message d'erreur
            return Response(
                {"error": "Votre abonnement a expiré. Veuillez entrer un nouveau code."},
                status=status.HTTP_403_FORBIDDEN  # Forbidden
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view


@api_view(['POST'])
@subscription_required
@login_required(login_url='loginuser')
def pigmortality_api(request):
    if request.method == 'POST':
        form = datetodate(request.data)  # Utilisation de request.data pour DRF
        if form.is_valid():
            fromdate = form.cleaned_data['from_date']
            todate = form.cleaned_data['to_date']

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

            if alldead.exists():
                df = pd.DataFrame.from_records(alldead.values('date_death'))
                df['date_death'] = pd.to_datetime(df['date_death'])
                death_count = df.groupby('date_death').size().reset_index(name='Nombre de décès')

                fig = px.line(
                    death_count, 
                    x='date_death', 
                    y='Nombre de décès', 
                    title="Nombre de décès de porcelets par jour",
                    labels={'date_death': 'Date', 'Nombre de décès': 'Nombre de décès'},
                    color_discrete_sequence=['red'],
                )
                graph_json = pio.to_html(fig, full_html=False)
            else:
                graph_json = None

            data = {
                'postweaning': postweaning,
                'preweaning': preweaning,
                'graph_json': graph_json,
            }

            return Response(data, status=status.HTTP_200_OK)

    return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@subscription_required
@login_required(login_url='loginuser')
def revenue_received_api(request):
    graph_json = None
    graph_json2 = None
    total = 0

    form = datetodate(request.data)
    if request.method == 'POST' and form.is_valid():
        fromdate = form.cleaned_data['from_date']
        todate = form.cleaned_data['to_date']

        revenues = disposal_culling.objects.filter(
            sale_date__range=(fromdate, todate),
            user=request.user
        )

        if revenues.exists():
            total = revenues.aggregate(Sum('revenue'))['revenue__sum'] or 0

            # Graphique 1 : Nombre de ventes par jour
            df = pd.DataFrame.from_records(revenues.values('sale_date'))
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            sales_count = df.groupby('sale_date').size().reset_index(name='Nombre de ventes')

            fig = px.line(
                sales_count,
                x='sale_date',
                y='Nombre de ventes',
                color_discrete_sequence=['green'],
                title="Nombre de ventes par jour",
                labels={'sale_date': 'Date', 'Nombre de ventes': 'Nombre de ventes'},
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
            )
            graph_json2 = pio.to_html(fig2, full_html=False)

        else:
            graph_json = "<p style='color: red;'>Aucune vente enregistrée pour cette période.</p>"
            graph_json2 = "<p style='color: red;'>Aucun revenu généré pour cette période.</p>"

        data = {
            'total': total,
            'graph_json': graph_json,
            'graph_json2': graph_json2,
        }
        return Response(data, status=status.HTTP_200_OK)

    return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

from .serializers import SelectPigsSerializer  # Assure-toi d’importer le bon

class SelectPigsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SelectPigsSerializer(data=request.data)
        if serializer.is_valid():
            n = serializer.validated_data['task']
            num = serializer.validated_data['amount']
            male = []
            female = []

            if n == '1':
                animals = general_identification_and_parentage.objects.filter(
                    colitter_size_of_birth__lt=num,
                    user=request.user
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

            if n in ['1', '2']:
                male = [i.animal_id for i in animals if i.gender == 'Male']
                female = [i.animal_id for i in animals if i.gender != 'Male']
            else:
                male = [i.gip for i in maleanimals]
                female = [i.gip for i in femaleanimals]

            return Response({
                'male': male,
                'female': female,
                'malelen': len(male),
                'femalelen': len(female)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiseaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filtrer les décès par utilisateur connecté
        alldeath = death.objects.filter(user=request.user)

        diseaseDict = {}
        for i in alldeath:
            cause = i.cause_death
            diseaseDict[cause] = diseaseDict.get(cause, 0) + 1  # Utilisation de .get() pour simplifier

        return Response({'diseases': diseaseDict}, status=status.HTTP_200_OK)


class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Récupérer l'abonnement de l'utilisateur connecté
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        return Response({
            'subscription': SubscriptionSerializer(subscription).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Saisir le code d'abonnement pour validation
        code = request.data.get('code')

        try:
            subscription = Subscription.objects.get(code=code)
            if subscription.expires_at > datetime.now():
                # Mettre à jour l'abonnement de l'utilisateur
                request.user.subscription.code = code
                request.user.subscription.expires_at = subscription.expires_at
                request.user.subscription.save()

                return Response({"message": "Abonnement activé avec succès !"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Ce code a expiré."}, status=status.HTTP_400_BAD_REQUEST)
        except Subscription.DoesNotExist:
            return Response({"error": "Code invalide."}, status=status.HTTP_400_BAD_REQUEST)


class HelpAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Désérialiser les données du formulaire
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Récupération des données
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            number = serializer.validated_data['number']
            message = serializer.validated_data['message']

            # Enregistrer le message dans la base de données
            contact = Contact.objects.create(
                name=name,
                email=email,
                number=number,
                message=message
            )

            # Envoi de l'email
            send_mail(
                subject=f"Nouveau message de {name}",
                message=f"De : {name}\nNuméro : {number}\n Email: {email}\n\nMessage: {message}",
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({"message": "Votre message a été envoyé avec succès !"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class SearchDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        results = []

        if query:
            results = general_identification_and_parentage.objects.filter(animal_id=query, user=request.user)

        # Sérialisation des résultats
        serializer = GeneralIdentificationAndParentageSerializer(results, many=True)

        return Response({
            'query': query,
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class SearchUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        results = []

        if query:
            results = general_identification_and_parentage.objects.filter(animal_id=query, user=request.user)

        # Sérialisation des résultats
        serializer = GeneralIdentificationAndParentageSerializer(results, many=True)

        return Response({
            'query': query,
            'results': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Mise à jour de l'animal
        query = request.data.get('query', None)
        updated_data = request.data.get('updated_data', None)

        if query and updated_data:
            try:
                animal = general_identification_and_parentage.objects.get(animal_id=query, user=request.user)
                for key, value in updated_data.items():
                    setattr(animal, key, value)  # Mise à jour des attributs
                animal.save()

                serializer = GeneralIdentificationAndParentageSerializer(animal)
                return Response({
                    'message': 'Animal mis à jour avec succès',
                    'animal': serializer.data
                }, status=status.HTTP_200_OK)
            except general_identification_and_parentage.DoesNotExist:
                return Response({'error': 'Animal non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Query ou données de mise à jour manquantes'}, status=status.HTTP_400_BAD_REQUEST)


class HomeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            'message': 'Bienvenue sur la page d\'accueil de Bangri!'
        }, status=status.HTTP_200_OK)

class DocumentationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'message': f"Bonjour {request.user.username}, vous êtes sur la documentation."
        }, status=status.HTTP_200_OK)


# class TarifsAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         tarifs = [
#             {'plan': 'Basique', 'price': 10, 'description': 'Accès aux fonctionnalités de base.'},
#             {'plan': 'Premium', 'price': 30, 'description': 'Accès aux fonctionnalités avancées.'},
#             {'plan': 'Entreprise', 'price': 100, 'description': 'Accès complet pour les grandes entreprises.'}
#         ]
#         return Response({
#             'tarifs': tarifs
#         }, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_subscription_code(request):
    if not request.user.is_staff:
        return Response({'error': 'Vous n\'avez pas l\'autorisation de générer un code.'}, status=status.HTTP_403_FORBIDDEN)

    subscription, created = Subscription.objects.get_or_create(user=request.user)
    subscription.generate_new_code()  # Génère un code mais ne l'active pas
    return Response({
        'message': 'Code généré ! Un admin doit maintenant l\'activer.'
    }, status=status.HTTP_200_OK)


class SubscriptionStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(user=request.user)
            return Response({
                'status': 'success',
                'subscription': {
                    'code': subscription.code,
                    'expires_at': subscription.expires_at,
                    'is_active': subscription.is_active,
                }
            }, status=200)
        except Subscription.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Aucun abonnement trouvé pour cet utilisateur.'
            }, status=404)


@api_view(['POST'])
def enter_subscription_code(request):
    # Permet à l'utilisateur de saisir un code fourni par l'admin

    # Vérifie si l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return Response({
            'status': 'error',
            'message': 'Vous devez être connecté pour entrer un code.'
        }, status=403)

    code = request.data.get("code")  # Récupère le code envoyé dans la requête

    if not code:
        return Response({
            'status': 'error',
            'message': 'Le code d\'abonnement est requis.'
        }, status=400)

    try:
        subscription = Subscription.objects.get(code=code)

        # Vérifie si le code est valide
        if subscription.is_valid():
            # Met à jour l'abonnement de l'utilisateur
            request.user.subscription.code = code
            request.user.subscription.expires_at = subscription.expires_at
            request.user.subscription.save()

            return Response({
                'status': 'success',
                'message': 'Abonnement activé avec succès!'
            }, status=200)
        
        elif not subscription.is_active:
            return Response({
                'status': 'error',
                'message': 'Ce code n\'a pas encore été activé.'
            }, status=400)
        else:
            return Response({
                'status': 'error',
                'message': 'Ce code a expiré.'
            }, status=400)
    
    except Subscription.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Code d\'abonnement invalide.'
        }, status=400)


# @api_view(['GET'])
# def shop(request):
#     # Récupère tous les produits du magasin et les retourne sous forme de JSON

#     # Récupère tous les produits disponibles dans le magasin
#     products = Product.objects.all()

#     # Crée une liste de dictionnaires représentant chaque produit
#     product_list = []
#     for product in products:
#         product_list.append({
#             'id': product.id,
#             'name': product.name,
#             'description': product.description,
#             'price': str(product.price),  # Convertit le prix en chaîne pour le format JSON
#             'stock': product.stock
#         })

#     # Retourne la liste des produits au format JSON
#     return Response({
#         'status': 'success',
#         'products': product_list
#     }, status=status.HTTP_200_OK)


