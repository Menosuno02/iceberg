# Generated by Django 4.2 on 2023-06-09 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_profile_search_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='orientation',
            field=models.CharField(blank=True, choices=[('Heterosexual', 'Heterosexual'), ('Homosexual', 'Homosexual'), ('Bisexual', 'Bisexual'), ('Pansexual', 'Pansexual'), ('Asexual', 'Asexual'), ('Otra', 'Otra')], max_length=12),
        ),
    ]