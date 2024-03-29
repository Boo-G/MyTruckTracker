# Generated by Django 4.2.6 on 2023-10-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='serviceImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('img', models.ImageField(default=None, upload_to='media/images/service')),
            ],
        ),
        migrations.CreateModel(
            name='ticketImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('img', models.ImageField(default=None, upload_to='media/images/ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignedEmployee', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
                ('licensePlate', models.CharField(max_length=10)),
                ('VIN', models.CharField(max_length=20)),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('kms', models.CharField(max_length=100)),
                ('currentTrip', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
        migrations.DeleteModel(
            name='TodoItem',
        ),
    ]
