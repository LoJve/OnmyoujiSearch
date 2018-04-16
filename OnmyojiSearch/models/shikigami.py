# _*_coding:utf-8_*_
from django.db import models


class Monster(models.Model):
    index = models.CharField(max_length=5)
    rarity = models.IntegerField()
    interactive = models.IntegerField()
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "monster"


class Chapter(models.Model):
    chapter = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "chapter"


class ChapterMonster(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10)
    location = models.IntegerField()
    genre = models.CharField(max_length=20)

    class Meta:
        db_table = "chapter_monster"


class ChapterMonsterDetail(models.Model):
    chapter_monster = models.ForeignKey(ChapterMonster, on_delete=models.CASCADE)
    monster = models.CharField(max_length=20)
    cnt = models.IntegerField()

    class Meta:
        db_table = "chapter_detail"


class Rarity(models.Model):
    rarity = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=10)

    class Meta:
        db_table = "rarity"
