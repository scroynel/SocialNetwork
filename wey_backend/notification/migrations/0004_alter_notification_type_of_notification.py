# Generated by Django 4.2.5 on 2023-11-04 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_alter_notification_type_of_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('accepted_friendrequest', 'Accepted friendrequest'), ('post_comment', 'Post comment'), ('new_friendrequest', 'New friendrequest'), ('post_like', 'Post like'), ('rejected_friendrequest', 'Rejected friendrequest')], max_length=50),
        ),
    ]