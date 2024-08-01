from django.urls import path
from .views import DiagnosisSubmitListCreateView, DiagnosisResultRetrieveView, DiagnosisHistoryListCreateView

urlpatterns = [
    path('diagnosis/Submit/', DiagnosisSubmitListCreateView.as_view(), name='diagnosis_submit'),
    path('diagnosis/result/<int:submit_id>/', DiagnosisResultRetrieveView.as_view(), name='diagnosis_result'),
    path('diagnosis/history/', DiagnosisHistoryListCreateView.as_view(), name='diagnosis_history'),
]
