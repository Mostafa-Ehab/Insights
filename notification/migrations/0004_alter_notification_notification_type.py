# Generated by Django 5.0.7 on 2024-08-02 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_remove_notification_is_opened'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Blog', 'Blog'), ('Follow', 'Follow'), ('Like', 'Like'), ('Comment', 'Comment'), ('Reply', 'Reply')], max_length=20),
        ),
    ]
