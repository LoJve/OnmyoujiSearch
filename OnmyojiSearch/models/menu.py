# _*_coding:utf-8_*_
from django.db import models
import uuid


class Menu(models.Model):
    menuID = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    menuName = models.CharField(max_length=20)
    menuDesc = models.CharField(max_length=50)
    menuUrl = models.CharField(max_length=100)

    class Meta:
        db_table = "sys_menu"

