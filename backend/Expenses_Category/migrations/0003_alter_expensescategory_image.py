# Generated by Django 4.2.2 on 2023-07-04 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expenses_Category', '0002_expensescategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensescategory',
            name='image',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
