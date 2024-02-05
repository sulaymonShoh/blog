# Generated by Django 5.0.1 on 2024-02-05 16:01

import blog.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user_photos/default/default.jpg', upload_to=blog.utils.avatar_path),
        ),
    ]