from django.db import models
from suser.models import *


# Create your models here.

class Base(object):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        """
        如果你想把某些公共信息添加到很多 model 中，抽象基类就显得非常有用。
        你编写完基类之后，在 Meta 内嵌类中设置 abstract=True ，
        该类就不能创建任何数据表。然而如果将它做为其他 model 的基类，那么该类的字段就会被添加到子类中。
        抽象基类和子类如果含有同名字段，就会导致错误(Django 将抛出异常)。
        """
        abstract = True  # 不用创建表可以省区重复写的代码直接继承就可以使用


class Cart(Base, models.Model):
    user_id = models.IntegerField()
    goods_id = models.IntegerField()
    count = models.IntegerField()
    goods_name = models.CharField(max_length=255)
    goods_price = models.DecimalField(max_digits=8, decimal_places=2)
    pic = models.CharField(max_length=255)
    is_check = models.IntegerField(default=0)  # 0 未选中 1 选中

    class Meta:
        db_table = 'cart'


# 订单表
class Order(Base, models.Model):
    order_sn = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmoney = models.DecimalField(max_digits=7, decimal_places=2)
    address = models.CharField(max_length=255, default='')
    status = models.IntegerField(default=0)  # 状态 0未支付 1已支付 2支付失败 3 待发货 4已发货 5
    pay_type = models.IntegerField(default=1)  # 1 支付宝 2 微信 3 网银
    code = models.CharField(max_length=100, default='')  # 流水号

    class Meta:
        db_table = 'order'


# 订单详情表
class OrderDetail(models.Model):
    order_sn = models.ForeignKey(Order, to_field='order_sn', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)
    is_comment = models.IntegerField(default=0)  # 是否评论 0没有评论，1已评论

    class Meta:
        db_table = 'order_detail'


# 地址表
class Address(models.Model):
    username = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province_id = models.IntegerField()  # 省id
    city_id = models.IntegerField()  # 市id
    district_id = models.IntegerField()  # 县区id
    detail_address = models.CharField(max_length=128)  # 详情地址
    phone = models.CharField(max_length=11)  # 手机号
    fix_phone = models.CharField(max_length=50, null=True, blank=True, default='')  # 固定电话
    e_mail = models.CharField(max_length=50, null=True, blank=True, default='')  # 邮箱
    is_default = models.IntegerField(default=0)  # 是否为默认 0 否 1 是
    address = models.CharField(max_length=255)  # 地址

    class Meta:
        db_table = 'address'


# 评论表
class Comment(models.Model):
    comment = models.CharField(max_length=255)  # 评论内容
    satisfaction = models.IntegerField(default=5)  # 评论满意度
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户评论
    is_anonymity = models.IntegerField(default=0)  # 是否匿名
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'
