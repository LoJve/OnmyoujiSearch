# Generated by Django 2.0.4 on 2018-04-16 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnmyojiSearch', '0003_auto_20180410_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonisterLevel',
            fields=[
                ('level', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rarity',
            fields=[
                ('rarity', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'rarity',
            },
        ),
    ]