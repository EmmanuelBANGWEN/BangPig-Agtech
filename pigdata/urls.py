from django.urls import path
from . import views
from . import views_api
from django.urls import path, re_path
from django.views.generic import TemplateView


urlpatterns=[
    path('', views.home, name='home'),
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
    # path('create/economics/<str:animal_id>', views.create_economics, name='create_economics'),
    path('create/efficiency/<str:animal_id>', views.create_efficiency, name='create_efficiency'),
    path('create/qualification/<str:animal_id>', views.create_qualification, name='create_qualification'),
    path('service/<str:animal_id>', views.create_service, name='create_service'),







    path('update/general/<str:animal_id>', views.update_general, name='update_general'),
    path('update/disposal/<str:animal_id>', views.update_disposal, name='update_disposal'),
    # path('update/economics/<str:animal_id>', views.update_economics, name='update_economics'),
    path('update/efficiency/<str:animal_id>', views.update_efficiency, name='update_efficiency'),
    path('update/qualification/<str:animal_id>', views.update_qualification, name='update_qualification'),
    path('update/death/<str:animal_id>', views.update_death, name='update_death'),
    path('update/vaccination/<str:animal_id>', views.update_vaccination, name='update_vaccination'),
    path('update/vetexam/<str:animal_id>', views.update_vetexam, name='update_vetexam'),
    path('update/service/<str:animal_id>', views.update_service, name='update_service'),
    path('update/nutrition/<str:animal_id>', views.update_nutrition, name='update_nutrition'),
    path('update_health_parameter/<int:animal_id>/', views.update_health_parameter, name='update_health_parameter'),


    path('report/history/<str:animal_id>', views.history, name='history'),
    path('report/pigletborn', views.pigletborn, name='pigletborn'),
    path('report/pigletweaned', views.pigletweaned, name='pigletweaned'),
    path('report/pigmortality', views.pigmortality, name='pigmortality'),
    path('report/revenue', views.revenue_received, name='revenue_received'),
    path('report/selectpigs', views.selectpigs, name='selectpigs'),
    path('report/disease', views.disease, name='disease'),




    path('deletepigs/', views.deletepigs, name='deletepigs'),
    path('delete/service/<str:animal_id>/<int:pk>', views.delete_service, name='deleteservice'),
    path('delete/vaccination/<str:animal_id>/<int:pk>', views.delete_vaccination, name='deletevaccination'),
    path('delete/vetexam/<str:animal_id>/<int:pk>', views.delete_vetexam, name='deletevetexam'),
    path('delete/nutrition/<str:animal_id>/<int:pk>', views.delete_nutrition, name='deletenutrition'),    
    
    path('account/', views.account, name='account'),
    path('help/', views.help, name='help'),

    path('search/', views.searchdelete, name='searchdelete'),
    path('searchall/', views.searchupdate, name='searchupdate'),

    path('documentation/', views.documentation, name='documentation'),
    path('tarifs/', views.tarifs, name='tarifs'),

    path('shop/', views.shop, name='shop'),

    path('entercode/', views.enter_subscription_code, name='enter_subscription_code'),
    path('statut/', views.subscription_status, name='subscription_status'),
    path('generate/', views.generate_subscription_code, name='generate_subscription_code'),




























































































    path('api/', views_api.HomeAPIView.as_view(), name='homeapi'),
    path('api/home/', views_api.index_api, name='indexapi'),
    path('api/login/', views_api.api_loginuser, name='loginuserapi'),
    path('api/register/', views_api.api_registeruser, name='registeruserapi'),
    path('api/logout/', views_api.api_logoutuser, name='logoutuserapi'),
    path('api/dataentry/', views_api.dataentry_api, name='dataentryapi'),
    path('api/report/', views_api.report_api, name='reportapi'),
    path('api/dbsuccess/', views_api.dbsuccess_api, name='dbsuccessapi'),
    path('api/allpigs/', views_api.AllPigs.as_view(), name='allpigsapi'),
    path('api/delete/<str:animal_id>', views_api.delete_api, name='deleteapi'),
    path('api/update/<str:animal_id>', views_api.update_animal_info_api, name='updateapi'),
    # path('api/update/success/', views_api.successupdate_api, name='successupdateapi'), 
    path('api/create/death/<str:animal_id>', views_api.deathview_api, name='deathviewapi'),
    path('api/create/general/', views_api.api_create_general, name='create_generalapi'),
    path('api/vaccination/<str:animal_id>',views_api.vaccination_api, name='vaccinationapi'),
    path('api/vetexam/<str:animal_id>', views_api.vetexam_api, name='vetexamapi'),
    path('api/create/disposal/<str:animal_id>', views_api.create_disposal_api, name='create_disposalapi'),
    path('api/nutrition/<str:animal_id>', views_api.create_nutrition_api, name='create_nutritionapi'),
    # path('create/economics/<str:animal_id>', views_api.create_economics, name='create_economicsapi'),
    path('api/create/efficiency/<str:animal_id>', views_api.CreateEfficiencyAPI.as_view(), name='create_efficiencyapi'),
    path('api/create/qualification/<str:animal_id>', views_api.CreateQualificationAPI.as_view(), name='create_qualificationapi'),
    path('api/service/<str:animal_id>', views_api.CreateServiceAPI.as_view(), name='create_serviceapi'),







    path('api/update/general/<str:animal_id>', views_api.UpdateGeneralAPIView.as_view(), name='update_generalapi'),
    path('api/update/disposal/<str:animal_id>', views_api.UpdateDisposalAPIView.as_view(), name='update_disposalapi'),
    # path('update/economics/<str:animal_id>', views_api.update_economics, name='update_economicsapi'),
    path('api/update/efficiency/<str:animal_id>', views_api.update_efficiency_api, name='update_efficiencyapi'),
    path('api/update/qualification/<str:animal_id>', views_api.update_qualification_api, name='update_qualificationapi'),
    path('api/update/death/<str:animal_id>', views_api.update_death_api, name='update_deathapi'),
    path('api/update/vaccination/<str:animal_id>', views_api.update_vaccination_api, name='update_vaccinationapi'),
    path('api/update/vetexam/<str:animal_id>', views_api.update_vetexam_api, name='update_vetexamapi'),
    path('api/update/service/<str:animal_id>', views_api.update_service_api, name='update_serviceapi'),
    path('api/update/nutrition/<str:animal_id>', views_api.UpdateNutritionAPIView.as_view(), name='update_nutritionapi'),
    path('api/update_health_parameter/<int:animal_id>/', views_api.update_health_parameter_api, name='update_health_parameterapi'),


    path('api/report/history/<str:animal_id>', views_api.AnimalHistory.as_view(), name='historyapi'),
    path('api/report/pigletborn', views_api.pigletborn_api, name='pigletbornapi'),
    path('api/report/pigletweaned', views_api.pigletweaned_api, name='pigletweanedapi'),
    path('api/report/pigmortality', views_api.pigmortality_api, name='pigmortalityapi'),
    path('api/report/revenue', views_api.revenue_received_api, name='revenue_receivedapi'),
    path('api/report/selectpigs', views_api.SelectPigsAPIView.as_view(), name='selectpigsapi'),
    path('api/report/disease', views_api.DiseaseAPIView.as_view(), name='diseaseapi'),




    path('api/deletepigs/', views_api.deletepigs_api, name='deletepigsapi'),
    path('api/delete/service/<str:animal_id>/<int:pk>', views_api.delete_service_api, name='deleteserviceapi'),
    path('api/delete/vaccination/<str:animal_id>/<int:pk>', views_api.delete_vaccination_api, name='deletevaccinationapi'),
    path('api/delete/vetexam/<str:animal_id>/<int:pk>', views_api.delete_vetexam_api, name='deletevetexamapi'),
    path('api/delete/nutrition/<str:animal_id>/<int:pk>', views_api.delete_nutrition_api, name='deletenutritionapi'),    
    
    path('api/account/', views_api.AccountAPIView.as_view(), name='accountapi'),
    path('api/help/', views_api.HelpAPIView.as_view(), name='helpapi'),

    path('api/search/', views_api.SearchDeleteAPIView.as_view(), name='searchdeleteapi'),
    path('api/searchall/', views_api.SearchUpdateAPIView.as_view(), name='searchupdateapi'),

    path('api/documentation/', views_api.DocumentationAPIView.as_view(), name='documentationapi'),
    # path('api/tarifs/', views_api.TarifsAPIView.as_view(), name='tarifsapi'),

    # path('api/shop/', views_api.shop, name='shopapi'),

    path('api/entercode/', views_api.enter_subscription_code, name='enter_subscription_codeapi'),
    path('api/statut/', views_api.SubscriptionStatusAPIView.as_view(), name='subscription_statusapi'),
    path('api/generate/', views_api.generate_subscription_code, name='generate_subscription_codeapi'),















#PWA

    re_path(r'^manifest\.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json')),
    re_path(r'^serviceworkerj̇s', TemplateView.as_view(template_name='serviceworker.js', content_type='application/javascript')),




]
