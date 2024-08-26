from django.db import models

class SymptomDescription(models.Model):
    seq = models.PositiveIntegerField(primary_key=True, db_column='seq')
    owner = models.CharField(max_length=30)
    pet = models.CharField(max_length=20)
    part = models.CharField(max_length=20)
    photo = models.CharField(max_length=255)
    
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
    
    class Meta:
        db_table = 'prediction'
    
class Disease(models.Model):
    disease = models.CharField(max_length=255, primary_key=True, db_column='disease')
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
