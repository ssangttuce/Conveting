from django.contrib import admin
from .models import Pets, Diagnosis, Prediction, Disease, ResultAI

admin.site.register(Pets)
admin.site.register(Diagnosis)
admin.site.register(Prediction)
admin.site.register(Disease)
admin.site.register(ResultAI)
