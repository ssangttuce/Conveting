from rest_framework import serializers
from .models import SymptomDescription, Prediction, Disease, Diagnosis

class SymptomDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomDescription
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'