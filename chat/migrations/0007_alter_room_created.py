from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_squashed_0006_auto_20210215_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
