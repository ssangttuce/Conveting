from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.FloatField()
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    neutered = models.BooleanField(default=False)
    allergies = models.CharField(max_length=255, blank=True, null=True)

class DiagnosisSubmission(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    diagnosis_area = models.CharField(max_length=50, choices=[('eye', 'Eye'), ('skin', 'Skin')])
    photo = models.ImageField(upload_to='diagnosis_photos/')
    submission_date = models.DateTimeField(auto_now_add=True)

class DiagnosisResult(models.Model):
    submission = models.OneToOneField(DiagnosisSubmission, on_delete=models.CASCADE)
    predicted_disease = models.CharField(max_length=100)
    description = models.TextField()
    result_date = models.DateTimeField(auto_now_add=True)
