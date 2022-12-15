# Generated by Django 4.1.4 on 2022-12-15 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('No role', 'None'), ('Administrator', 'Admin'), ('Manager', 'Manager'), ('Shop assistant', 'Seller'), ('Support assistant', 'Support')], default='No role', max_length=50),
        ),
    ]
