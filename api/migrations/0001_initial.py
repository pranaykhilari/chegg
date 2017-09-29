# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-24 09:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chegg_uuid', models.CharField(db_index=True, max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('dummy_email', models.EmailField(max_length=254)),
                ('source', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAvailabilityFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filters', django.contrib.postgres.fields.jsonb.JSONField()),
                ('graph', models.CharField(max_length=255)),
                ('future', models.CharField(max_length=255)),
                ('length', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='api.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_id', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to='api.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserCalendarBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='api.User')),
            ],
        ),
    ]
