# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 00:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_candidate_question_rater_showdown'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rater',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wolfpage',
            name='site',
        ),
        migrations.RenameField(
            model_name='candidate',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='showdown',
            name='description',
        ),
        migrations.RemoveField(
            model_name='showdown',
            name='title',
        ),
        migrations.AddField(
            model_name='showdown',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='showdown',
            name='loser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='loses', to='api.Candidate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='showdown',
            name='rater',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='showdowns', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='showdown',
            name='winner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='api.Candidate'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Rater',
        ),
        migrations.DeleteModel(
            name='WolfPage',
        ),
    ]
