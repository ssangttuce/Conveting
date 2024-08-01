from rest_framework import serializers
from .models import Pet, DiagnosisSubmission, DiagnosisResult

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class DiagnosisSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisSubmission
        fields = '__all__'

class DiagnosisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisResult
        fields = '__all__'
