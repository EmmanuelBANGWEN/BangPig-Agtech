from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(general_identification_and_parentage)
admin.site.register(health_parameter_vaccination)
admin.site.register(health_parameter_vetexam)
admin.site.register(disposal_culling)
admin.site.register(nutrition_and_feeding)
# admin.site.register(economics)
admin.site.register(death)
admin.site.register(efficiency_parameter_male)
admin.site.register(efficiency_parameter_female)
admin.site.register(qualification_boar)
admin.site.register(service_record_male)
admin.site.register(service_record_female)
admin.site.register(lifetime_litter_character)