# Generated by Django 5.1.1 on 2024-09-11 04:36

import diagnosis.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('code', models.CharField(db_column='code', max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=255)),
                ('symptom', models.TextField(max_length=500)),
                ('cure', models.TextField(default='Nothing', max_length=500)),
            ],
            options={
                'db_table': 'disease',
            },
        ),
        migrations.CreateModel(
            name='SymptomDescription',
            fields=[
                ('seq', models.PositiveIntegerField(db_column='seq', primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=30)),
                ('pet', models.CharField(max_length=20)),
                ('part', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to=diagnosis.models.diag_img_upload)),
            ],
            options={
                'db_table': 'symptomdescription',
            },
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('seq', models.OneToOneField(db_column='seq', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='diagnosis.symptomdescription')),
                ('skin1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('skin2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('skin3', models.DecimalField(decimal_places=2, max_digits=5)),
                ('skin4', models.DecimalField(decimal_places=2, max_digits=5)),
                ('skin5', models.DecimalField(decimal_places=2, max_digits=5)),
                ('skin6', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye3', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye4', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye5', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye6', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye7', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye8', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye9', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eye10', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'prediction',
            },
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.ForeignKey(db_column='disease', on_delete=django.db.models.deletion.DO_NOTHING, to='diagnosis.disease')),
                ('seq', models.ForeignKey(db_column='seq', on_delete=django.db.models.deletion.CASCADE, to='diagnosis.symptomdescription')),
            ],
            options={
                'db_table': 'diagnosis',
                'unique_together': {('seq', 'disease')},
            },
        ),
    ]
