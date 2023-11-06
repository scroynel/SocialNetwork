# Generated by Django 4.2.5 on 2023-11-04 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('post_comment', 'Post comment'), ('rejected_friendrequest', 'Rejected friendrequest'), ('new_friendrequest', 'New friendrequest'), ('post_like', 'Post like'), ('accepted_friendrequest', 'Accepted friendrequest')], max_length=50),
        ),
    ]
