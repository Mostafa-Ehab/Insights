# Generated by Django 5.0.7 on 2024-08-02 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField()),
                ('text', models.CharField(max_length=150)),
                ('is_seen', models.BooleanField(default=False)),
                ('is_opened', models.BooleanField(default=False)),
                ('notification_type', models.CharField(choices=[('Blog', 'Blog'), ('Follow', 'Follow'), ('Like', 'Like')], max_length=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
