# Generated by Django 5.0 on 2025-01-17 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letstalkapp', '0005_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_image/profile.png', null=True, upload_to='profile_image'),
        ),
    ]
