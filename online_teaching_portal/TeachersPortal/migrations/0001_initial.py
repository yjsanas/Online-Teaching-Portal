# Generated by Django 3.1.3 on 2020-11-24 15:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='assignment',
            fields=[
                ('Asid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('Atid', models.IntegerField()),
                ('Atitle', models.TextField()),
                ('Adec', models.TextField()),
                ('Amarked', models.TextField(default=None)),
                ('Atotalmark', models.TextField(default=None)),
                ('Aduedate', models.TextField(default=None)),
                ('Acreatedat', models.DateTimeField()),
                ('Aupdatedat', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='assignment_join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField()),
                ('Aid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='material',
            fields=[
                ('mid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('tid', models.IntegerField()),
                ('mtitle', models.TextField()),
                ('mdecription', models.TextField()),
                ('createdat', models.DateTimeField()),
                ('updatedat', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='material_join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField()),
                ('mid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='tcourse',
            fields=[
                ('cid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('tid', models.IntegerField()),
                ('cinfo', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacherlogin',
            fields=[
                ('Tid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]
