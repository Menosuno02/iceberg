# Generated by Django 3.1.4 on 2021-01-20 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorites', to='blog.Post'),
        ),
    ]
