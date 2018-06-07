# Generated by Django 2.0.5 on 2018-06-07 21:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_privilegeduserprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enduserprofile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='enduserprofile',
            name='phone_number',
            field=models.CharField(
                blank=True,
                default='+99999999',
                max_length=16,
                validators=[
                    django.core.validators.RegexValidator(
                        '^\\+\\d{8,15}$',
                        message='Use the format +99999999. From 8 to 15 '
                                'digits allowed'
                    )
                ]
            ),
        )
    ]
