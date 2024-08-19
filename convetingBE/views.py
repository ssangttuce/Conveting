import os
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import models
from .models import SymptomDescription, Disease, Diagnosis
from .serializers import SymptomDescriptionSerializer, DiseaseSerializer, DiagnosisSerializer
from .utils import run_diagnosis  # 예측 함수를 임포트

class DiagnosisHistoryView(APIView):
    def get(self, request, user_id):
        try:
            # SymptomDescription 테이블에서 해당 user_id로 필터링
            symptoms = SymptomDescription.objects.filter(owner=user_id)
            
            # symptoms의 seq 번호를 이용하여 Diagnosis 테이블에서 해당 진단 내역 조회
            diagnosis_list = Diagnosis.objects.filter(seq__in=symptoms)
            
            # 조회된 Diagnosis 데이터를 직렬화
            serializer = DiagnosisSerializer(diagnosis_list, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except SymptomDescription.DoesNotExist:
            return Response({"error": "No history found for this user."}, status=status.HTTP_404_NOT_FOUND)

class SymptomDescriptionViewSet(APIView):
    def post(self, request, *args, **kwargs):
        # 요청 데이터에서 owner, pet, photo 정보 가져오기
        owner = request.data.get('owner')
        pet = request.data.get('pet')
        photo = request.FILES.get('photo')  # 파일은 FILES에서 가져옵니다
        part = request.data.get('part')  # 진단 부위 ('eye' 또는 'skin')

        if not owner or not pet or not photo:
            return Response({"error": "owner, pet, and photo are required fields."}, status=status.HTTP_400_BAD_REQUEST)
    
        # 파일 이름과 확장자 분리
        file_name, file_extension = os.path.splitext(photo.name)
        
        photo_name = f"{owner}_{pet}_{file_name}{file_extension}"
        photo_path = os.path.join(settings.MEDIA_ROOT, 'photos', photo_name)

        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)

        # 파일 저장
        with open(photo_path, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)
        
        # 가장 큰 seq 번호를 조회하여 다음 seq 번호 생성
        max_seq = SymptomDescription.objects.all().aggregate(models.Max('seq'))['seq__max'] or 0
        new_seq = max_seq + 1
        
        # SymptomDescription 모델에 데이터 저장
        symptom_description = SymptomDescription.objects.create(
            seq=new_seq,  # 생성한 seq 번호를 저장
            owner=owner,
            pet=pet,
            photo=photo_path
        )

        # AI 모델에 사진 경로를 전달하고 진단을 수행
        # 예시: AI 모델 호출 (여기서는 가상의 함수로 표시)
        # 모델 예측 수행
        try:
            prediction_results = run_diagnosis(photo_path, part)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 예측 결과 반환
        return Response({
            "message": "예측이 성공적으로 완료되었습니다.",
            "predictions": prediction_results
        }, status=status.HTTP_200_OK)

class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
