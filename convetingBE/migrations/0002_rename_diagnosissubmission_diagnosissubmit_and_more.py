# Generated by Django 4.2.14 on 2024-08-02 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convetingBE', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DiagnosisSubmission',
            new_name='DiagnosisSubmit',
        ),
        migrations.RenameField(
            model_name='diagnosisresult',
            old_name='submission',
            new_name='submit',
        ),
        migrations.RenameField(
            model_name='diagnosissubmit',
            old_name='submission_date',
            new_name='submit_date',
        ),
    ]
