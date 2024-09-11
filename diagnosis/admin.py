from django.contrib import admin
from .models import SymptomDescription, Diagnosis, Prediction, Disease

admin.site.register(SymptomDescription)
admin.site.register(Diagnosis)
admin.site.register(Prediction)
admin.site.register(Disease)
