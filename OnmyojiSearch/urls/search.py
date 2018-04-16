# _*_coding:utf-8_*_
from django.conf.urls import url

from OnmyojiSearch.views import IndexView


urlpatterns = [
    url(r'^index/(?P<rarity>[0-9])/$', IndexView.IndexView.as_view(), name="index"),
    url(r'^index/$', IndexView.index, name="index"),
]

app_name = "search"
