# Generated by Django 4.2.6 on 2023-11-25 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_trips_vehicle_currenttrip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licensePlate', models.CharField(max_length=6)),
                ('tripType', models.CharField(choices=[('IN', 'check_in'), ('OUT', 'check_out')], default='OUT', max_length=3, null=True)),
                ('location', models.CharField(max_length=32)),
                ('checkout', models.DateTimeField(db_comment='Date and time when the Vehicle was checked out', null=True)),
                ('checkin', models.DateTimeField(db_comment='Date and time when the Vehicle was checked in', null=True)),
                ('user', models.CharField(max_length=6, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='currentTrip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='website.trip'),
        ),
        migrations.DeleteModel(
            name='Trips',
        ),
    ]
