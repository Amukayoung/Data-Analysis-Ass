# Generated by Django 5.0.1 on 2024-01-14 23:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("danalysis", "0006_remove_organisation_sectorid_organisation_sectors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="sectorId",
            field=models.ForeignKey(
                max_length=255,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workers_sector",
                to="danalysis.sector",
            ),
        ),
    ]