# Generated by Django 2.0.4 on 2018-04-09 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapter', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'chapter',
            },
        ),
        migrations.CreateModel(
            name='ChapterMonster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(max_length=10)),
                ('location', models.IntegerField()),
                ('genre', models.CharField(max_length=20)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnmyojiSearch.Chapter')),
            ],
            options={
                'db_table': 'chapter_monster',
            },
        ),
        migrations.CreateModel(
            name='ChapterMonsterDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt', models.IntegerField()),
                ('chapter_monster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnmyojiSearch.ChapterMonster')),
            ],
            options={
                'db_table': 'chapter_detail',
            },
        ),
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=5)),
                ('rarity', models.IntegerField()),
                ('interactive', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('icon', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'monster',
            },
        ),
        migrations.AddField(
            model_name='chaptermonsterdetail',
            name='monster',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='OnmyojiSearch.Monster'),
        ),
        migrations.AddField(
            model_name='chaptermonster',
            name='monster',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='OnmyojiSearch.Monster'),
        ),
    ]