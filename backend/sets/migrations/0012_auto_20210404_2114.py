# Generated by Django 3.1.6 on 2021-04-04 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0011_auto_20210404_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='owner',
            field=models.CharField(max_length=100),
        ),
    ]
