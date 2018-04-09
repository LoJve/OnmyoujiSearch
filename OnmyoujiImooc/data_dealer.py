# _*_coding:utf-8_*_
import sqlite3

import os


class DataDealer(object):
    def __init__(self):
        self.database = "../db.sqllite3"
        self.new_datas = []

    # 式神基础信息处理
    def collect_data(self, new_data):
        if new_data is not None:
            self.new_datas.append(new_data)

    def deal_data_shikigami(self):
        if len(self.new_datas) > 0:
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
        dict_chapter = dict_chapter
        dict_chapter_monster = dict_chapter_monster
        dict_chapter_monster_detail = dict_chapter_monster_detail

        sql_chapter = """
            INSERT INTO chapter (chapter, title)
            VALUES  
        """
        sql_chapter_monster = """
            INSERT INTO chapter_monster (chapter, monster, difficulty, location, monster_type)
            VALUES  
        """
        sql_chapter_monster_detail = """
            INSERT INTO chapter_detail (chapter, location, monster, monster_cnt)
            VALUES  
        """

        for chapter in dict_chapter:
            sql_chapter += "(%d, '%s')," % (int(chapter["chapter"]), chapter["title"])

        for monster in dict_chapter_monster:
            sql_chapter_monster += "(%d, '%s', '%s', %d, '%s')," \
                  % (monster["chapter"], monster["monster"], monster["difficulty"], int(str(monster["location"])), monster["monster_type"])
        for detail in dict_chapter_monster_detail:
            sql_chapter_monster_detail += "(%d, %d, '%s', %d)," \
                  % (int(detail["chapter"]), int(detail["location"]), detail["monster"], int(detail["monster_cnt"]))
        sql_chapter = sql_chapter.rstrip(",")
        sql_chapter_monster = sql_chapter_monster.rstrip(",")
        sql_chapter_monster_detail = sql_chapter_monster_detail.rstrip(",")
        print(sql_chapter)
        self.execute_sql(self.database, sql_chapter)
        print(sql_chapter_monster)
        self.execute_sql(self.database, sql_chapter_monster)
        print(sql_chapter_monster_detail)
        self.execute_sql(self.database, sql_chapter_monster_detail)

    # 插入式神基础信息
    def insert_shikigami_data(self):
        if len(self.new_datas) > 0:
            sql = """
                      INSERT INTO shikigami (key, rarity, interactive, name, icon)
                      VALUES  
                  """

            for new_data in self.new_datas:
                sql += "('%s', %d, %d, '%s', '%s')," \
                       % (new_data["index"],int(new_data["rarity"]),int(new_data["interactive"]),new_data["name"],new_data["icon"])
            sql = sql.rstrip(',')

            self.execute_sql(self.database, sql)

    # 更新数据库表--新增
    def execute_sql(self, database, sql):
        if sql is not None:
            conn = sqlite3.connect(database)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()
