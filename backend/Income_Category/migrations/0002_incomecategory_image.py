# Generated by Django 4.2.2 on 2023-06-30 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Income_Category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomecategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
