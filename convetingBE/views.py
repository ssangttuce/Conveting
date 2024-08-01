from rest_framework import generics
from .models import DiagnosisSubmit, DiagnosisResult
from .serializers import DiagnosisSubmitSerializer, DiagnosisResultSerializer

class DiagnosisSubmitListCreateView(generics.ListCreateAPIView):
    queryset = DiagnosisSubmit.objects.all()
    serializer_class = DiagnosisSubmitSerializer

class DiagnosisResultRetrieveView(generics.RetrieveAPIView):
    queryset = DiagnosisResult.objects.all()
    serializer_class = DiagnosisResultSerializer
    lookup_field = 'submit_id'

class DiagnosisHistoryListCreateView(generics.ListCreateAPIView):
    queryset = DiagnosisResult.objects.all()
    serializer_class = DiagnosisResultSerializer
