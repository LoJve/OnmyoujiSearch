# _*_coding:utf-8_*_
from django import template


register = template.Library()


@register.filter
def format_str(value, arg):
    return arg % value

