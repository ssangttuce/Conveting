from django.contrib import admin
from .models import Pet, DiagnosisSubmission, DiagnosisResult

admin.site.register(Pet)
admin.site.register(DiagnosisSubmission)
admin.site.register(DiagnosisResult)
