# Generated by Django 5.0.1 on 2024-01-13 21:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("danalysis", "0002_alter_organisation_id_alter_sector_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="osversion",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
