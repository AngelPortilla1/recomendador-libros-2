# Generated by Django 5.1.3 on 2024-11-19 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_libros', '0002_usuario_recomendacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
