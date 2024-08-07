from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SymptomDescriptionViewSet, PredictionViewSet, DiseaseViewSet, DiagnosisViewSet

router = DefaultRouter()
router.register('symptoms', SymptomDescriptionViewSet)
router.register('predictions', PredictionViewSet)
router.register('diseases', DiseaseViewSet)
router.register('diagnoses', DiagnosisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
