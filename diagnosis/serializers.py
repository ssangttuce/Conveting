from rest_framework import serializers
from .models import SymptomDescription, Diagnosis, Disease, Prediction

class SymptomDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomDescription
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ['name', 'symptom', 'cure']

class DiagnosisSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer()

    class Meta:
        model = Diagnosis
        fields = '__all__'

# class PredictionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prediction
#         fields = '__all__'
