# Generated by Django 3.1.6 on 2021-03-18 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rydde_setninger', '0003_auto_20210317_1730'),
        ('sets', '0003_auto_20210317_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='sets',
            name='ryddeSetninger1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ryddeSetninger1', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AddField(
            model_name='sets',
            name='ryddeSetninger2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ryddeSetninger2', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AddField(
            model_name='sets',
            name='ryddeSetninger3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ryddeSetninger3', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AddField(
            model_name='sets',
            name='ryddeSetninger4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ryddeSetninger4', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AddField(
            model_name='sets',
            name='ryddeSetninger5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ryddeSetninger5', to='rydde_setninger.ryddesetninger'),
        ),
    ]
