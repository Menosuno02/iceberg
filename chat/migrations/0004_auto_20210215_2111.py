from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_room_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
