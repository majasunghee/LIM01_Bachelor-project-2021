# Generated by Django 3.1.6 on 2021-03-26 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forstaelse', '0002_auto_20210226_1657'),
        ('chat', '0002_auto_20210308_1607'),
        ('rydde_setninger', '0003_auto_20210317_1730'),
        ('sets', '0005_sets_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sets',
            name='chat1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat1', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='chat2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat2', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='chat3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat3', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='chat4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat4', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='chat5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat5', to='chat.chat'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='forstaelse1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forstaelse1', to='forstaelse.forstaelse'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='forstaelse2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forstaelse2', to='forstaelse.forstaelse'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='forstaelse3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forstaelse3', to='forstaelse.forstaelse'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='forstaelse4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forstaelse4', to='forstaelse.forstaelse'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='forstaelse5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forstaelse5', to='forstaelse.forstaelse'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='ryddeSetninger1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ryddeSetninger1', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='ryddeSetninger2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ryddeSetninger2', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='ryddeSetninger3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ryddeSetninger3', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='ryddeSetninger4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ryddeSetninger4', to='rydde_setninger.ryddesetninger'),
        ),
        migrations.AlterField(
            model_name='sets',
            name='ryddeSetninger5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ryddeSetninger5', to='rydde_setninger.ryddesetninger'),
        ),
    ]
