# Generated by Django 4.2.5 on 2023-10-21 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_post_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='post_count',
            new_name='posts_count',
        ),
    ]