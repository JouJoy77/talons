# Generated by Django 4.1.4 on 2023-02-15 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ticket',
            field=models.ManyToManyField(blank=True, to='users.tickets', verbose_name='Талоны'),
        ),
    ]
