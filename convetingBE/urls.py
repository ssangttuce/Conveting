from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, DiagnosisHistoryView, DiagnosisView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('home', home, name='home'),
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
    # path('diagnosis/result', DiagnosisView.as_view(), name='diagnosis-result'),
    path('diagnosis/history/', DiagnosisHistoryView.as_view(), name='diagnosis-history')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)