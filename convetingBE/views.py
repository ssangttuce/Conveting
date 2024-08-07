from rest_framework import viewsets
from .models import SymptomDescription, Prediction, Disease, Diagnosis
from .serializers import SymptomDescriptionSerializer, PredictionSerializer, DiseaseSerializer, DiagnosisSerializer

class SymptomDescriptionViewSet(viewsets.ModelViewSet):
    queryset = SymptomDescription.objects.all()
    serializer_class = SymptomDescriptionSerializer

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
