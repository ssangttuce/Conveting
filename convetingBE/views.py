import os
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import models
from .models import Prediction, Diagnosis, Disease, SymptomDescription
from .serializers import SymptomDescriptionSerializer, DiseaseSerializer, DiagnosisSerializer
from .utils import run_diagnosis  # 예측 함수를 임포트

class DiagnosisHistoryView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            # SymptomDescription 테이블에서 해당 user_id(owner)로 필터링
            symptoms = SymptomDescription.objects.filter(owner=user_id)
            
            if not symptoms.exists():
                return Response({"error": "No history found for this user."}, status=status.HTTP_404_NOT_FOUND)
            
            # 진단 내역을 담을 리스트
            response_data = []

            for symptom in symptoms:
                # SymptomDescription의 seq를 이용하여 Diagnosis 테이블에서 해당 진단 내역 조회
                diagnosis_list = Diagnosis.objects.filter(seq=symptom)

                # 해당 진단에 대해 직렬화 및 추가 정보 구성
                for diagnosis in diagnosis_list:
                    disease_instance = diagnosis.disease
                    
                    # Disease 테이블에서 symptom과 cure를 가져와서 응답 데이터에 추가
                    response_data.append({
                        "disease": disease_instance.disease,
                        "symptom": disease_instance.symptom,
                        "cure": disease_instance.cure,
                        "photo": symptom.photo,  # 각 진단 내역에 대해 사진 경로도 추가
                        "part": symptom.part,  # 각 진단 내역에 대해 부위도 추가
                        "pet": symptom.pet,
                        "seq": symptom.seq
                    })
            
            # 결과 반환
            return Response(response_data, status=status.HTTP_200_OK)
        
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
            part=part,
            photo=photo_path
        )

        # AI 모델에 사진 경로를 전달하고 진단을 수행
        # 예시: AI 모델 호출 (여기서는 가상의 함수로 표시)
        # 모델 예측 수행
        try:
            prediction_results = run_diagnosis(photo_path, part)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Prediction 모델에 예측 결과 저장
        prediction = Prediction.objects.create(
            seq=symptom_description,
            skin1=prediction_results.get('구진, 플라크', 0),
            skin2=prediction_results.get('비듬, 각질, 상피성잔고리', 0),
            skin3=prediction_results.get('태선화, 과다색소침착', 0),
            skin4=prediction_results.get('농포, 여드름', 0),
            skin5=prediction_results.get('미란, 궤양', 0),
            skin6=prediction_results.get('결절, 종괴', 0),
            eye1=prediction_results.get('결막염', 0),
            eye2=prediction_results.get('궤양성 각막질환', 0),
            eye3=prediction_results.get('백내장', 0),
            eye4=prediction_results.get('비궤양성 각막질환', 0),
            eye5=prediction_results.get('색소침착성각막염', 0),
            eye6=prediction_results.get('안검 내반증', 0),
            eye7=prediction_results.get('안검종양', 0),
            eye8=prediction_results.get('유루증', 0),
        )
        # 상위 2개의 확률이 높은 질환을 선택
        top_diseases = sorted(prediction_results.items(), key=lambda x: x[1], reverse=True)[:2]

        # 30% 이상 확률의 질환을 Diagnosis 테이블에 저장하고, 상위 2개의 질환을 반환
        response_data = []
        for disease, probability in top_diseases:
            if probability > 0:  # 확률이 0% 이상인 경우에만 처리
                disease_instance, _ = Disease.objects.get_or_create(disease=disease)
                Diagnosis.objects.create(seq=symptom_description, disease=disease_instance)
                response_data.append({
                    "disease": disease_instance.disease,
                    "symptom": disease_instance.symptom,
                    "cure": disease_instance.cure,
                    "probability": probability  # 확률 추가
                })

        return Response({
            "message": "예측이 성공적으로 완료되었고 결과가 저장되었습니다.",
            "predictions": prediction_results,
            "diagnoses": response_data  # 상위 2개의 질환과 확률 정보 포함
        }, status=status.HTTP_200_OK)


class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
