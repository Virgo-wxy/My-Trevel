from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# 洲
class City(models.Model):
    image = models.CharField(max_length=225)
    title = models.CharField(max_length=225)
    name1 = models.CharField(max_length=225)
    name2 = models.CharField(max_length=225)
    name3 = models.CharField(max_length=225)
    price = models.IntegerField()


# 详情页
class CartInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(City, on_delete=models.CASCADE)
    # 出行人数
    travel_count = models.IntegerField(default=1)
    # 出发城市
    travel_city = models.CharField(max_length=225)
    # 出发日期
    travel_data = models.CharField(max_length=225)
    #联系方式
    travel_number = models.CharField(max_length=255)


# 高级定制
class Custom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # 出发城市
    cf_city = models.CharField(max_length=225)
    # 目的地
    dd_city = models.CharField(max_length=225)
    # 出发时间
    cf_date = models.CharField(max_length=225)
    # 旅行天数
    travel_days = models.IntegerField()
    # 出行成人
    travel_adult = models.IntegerField()
    # 出行儿童
    travel_children = models.IntegerField()
    # 称呼
    name = models.CharField(max_length=225)
    # 联系电话
    number = models.CharField(max_length=225)
    # 留言
    content = models.CharField(max_length=255,null=True,blank=True)

# 我要留言
class Guestbook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=225,null=True, blank=True)
    content = models.CharField(max_length=225,null=True, blank=True)