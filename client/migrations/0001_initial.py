# Generated by Django 3.1.4 on 2021-05-03 18:21

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('channel_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('music', models.CharField(max_length=100000000)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('music_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='muisc_images')),
                ('singer', models.CharField(max_length=2000)),
                ('band', models.CharField(max_length=2000)),
                ('banner', models.ImageField(upload_to='music_banner')),
                ('music', models.FileField(upload_to='musics')),
                ('category', models.CharField(choices=[('pop', 'POP'), ('funk', 'FUNK'), ('classical', 'CLASSICAL'), ('rock', 'ROCK'), ('country', 'COUNTRY'), ('hiphop', 'HIPHOP'), ('jazz', 'JAZZ'), ('folk', 'FOLK'), ('rap', 'RAP'), ('metal', 'METAL')], max_length=10)),
                ('language', models.CharField(choices=[('english', 'ENGLISH'), ('nepali', 'NEPALI'), ('hindi', 'HINDI')], max_length=10)),
                ('status', models.CharField(choices=[('RA', 'RECENTLY ADDED'), ('MW', 'MOST WATCHED'), ('TR', 'TOP RATED')], max_length=2)),
                ('cast', models.CharField(max_length=100)),
                ('year_of_production', models.DateField()),
                ('views_count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=datetime.datetime(2021, 5, 4, 0, 6, 5, 886706))),
                ('updated', models.DateTimeField(default=datetime.datetime(2021, 5, 4, 0, 6, 5, 886706))),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='playlist_images')),
                ('playlistName', models.CharField(max_length=2000)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=250)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.music')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.music')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listenlater',
            fields=[
                ('listen_id', models.AutoField(primary_key=True, serialize=False)),
                ('video_id', models.CharField(max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('hist_id', models.AutoField(primary_key=True, serialize=False)),
                ('music_id', models.CharField(max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
