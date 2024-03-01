# Generated by Django 4.2.6 on 2023-11-25 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_remove_licenseplate_plate_alter_licenseplate_plateid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='currentTrip',
        ),
        migrations.AlterField(
            model_name='expense',
            name='LicensePlate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='website.licenseplate'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='LicensePlate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='website.licenseplate'),
        ),
    ]
