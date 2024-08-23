from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiagnosisHistoryView, SymptomDescriptionViewSet, DiseaseViewSet, DiagnosisViewSet

router = DefaultRouter()
# router.register('symptoms', SymptomDescriptionViewSet)
# router.register('diseases', DiseaseViewSet)
# router.register('diagnosis', DiagnosisViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('diagnosis/history/', DiagnosisHistoryView.as_view(), name='diagnosis-history'),  # 추가된 라우팅
    path('diagnosis/description/', SymptomDescriptionViewSet.as_view(), name='symptom-description')
]
