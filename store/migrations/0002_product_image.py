# Generated by Django 5.1 on 2024-10-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='static/images/'),
        ),
    ]
