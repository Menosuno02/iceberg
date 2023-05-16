from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saves',
            field=models.ManyToManyField(related_name='blogsave', to=settings.AUTH_USER_MODEL),
        ),
    ]
