# Generated by Django 4.2.1 on 2023-06-05 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Expenses_Category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('amount', models.FloatField(blank=True, default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now=True)),
                ('exCategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Expenses_Category.expensescategory')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
