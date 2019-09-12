from django.db import models


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


# 管理员表
class Sadmin(Base, models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.IntegerField(default=0)  # 1超级管理员，0普通管理员

    class Meta:
        db_table = 'sadmin'


# 分类表
class Cate(Base, models.Model):
    name = models.CharField(max_length=128)
    pid = models.IntegerField(default=0)  # 上级分类ID
    type = models.IntegerField(default=1)  # 标识几级分类
    top_id = models.IntegerField(default=0)  # 顶级id
    is_recommend = models.IntegerField(default=0)  # 首页是否推荐，0不推荐，1推荐
    pic = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'cate'


# 标签表
class Tags(Base, models.Model):
    name = models.CharField(max_length=50, unique=True)
    cid = models.ForeignKey(Cate, on_delete=models.CASCADE)
    is_recommend = models.IntegerField(default=0)  # 首页是否推荐，0不推荐，1推荐

    class Meta:
        db_table = 'tags'


# 焦点图表
class Banner(Base, models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_show = models.IntegerField(default=0)  # 是否显示，0不显示，1显示
    sort = models.IntegerField(default=1)  # 显示顺序
    type = models.IntegerField(default=1)  # 1 焦点图 2 广告图

    class Meta:
        db_table = 'banner'


# 新闻表
class News(Base, models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    is_recommend = models.IntegerField(default=0)  # 是否推荐 1 推荐， 0 不推荐

    class Meta:
        db_table = 'news'


# 商品表
class Goods(Base, models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)  # 商品描述
    price = models.DecimalField(max_digits=7, decimal_places=2)
    store = models.IntegerField(default=0)  # 库存
    lock_store = models.IntegerField(default=0)  # 锁定库存
    pic = models.CharField(max_length=100)  # 图片
    is_recommend = models.IntegerField(default=0)  # 是否推荐 1 推荐， 0 不推荐
    content = models.TextField()
    cid = models.ForeignKey(Cate, on_delete=models.CASCADE)  # 分类id
    tagid = models.ForeignKey(Tags, on_delete=models.CASCADE)  # 标签id
    t_comment = models.IntegerField(default=0)  # 总评论数
    top_id = models.IntegerField(default=0)  # 顶级分类ID
    sales = models.IntegerField(default=0)  # 销量

    class Meta:
        db_table = 'goods'


from django.contrib.auth.models import AbstractUser


# 用户表
class User(Base, AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    image = models.CharField(max_length=255, default='')
    signator = models.CharField(max_length=255, default='')  # 个性签名
    is_valide = models.IntegerField(default=0)  # 验证 0未验证，1验证
    token = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'user'


# 资源表(resource)
class Resource(models.Model):
    name = models.CharField(max_length=255)  # 资源名称
    url = models.CharField(max_length=255)  # 跳转url
    status = models.IntegerField()  # 1、启用 0、停用

    class Meta:
        db_table = 'resource'


# 角色表(role)
class Role(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField()  # 1、启用 2、停用
    resource_role = models.ManyToManyField(Resource, blank=True, related_name='role_resource')

    class Meta:
        db_table = 'role'


# 管理员表
class Aaa(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.IntegerField(default=0)  # 是否为超级管理员 1是 0否
    aa = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'aaa'


class City(models.Model):
    pid = models.IntegerField()
    cityname = models.CharField(max_length=50)
    type = models.IntegerField()

    class Meta:
        db_table = 'city'
