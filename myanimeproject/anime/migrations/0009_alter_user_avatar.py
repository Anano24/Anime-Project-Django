# Generated by Django 5.0.6 on 2024-07-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0008_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='blank-profile-picture-973460_1280.png', null=True, upload_to='profile_img/'),
        ),
    ]
