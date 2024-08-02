from django.db import models

class Pets(models.Model):
    owner = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=15, primary_key=True)
    
class Disease(models.Model):
    disease = models.CharField(max_length=255, primary_key=True)
    symptom = models.TextField(max_length=500)

class ResultAI(models.Model):
    seq = models.PositiveIntegerField(primary_key=True)
    predicted_disease1 = models.DecimalField(max_digits=5, decimal_places=2)
    predicted_disease2 = models.DecimalField(max_digits=5, decimal_places=2)
    predicted_disease3 = models.DecimalField(max_digits=5, decimal_places=2)

class Diagnosis(models.Model):
    owner = models.ForeignKey(Pets, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    seq = models.ForeignKey(ResultAI, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    photo = models.CharField(max_length=255)

class Prediction(models.Model):
    seq = models.ForeignKey(ResultAI, on_delete=models.CASCADE, primary_key=True)
    disease = models.ForeignKey(Disease, on_delete=models.DO_NOTHING, primary_key=True)
