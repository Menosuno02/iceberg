from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('notification', '0001_initial'), ('notification', '0002_auto_20210201_1854'), ('notification', '0003_alter_notification_notification_type')]

    initial = True

    dependencies = [
        ('blog', '0003_auto_20210122_1426'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField(choices=[(1, 'Me gusta'), (2, 'Seguido'), (3, 'Comentario'), (4, 'Respuesta'), (5, 'Me gusta-Comentario'), (6, 'Me gusta-Respuesta')])),
                ('text_preview', models.CharField(blank=True, max_length=120)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notify_post', to='blog.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_from_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notify_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
