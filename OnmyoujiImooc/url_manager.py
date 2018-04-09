# _*_coding:utf-8_*_


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()       # url下载管理器
        self.new_urls_pic = set()   # 图片下载url管理器

    def add_new_url(self, root_url, is_pic = False):
        if root_url is None or root_url in self.new_urls:
            return
        if is_pic:
            self.new_urls_pic.add(root_url)
        else:
            self.new_urls.add(root_url)

    def has_new_url(self, is_pic = False):
        if is_pic:
            return len(self.new_urls_pic) > 0
        return len(self.new_urls) > 0

    def get_new_url(self, is_pic = False):
        if is_pic:
            return self.new_urls_pic.pop()
        new_url = self.new_urls.pop()
        return new_url
