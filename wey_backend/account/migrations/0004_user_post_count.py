# Generated by Django 4.2.5 on 2023-10-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_friends_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
