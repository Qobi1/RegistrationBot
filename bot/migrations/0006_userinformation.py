# Generated by Django 4.0.6 on 2022-07-18 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_delete_userinformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('region', models.CharField(max_length=256, null=True)),
                ('full_name', models.CharField(max_length=256, null=True)),
                ('birthday', models.CharField(max_length=256, null=True)),
                ('location', models.CharField(max_length=256, null=True)),
                ('phone_number', models.CharField(max_length=256, null=True)),
                ('education', models.CharField(max_length=256, null=True)),
                ('project_name', models.CharField(max_length=256, null=True)),
                ('description', models.TextField(null=True)),
                ('file', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]