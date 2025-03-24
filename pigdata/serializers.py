# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import *

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)


# class RegisterSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
#         return data

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password1'])
#         user.save()
#         return user


# class GeneralIdentificationAndParentageSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = general_identification_and_parentage
#         fields = '__all__'

# class HealthParameterVaccinationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = health_parameter_vaccination
#         fields = '__all__'

# class HealthParameterVetExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = health_parameter_vetexam
#         fields = '__all__'

# class DisposalCullingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = disposal_culling
#         fields = '__all__'

# class NutritionAndFeedingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = nutrition_and_feeding
#         fields = '__all__'

# class VaccinationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = health_parameter_vaccination
#         fields = '__all__'

# class DeathSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = death
#         fields = '__all__'

# class VetExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = health_parameter_vetexam
#         fields = '__all__'

# class EfficiencyParameterMaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = efficiency_parameter_male
#         fields = '__all__'

# class EfficiencyParameterFemaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = efficiency_parameter_female
#         fields = '__all__'

# class QualificationBoarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = qualification_boar
#         fields = '__all__'

# class NutritionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = nutrition_and_feeding
#         fields = '__all__'

# class DisposalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = disposal_culling
#         fields = '__all__'

# class ServiceRecordMaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service_record_male
#         fields = '__all__'

# class ServiceRecordFemaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service_record_female
#         fields = '__all__'

# class LifetimeLitterCharacterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = lifetime_litter_character
#         fields = '__all__'

# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = '__all__'

# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = '__all__'

