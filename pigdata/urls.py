from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('login/', views.loginuser, name='loginuser'),
    path('register/', views.registeruser, name='registeruser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('dataentry/', views.dataentry, name='dataentry'),
    path('report/', views.report, name='report'),
    path('dbsuccess/', views.dbsuccess, name='dbsuccess'),
    path('allpigs/', views.allpigs, name='allpigs'),
    path('delete/<str:animal_id>', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('update/success/', views.successupdate, name='successupdate'), 
    path('create/death/<str:animal_id>', views.deathview, name='deathview'),
    path('create/general/', views.create_general, name='create_general'),
    path('vaccination/<str:animal_id>',views.vaccination, name='vaccination'),
    path('vetexam/<str:animal_id>', views.vetexam, name='vetexam'),
    path('create/disposal/<str:animal_id>', views.create_disposal, name='create_disposal'),
    path('nutrition/<str:animal_id>', views.create_nutrition, name='create_nutrition'),
    path('create/economics/<str:animal_id>', views.create_economics, name='create_economics'),
    path('create/efficiency/<str:animal_id>', views.create_efficiency, name='create_efficiency'),
    path('create/qualification/<str:animal_id>', views.create_qualification, name='create_qualification'),
    path('service/<str:animal_id>', views.create_service, name='create_service'),







    path('update/general/<str:animal_id>', views.update_general, name='update_general'),
    path('update/disposal/<str:animal_id>', views.update_disposal, name='update_disposal'),
    path('update/economics/<str:animal_id>', views.update_economics, name='update_economics'),
    path('update/efficiency/<str:animal_id>', views.update_efficiency, name='update_efficiency'),
    path('update/qualification/<str:animal_id>', views.update_qualification, name='update_qualification'),
    path('update/death/<str:animal_id>', views.update_death, name='update_death'),
    path('update/vaccination/<str:animal_id>', views.update_vaccination, name='update_vaccination'),
    path('update/vetexam/<str:animal_id>', views.update_vetexam, name='update_vetexam'),
    path('update/service/<str:animal_id>', views.update_service, name='update_service'),
    path('update/nutrition/<str:animal_id>', views.update_nutrition, name='update_nutrition'),

    path('report/history/<str:animal_id>', views.history, name='history'),
    path('report/pigletborn', views.pigletborn, name='pigletborn'),
    path('report/pigletweaned', views.pigletweaned, name='pigletweaned'),
    path('report/pigmortality', views.pigmortality, name='pigmortality'),
    path('report/revenue', views.revenue_received, name='revenue_received'),
    path('report/selectpigs', views.selectpigs, name='selectpigs'),
    path('report/disease', views.disease, name='disease'),




    path('deletepigs', views.deletepigs, name='deletepigs'),
    path('delete/service/<str:animal_id>/<int:pk>', views.delete_service, name='deleteservice'),
    path('delete/vaccination/<str:animal_id>/<int:pk>', views.delete_vaccination, name='deletevaccination'),
    path('delete/vetexam/<str:animal_id>/<int:pk>', views.delete_vetexam, name='deletevetexam'),
    path('delete/nutrition/<str:animal_id>/<int:pk>', views.delete_nutrition, name='deletenutrition'),    
    
    path('account/', views.account, name='account'),
    path('help/', views.help, name='help'),

]