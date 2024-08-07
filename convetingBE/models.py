from django.db import models

class Pets(models.Model):
    owner = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=20, primary_key=True)
    
class Disease(models.Model):
    disease = models.CharField(max_length=255, primary_key=True)
    symptom = models.TextField(max_length=500)

class ResultAI(models.Model):
    seq = models.PositiveIntegerField(primary_key=True)
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
    

class Diagnosis(models.Model):
    owner = models.ForeignKey(Pets, on_delete=models.CASCADE, primary_key=True)
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE, primary_key=True)
    seq = models.ForeignKey(ResultAI, on_delete=models.CASCADE, primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    photo = models.CharField(max_length=255)

class Prediction(models.Model):
    seq = models.ForeignKey(ResultAI, on_delete=models.CASCADE, primary_key=True)
    disease = models.ForeignKey(Disease, on_delete=models.DO_NOTHING, primary_key=True)
