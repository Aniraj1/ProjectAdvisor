# Generated by Django 4.2.2 on 2023-06-30 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expenses_Category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensescategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
