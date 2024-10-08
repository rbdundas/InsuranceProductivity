# Generated by Django 5.0.1 on 2024-06-30 01:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=240)),
                ('Description', models.CharField(max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name='CarrierInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=240)),
                ('NAIC', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LinesOfBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=240, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acord.addresstype')),
            ],
        ),
        migrations.CreateModel(
            name='AgencyInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=240)),
                ('ContactName', models.CharField(max_length=120)),
                ('ContactPhone', models.CharField(max_length=30)),
                ('ContactEmail', models.CharField(max_length=240)),
                ('Code', models.CharField(blank=True, max_length=4, null=True)),
                ('SubCode', models.CharField(blank=True, max_length=4, null=True)),
                ('Address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acord.address')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('PolicyNumber', models.CharField(blank=True, max_length=60, null=True)),
                ('Underwriter', models.CharField(blank=True, max_length=60, null=True)),
                ('UnderwriterOffice', models.CharField(blank=True, max_length=60, null=True)),
                ('AgencyCustomerID', models.CharField(blank=True, max_length=60, null=True)),
                ('BindTimestamp', models.DateTimeField(blank=True, null=True)),
                ('AgencyInformation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acord.agencyinformation')),
                ('Attachments', models.ManyToManyField(blank=True, null=True, to='acord.attachment')),
                ('CarrierInformation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acord.carrierinformation')),
                ('LinesOfBusiness', models.ManyToManyField(blank=True, null=True, to='acord.linesofbusiness')),
                ('TransactionStatus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='acord.transactionstatus')),
            ],
        ),
    ]
