from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
