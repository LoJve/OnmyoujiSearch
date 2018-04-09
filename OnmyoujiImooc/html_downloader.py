# _*_coding:utf-8_*_
from urllib import request


class HtmlDownloader(object):
    def download_with_header(self, new_url, headers):
        req = request.Request(new_url, None, headers)
        response = request.urlopen(req)
        return response

    def download(self, new_url):
        response = request.urlopen(new_url)
        return response
