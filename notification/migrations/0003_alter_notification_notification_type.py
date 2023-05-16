from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20210201_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'Me gusta'), (2, 'Seguido'), (3, 'Comentario'), (4, 'Respuesta'), (5, 'Me gusta-Comentario'), (6, 'Me gusta-Respuesta')]),
        ),
    ]
