# _*_coding:utf-8_*_
import json
import re

from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self):
        self.dict_data = []
        self.dict_chapter = []
        self.dict_chapter_monster = []
        self.dict_chapter_monster_detail = []
        self.dict_boss = {"1": "九命猫", "2": "座敷童子", "3": "凤凰火", "4": "雨女", "5": "食发鬼",
                          "6": "巫蛊师", "7": "妖狐", "8": "桃花妖", "9": "孟婆", "10": "酒吞童子",
                          "11": "鬼女红叶", "12": "雪女", "13": "首无", "14": "食梦貘",
                          "15": "跳跳妹妹", "16": "判官", "17": "荒川之主", "18": "大天狗"}

    # 式神基础信息解析
    def parser_shikigami(self, response):
        json_str = re.compile(r'{.*}')
        json_str = json_str.search(response).group()
        json_dict = json.loads(json_str)
        shikigami_dict = json_dict["data"]
        for key in shikigami_dict:
            dict_value = shikigami_dict[key]
            if isinstance(dict_value, dict):
                dict_value["index"] = key
                self.dict_data.append(dict_value)
        return self.dict_data

    def parser_shikigami_dict(self, shikigami_dict, key):
        dict_value = shikigami_dict[key]
        if isinstance(dict_value, dict):
            dict_value["index"] = key
        return dict_value

    # 章节怪物信息解析
    def parser_explore(self, response):
        soup = BeautifulSoup(response, "html.parser", from_encoding="utf-8")
        html_p = soup.find_all("p")
        is_print = False
        chapter = 0
        for html in html_p:
            html_text = html.get_text()
            if html_text == "1、雀食奇谭：":
                is_print = True
            # 妖怪1(困难)-天邪鬼绿<天邪鬼绿*1+跳跳犬*2>
            # 番外、见习鬼使
            if html_text == "番外、见习鬼使":
                is_print = False
            if is_print:
                try:
                    if re.search(r'\d+、', html_text) is not None:
                        chapter, new_data = self.__parser_chapter_title(html_text)
                        self.dict_chapter.append(new_data)
                    else:
                        # 妖怪1(简单)-天邪鬼绿<天邪鬼绿*1+灯笼鬼*2>
                        # 妖怪2-天邪鬼绿<天邪鬼绿*1+ 提灯小僧*2>
                        # BOSS-九命猫<九命猫*3>
                        info = re.search(r"(.*)-(.*)<(.*)>", html_text)
                        if info.group() is not None:
                            monster_desc = info.group(1)        # 妖怪1(简单)
                            monster_main = info.group(2)        # 天邪鬼绿
                            monster_detail = info.group(3)      # 天邪鬼绿*1+灯笼鬼*2

                            all_descs = []
                            info_desc = re.search(r'妖怪(.*)', monster_desc)
                            if info_desc is None:
                                all_descs.append(monster_desc) # BOSS
                            else:
                                chapters = info_desc.group(1).split("，")
                                for cpt in chapters:
                                    all_descs.append(cpt)
                            # print(all_descs)
                            for cpt in all_descs:
                                dict_monster, dict_monster_details = \
                                    self.__parser_chapter_monster(chapter, cpt, monster_main, monster_detail)
                                self.dict_chapter_monster.append(dict_monster)
                                self.dict_chapter_monster_detail.extend(dict_monster_details)
                except Exception as e:
                    print("craw error! %s", html_text)
                    print(e)
        return self.dict_chapter, self.dict_chapter_monster, self.dict_chapter_monster_detail

    # 处理探索章节标题 例如：1、雀食奇谭：
    def __parser_chapter_title(self, html_text):
        new_data = {}
        info = re.search(r'(\d+)、(.*)', html_text)
        chapter = int(info.group(1))
        title = info.group(2).strip("：")
        new_data["chapter"] = chapter
        new_data["title"] = title
        print("第%d章 %s" % (chapter, title))
        return chapter, new_data

    # 处理各章节中的怪物明细
    def __parser_chapter_monster(self, chapter, monster_desc, monster_main, monster_detail):
        dict_monster = {}
        monster_type = "monster"
        difficulty = "all"
        location = 1

        if monster_main == self.dict_boss[str(chapter)]:        # BOSS
            monster_type = "BOSS"
        else:
            # 普通怪物
            # print(monster_desc)
            # print(re.search(r'\((.*)\)', monster_desc) is not None)
            if re.search(r'\((.*)\)', monster_desc) is not None:
                info = re.search(r'(\d+)\((.*)\)', monster_desc)
                location = info.group(1)
                if info.groups(2) == "简单":
                    difficulty = "easy"
                elif info.groups(2) == "困难":
                    difficulty = "difficult"
            else:
                info = re.search(r'(\d+)', monster_desc)
                location = info.group(1)
        dict_monster["chapter"] = chapter
        dict_monster["monster"] = monster_main
        dict_monster["difficulty"] = difficulty
        dict_monster["location"] = location
        dict_monster["monster_type"] = monster_type
        dict_monster_details = self.__parser_chapter_monster_detail(chapter, location, monster_detail)
        return dict_monster, dict_monster_details

    # 解析每一个怪物里的怪物种类
    def __parser_chapter_monster_detail(self, chapter, location, monster_detail):
        dict_monster_details = []

        # 涂壁*1+黑豹*1+天邪鬼赤*2
        if monster_detail is not None and len(monster_detail) > 0:
            infos = monster_detail.split("+")
            for info in infos:
                dict_monster_detail = {}
                info_detail = info.split("*")
                dict_monster_detail["chapter"] = chapter
                dict_monster_detail["location"] = location
                dict_monster_detail["monster"] = info_detail[0]
                dict_monster_detail["monster_cnt"] = int(info_detail[1])
                dict_monster_details.append(dict_monster_detail)
        return dict_monster_details
