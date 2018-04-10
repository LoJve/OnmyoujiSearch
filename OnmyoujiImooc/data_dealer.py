# _*_coding:utf-8_*_
import sqlite3

import os

from django.shortcuts import get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnmyojiSearch.settings")
import django
django.setup()

from OnmyojiSearch.models import *


class DataDealer(object):
    def __init__(self):
        self.database = "../db.sqllite3"
        self.new_datas = []

    # 式神基础信息处理
    def collect_data(self, new_data):
        if new_data is not None and new_data not in self.new_datas:
            self.new_datas.append(new_data)

    def deal_data_shikigami(self):
        self.insert_shikigami_data()

    # 式神图片下载
    def download_pic(self, response, path, filename):
        if not os.path.exists(path):
            os.makedirs(path)
        if not path.endswith("/"):
            path = path + "/"
        file = open(path + filename, "wb")
        file.write(response)
        file.flush()
        file.close()

    # 章节怪物信息处理
    def save_chapter_data(self, dict_chapter, dict_chapter_monster, dict_chapter_monster_detail):
        chapters = []
        chapter_monsters = []
        chapter_details = []
        if dict_chapter is not None and len(dict_chapter) > 0:
            for dict in dict_chapter:
                chapter = Chapter(chapter=int(dict["chapter"]), title=dict["title"])
                chapters.append(chapter)
        Chapter.objects.bulk_create(chapters)

        if dict_chapter_monster is not None and len(dict_chapter_monster) > 0:
            for dict in dict_chapter_monster:
                try:
                    chapter = get_object_or_404(Chapter,chapter=dict["chapter"])
                    monster = get_object_or_404(Monster,name=dict["monster"])
                except Exception as e:
                    print(dict)
                chapter_monster = ChapterMonster(chapter=chapter, monster=monster,difficulty=dict["difficulty"],
                                                 location=int(str(dict["location"])), genre=dict["monster_type"])
                if chapter_monster not in chapter_monsters:
                    chapter_monsters.append(chapter_monster)
            ChapterMonster.objects.bulk_create(chapter_monsters)

        if dict_chapter_monster_detail is not None and len(dict_chapter_monster_detail) > 0:
            for dict in dict_chapter_monster_detail:
                try:
                    # monster = get_object_or_404(Monster, name=dict["monster"])
                    chapster_monster = get_object_or_404(ChapterMonster, chapter=dict["chapter"],
                                                         difficulty=dict["difficulty"], location=int(dict["location"]))

                    chapter_detail = ChapterMonsterDetail(chapter_monster=chapster_monster, monster=dict["monster"],
                                                          cnt=int(dict["monster_cnt"]))
                    if chapter_detail not in chapter_details:
                        chapter_details.append(chapter_detail)
                except Exception as e:
                    print(dict)
                    print(e)
                    return


        ChapterMonsterDetail.objects.bulk_create(chapter_details)

    # 插入式神基础信息
    def insert_shikigami_data(self):
        if len(self.new_datas) > 0:
            monsters = []
            for new_data in self.new_datas:
                monster = Monster(index=new_data["index"],rarity=int(new_data["rarity"]),
                                  interactive=int(new_data["interactive"]),name=new_data["name"],icon=new_data["icon"])
                monsters.append(monster)
            Monster.objects.bulk_create(monsters)



