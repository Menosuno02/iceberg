# Generated by Django 4.2 on 2023-05-31 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_squashed_0003_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'Me gusta'), (2, 'Seguido'), (3, 'Comentario'), (4, 'Respuesta')]),
        ),
    ]