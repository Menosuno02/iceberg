# Generated by Django 4.2 on 2023-06-09 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_profile_search_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='search_options',
            field=models.CharField(blank=True, default='Intereses', max_length=20, null=True),
        ),
    ]
