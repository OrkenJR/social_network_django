# Generated by Django 3.2.9 on 2021-11-09 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socnet', '0002_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='posts/default.jpg', upload_to='posts'),
        ),
    ]
