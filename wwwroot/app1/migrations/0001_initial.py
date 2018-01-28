# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-28 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cameras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('key', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('board', models.CharField(default='Tegra X1', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastCaptureFile', models.ImageField(upload_to='camera_images/')),
                ('lastCaptureTime', models.TimeField(auto_now=True)),
                ('jsonresult', models.TextField(default='{}')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Cameras')),
            ],
        ),
    ]
