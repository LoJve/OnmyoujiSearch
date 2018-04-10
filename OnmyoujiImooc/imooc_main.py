# _*_coding:utf-8_*_
import os

from OnmyoujiImooc import url_manager, html_downloader, html_parser, data_dealer


class ImoocMain(object):
    def __init__(self):
        self.header_shikigami = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Cookie': '_ntes_nnid=c5b5daeb1272d97430468e1732b568cb,1519825183974; _ntes_nuid=c5b5daeb1272d97430468e1732b568cb; vjuids=62e79541e.16205da9fb2.0.e23af2242a33e8; vjlast=1520516637.1520516637.30; __gads=ID=59c97ce1e0c376c9:T=1520516640:S=ALNI_MY-Ulu5qdgjdVnFyI8fl1cbMrvlgg; __f_=1520606092579; usertrack=ezq0pVqv1lZt26J6F2vwAg==; _ga=GA1.2.882545791.1521473117; __oc_uuid=a45a5000-2d17-11e8-bb06-219006dfa7e9; __utma=187553192.882545791.1521473117.1521644020.1521644020.1; __utmz=187553192.1521644020.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; P_INFO=hjdong8@163.com|1522930382|1|imooc|00&99|jis&1522703808&mail#gud&440300#10#0#0|150232&0|mail&vipmember&mailuni|hjdong8@163.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Host': 'g37simulator.webapp.163.com',
            'Referer': 'https://yys.163.com/shishen/index.html'
        }
        self.root_url_shikigami = "https://g37simulator.webapp.163.com/get_heroid_list?callback=jQuery1113018601753522716624_1523006109494&rarity=0&page=1&per_page=200&_=1523006109496"
        self.root_url_pic = "https://yys.res.netease.com/pc/zt/20161108171335/data/shishen/%d.png"
        self.root_url_explore = "http://yys.163.com/skill/xinshou/2016/10/18/23029_648575.html"
        self.pic_path = "../OnmyojiSearch/static/OnmyojiSearch/image/"
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.dealer = data_dealer.DataDealer()

    # 爬取式神基础数据
    def craw_shikigami(self):
        self.urls.add_new_url(self.root_url_shikigami)
        if self.urls.has_new_url():
            new_url = self.urls.get_new_url()
            response = self.downloader.download_with_header(new_url, self.header_shikigami)
            shikigami_dict = self.parser.parser_shikigami(response.read().decode("utf-8"))
            for new_data in shikigami_dict:
                self.craw_shikugami_pic(int(new_data["index"]))
                self.dealer.collect_data(new_data)
            self.dealer.deal_data_shikigami()

    # 爬取式神图片
    def craw_shikugami_pic(self, index):
        root_url_pic = self.root_url_pic % index
        self.urls.add_new_url(root_url_pic, is_pic=True)
        if self.urls.has_new_url(True):
            # 有部分图片获取不到，加个异常捕获
            try:
                new_url = self.urls.get_new_url(True)
                response = self.downloader.download(new_url)
                # 图片下载
                BASE_DIR = os.path.dirname(__file__)
                path = os.path.join(BASE_DIR, self.pic_path)
                filename = "%d.png" % index
                self.dealer.download_pic(response.read(), path, filename)
            except Exception as e:
                print("craw %d pic failed" % index)

    # 爬取探索章节副本每章怪物详情
    def craw_explore(self):
        self.urls.add_new_url(self.root_url_explore)
        if self.urls.has_new_url():
            new_url = self.urls.get_new_url()
            response = self.downloader.download(new_url)
            dict_chapter, dict_chapter_monster, dict_chapter_monster_details = self.parser.parser_explore(response)
            self.dealer.save_chapter_data(dict_chapter, dict_chapter_monster, dict_chapter_monster_details)



if __name__ == "__main__":
    obj = ImoocMain()
    obj.craw_shikigami() # 爬取基础数据
    obj.craw_explore()      # 爬取探索章节怪物信息

