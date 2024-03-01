# Generated by Django 4.2.6 on 2023-11-10 22:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_serviceimg_ticketimg_vehicle_rename_users_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empID', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopName', models.CharField(max_length=100)),
                ('date', models.DateField(verbose_name='Expense Date')),
                ('repairType', models.CharField(max_length=100)),
                ('amountCharged', models.DecimalField(decimal_places=2, max_digits=15)),
                ('LicensePlate', models.CharField(max_length=6)),
                ('receipt', models.ImageField(upload_to='media/images/service')),
            ],
        ),
        migrations.CreateModel(
            name='LicensePlate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plateID', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticketType', models.CharField(max_length=100)),
                ('ticketAmt', models.CharField(max_length=100)),
                ('date', models.DateField(verbose_name='Ticket Date')),
                ('LicensePlate', models.CharField(max_length=6)),
                ('assignedEmployee', models.CharField(max_length=100)),
                ('ticket', models.ImageField(blank=True, null=True, upload_to='images/ticket')),
            ],
        ),
        migrations.DeleteModel(
            name='serviceImg',
        ),
        migrations.DeleteModel(
            name='ticketImg',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='licensePlate',
        ),
        migrations.AddField(
            model_name='user',
            name='ticket',
            field=models.ImageField(blank=True, null=True, upload_to='images/ticket'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='receipt',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='media/images/service'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='active',
            field=models.CharField(max_length=10),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='LicensePlate',
            field=models.CharField(default=django.utils.timezone.now, max_length=6),
            preserve_default=False,
        ),
    ]