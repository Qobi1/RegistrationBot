# Generated by Django 4.0.6 on 2022-07-18 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_userinformation_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
