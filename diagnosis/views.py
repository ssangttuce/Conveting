import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.db import models
from .models import Prediction, Diagnosis, Disease, SymptomDescription
from .serializers import SymptomDescriptionSerializer, DiagnosisSerializer
from .utils import run_diagnosis  # 예측 함수를 임포트
from django.shortcuts import render
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = os.path.join(BASE_DIR, 'templates')
DIAGNOSIS_DIR = os.path.join(TEMPLATE_ROOT, 'diagnosis')

def home(request):
    return render(request, os.path.join(TEMPLATE_ROOT, 'home.html'))

class DiagnosisHistoryView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            symptoms = SymptomDescription.objects.filter(owner=user_id)
            
            if not symptoms.exists():
                return Response({"error": "No history found for this user."}, status=status.HTTP_404_NOT_FOUND)

            response_data = []
            for symptom in symptoms:
                diagnosis_list = Diagnosis.objects.filter(seq=symptom)
                response_data.append({
                    "symptom": SymptomDescriptionSerializer(symptom).data,
                    "diagnoses": DiagnosisSerializer(diagnosis_list, many=True).data
                })
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except SymptomDescription.DoesNotExist:
            return Response({"error": f"No history found for '{user_id}'."}, status=status.HTTP_404_NOT_FOUND)

class DiagnosisView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=os.path.join(DIAGNOSIS_DIR, 'submittal.html'))
        # return Response("result", status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # 요청 데이터에서 owner, pet, photo 정보 가져오기
        owner = request.data.get('owner')
        pet = request.data.get('pet')
        photo = request.FILES.get('photo')  # 파일은 FILES에서 가져옵니다
        part = request.data.get('part')  # 진단 부위 ('eye' 또는 'skin')

        if not owner or not pet or not photo:
            return Response({"error": "owner, pet, and photo are required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 가장 큰 seq 번호를 조회하여 다음 seq 번호 생성
        max_seq = SymptomDescription.objects.all().aggregate(models.Max('seq'))['seq__max'] or 0
        new_seq = max_seq + 1
        
        # SymptomDescription 모델에 데이터 저장
        symptom_description = SymptomDescription.objects.create(
            seq=new_seq,
            owner=owner,
            pet=pet,
            part=part,
            photo=photo
        )
        
        photo_path = os.path.join(BASE_DIR, symptom_description.photo.path)
        
        # 모델 예측 수행
        try:
            prediction_results = run_diagnosis(photo_path, part)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Prediction 모델에 예측 결과 저장
        Prediction.objects.create(
            seq=symptom_description,
            skin1=prediction_results.get('s1', 0),
            skin2=prediction_results.get('s2', 0),
            skin3=prediction_results.get('s3', 0),
            skin4=prediction_results.get('s4', 0),
            skin5=prediction_results.get('s5', 0),
            skin6=prediction_results.get('s6', 0),
            eye1=prediction_results.get('e1', 0),
            eye2=prediction_results.get('e2', 0),
            eye3=prediction_results.get('e3', 0),
            eye4=prediction_results.get('e4', 0),
            eye5=prediction_results.get('e5', 0),
            eye6=prediction_results.get('e6', 0),
            eye7=prediction_results.get('e7', 0),
            eye8=prediction_results.get('e8', 0),
            eye9=prediction_results.get('e9', 0),
            eye10=prediction_results.get('e10', 0)
        )
        
        # 상위 2개의 확률이 높은 질환을 선택
        top_diseases = sorted(prediction_results.items(), key=lambda x: x[1], reverse=True)[:2]

        # 상위 2개의 질환을 반환
        response_data = []
        for disease, probability in top_diseases:
            disease_instance, _ = Disease.objects.get_or_create(code=disease) # 인스턴스, 새로 생성 여부
            Diagnosis.objects.create(seq=symptom_description, disease=disease_instance)
            response_data.append({
                "disease": disease_instance.name,
                "symptom": disease_instance.symptom,
                "cure": disease_instance.cure,
                "probability": probability
            })

        context = {
            "results": response_data,
            "photo": symptom_description.photo.url
        }
        return render(request=request, template_name=os.path.join(DIAGNOSIS_DIR, 'result.html'), context=context)
