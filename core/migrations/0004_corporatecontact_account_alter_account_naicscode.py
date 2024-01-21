# Generated by Django 5.0.1 on 2024-01-19 22:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_epicsdkconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporatecontact',
            name='Account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='NAICSCode',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]