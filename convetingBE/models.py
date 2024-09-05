from django.db import models
from datetime import datetime
from zoneinfo import ZoneInfo
import os

def diag_img_upload(instance, filename):
    NOW_KST = datetime.now(ZoneInfo("Asia/Seoul"))
    
    _, file_extension = os.path.splitext(filename)
    timestamp = NOW_KST.strftime("%Y%m%d_%H%M%S")
    
    owner = instance.owner
    pet = instance.pet
    part = instance.part
    
    photo_name = f"{timestamp}_{owner}_{pet}_{part}{file_extension}"

    # 파일을 저장할 경로 지정
    return os.path.join('photos/', photo_name)

class SymptomDescription(models.Model):
    seq = models.PositiveIntegerField(primary_key=True, db_column='seq')
    owner = models.CharField(max_length=30)
    pet = models.CharField(max_length=20)
    part = models.CharField(max_length=20)
    photo = models.ImageField(upload_to=diag_img_upload)
    
    class Meta:
        db_table = 'symptomdescription'

class Prediction(models.Model):
    seq = models.OneToOneField(SymptomDescription, on_delete=models.CASCADE, primary_key=True, db_column='seq')
    skin1 = models.DecimalField(max_digits=5, decimal_places=2)
    skin2 = models.DecimalField(max_digits=5, decimal_places=2)
    skin3 = models.DecimalField(max_digits=5, decimal_places=2)
    skin4 = models.DecimalField(max_digits=5, decimal_places=2)
    skin5 = models.DecimalField(max_digits=5, decimal_places=2)
    skin6 = models.DecimalField(max_digits=5, decimal_places=2)
    eye1 = models.DecimalField(max_digits=5, decimal_places=2)
    eye2 = models.DecimalField(max_digits=5, decimal_places=2)
    eye3 = models.DecimalField(max_digits=5, decimal_places=2)
    eye4 = models.DecimalField(max_digits=5, decimal_places=2)
    eye5 = models.DecimalField(max_digits=5, decimal_places=2)
    eye6 = models.DecimalField(max_digits=5, decimal_places=2)
    eye7 = models.DecimalField(max_digits=5, decimal_places=2)
    eye8 = models.DecimalField(max_digits=5, decimal_places=2)
    eye9 = models.DecimalField(max_digits=5, decimal_places=2)
    eye10 = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = 'prediction'
    
class Disease(models.Model):
    code = models.CharField(max_length=10, primary_key=True, db_column='code')
    name = models.CharField(max_length=255, db_column='name')
    symptom = models.TextField(max_length=500)
    cure = models.TextField(max_length=500, default='Nothing')
    
    class Meta:
        db_table = 'disease'

class Diagnosis(models.Model):
    seq = models.ForeignKey(SymptomDescription, on_delete=models.CASCADE, db_column='seq')
    disease = models.ForeignKey(Disease, on_delete=models.DO_NOTHING, db_column='disease')

    class Meta:
        db_table = 'diagnosis'
        unique_together = ('seq', 'disease')
