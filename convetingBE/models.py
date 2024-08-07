from django.db import models

class SymptomDescription(models.Model):
    seq = models.PositiveIntegerField()
    owner = models.CharField(max_length=30)
    pet = models.CharField(max_length=20)
    photo = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('seq', 'owner', 'pet')

class Prediction(models.Model):
    seq = models.ForeignKey(SymptomDescription, on_delete=models.CASCADE)
    skin1 = models.DecimalField(max_digits=5, decimal_places=2)
    skin2 = models.DecimalField(max_digits=5, decimal_places=2)
    skin3 = models.DecimalField(max_digits=5, decimal_places=2)
    skin4 = models.DecimalField(max_digits=5, decimal_places=2)
    skin5 = models.DecimalField(max_digits=5, decimal_places=2)
    skin6 = models.DecimalField(max_digits=5, decimal_places=2)
    skin7 = models.DecimalField(max_digits=5, decimal_places=2)
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
    eye11 = models.DecimalField(max_digits=5, decimal_places=2)
    
class Disease(models.Model):
    disease = models.CharField(max_length=255, primary_key=True)
    symptom = models.TextField(max_length=500)

class Diagnosis(models.Model):
    seq = models.ForeignKey(SymptomDescription, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.DO_NOTHING)
    
    class Meta:
        unique_together = ('seq', 'disease')
