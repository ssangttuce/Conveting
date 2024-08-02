from rest_framework import serializers
from .models import Pet, DiagnosisSubmit, DiagnosisResult

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class DiagnosisSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisSubmit
        fields = '__all__'

class DiagnosisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisResult
        fields = '__all__'
