# Generated by Django 4.2.17 on 2025-03-03 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0001_initial'),
        ('hashtags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platforms.platform'),
        ),
    ]
