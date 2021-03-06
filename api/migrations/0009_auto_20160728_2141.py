# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 21:41
from __future__ import unicode_literals

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20160721_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('chosen', models.BooleanField(default=False)),
                ('color', models.CharField(choices=[('red', 'red'), ('blue', 'blue'), ('grey', 'grey'), ('black', 'black')], default='grey', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Clue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('word', models.CharField(max_length=96)),
                ('number', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('unique_id', models.CharField(default=api.models._create_hash, max_length=10, unique=True)),
                ('current_turn', models.CharField(choices=[('blue_give', 'Blue Team to give clue'), ('blue_guess', 'Blue Team to guess'), ('red_give', 'Red Team to give clue'), ('red_guess', 'Red Team to guess')], default='red_give', max_length=16)),
                ('current_guess_number', models.IntegerField(default=0)),
                ('red_remaining', models.IntegerField(default=9)),
                ('blue_remaining', models.IntegerField(default=9)),
                ('started_date', models.DateTimeField(auto_now_add=True, verbose_name='date started')),
                ('active', models.BooleanField(default=True)),
                ('winning_team', models.CharField(choices=[('red', 'red'), ('blue', 'blue')], max_length=5, null=True)),
                ('blue_giver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blue_giver', to=settings.AUTH_USER_MODEL)),
                ('blue_guesser', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blue_guesser', to=settings.AUTH_USER_MODEL)),
                ('red_giver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='red_giver', to=settings.AUTH_USER_MODEL)),
                ('red_guesser', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='red_guesser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('guesser_team', models.CharField(choices=[('red', 'red'), ('blue', 'blue')], default='red', max_length=5)),
                ('card', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Card')),
                ('game', models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='alternate', max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='friend',
            name='source_user',
        ),
        migrations.RemoveField(
            model_name='showdown',
            name='loser',
        ),
        migrations.RemoveField(
            model_name='showdown',
            name='question',
        ),
        migrations.RemoveField(
            model_name='showdown',
            name='rater',
        ),
        migrations.RemoveField(
            model_name='showdown',
            name='winner',
        ),
        migrations.DeleteModel(
            name='Candidate',
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Showdown',
        ),
        migrations.AddField(
            model_name='word',
            name='word_set',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.WordSet'),
        ),
        migrations.AddField(
            model_name='game',
            name='word_set',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.WordSet'),
        ),
        migrations.AddField(
            model_name='clue',
            name='game',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
        migrations.AddField(
            model_name='clue',
            name='giver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='game',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
        migrations.AddField(
            model_name='card',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Word'),
        ),
    ]
