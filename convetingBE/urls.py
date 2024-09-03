from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, DiagnosisHistoryView, DiagnosisView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('home', home, name='home'),
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
    # path('diagnosis/result', DiagnosisView.as_view(), name='diagnosis-result'),
    path('diagnosis/history/', DiagnosisHistoryView.as_view(), name='diagnosis-history')
]
