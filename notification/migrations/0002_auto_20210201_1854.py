from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'Like'), (2, 'Follow'), (3, 'Comment'), (4, 'Reply'), (5, 'Like-Comment'), (6, 'Like-Reply')]),
        ),
    ]
