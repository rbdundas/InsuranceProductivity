# Generated by Django 5.0.1 on 2024-05-28 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amsforms', '0002_alter_jotformparameters_formid'),
    ]

    operations = [
        migrations.AddField(
            model_name='amsobjecttype',
            name='AMSObjectType',
            field=models.CharField(choices=[('Activity', 'Activity'), ('Client', 'Client')], default='Activity', max_length=255),
            preserve_default=False,
        ),
    ]