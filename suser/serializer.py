from rest_framework import serializers
from suser.models import *
from django.contrib.auth.hashers import check_password, make_password


# 获取分类列表
class CateModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cate
        fields = '__all__'


# 添加分类
class CateSerializers(serializers.Serializer):
    name = serializers.CharField()
    pid = serializers.IntegerField()
    type = serializers.IntegerField()
    top_id = serializers.IntegerField()
    is_recommend = serializers.IntegerField()
    pic = serializers.CharField(default='')

    def create(self, data):
        cate = Cate.objects.create(**data)
        return cate

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.pid = validated_data['pid']
        instance.type = validated_data['type']
        instance.top_id = validated_data['top_id']
        instance.is_recommend = validated_data['is_recommend']
        instance.pic = validated_data['pic']
        instance.save()
        return instance


# 获取标签列表
class TagModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


# 添加标签
class TagSerializers(serializers.Serializer):
    name = serializers.CharField()
    cid = serializers.IntegerField()
    is_recommend = serializers.IntegerField()

    def create(self, data):
        A = Cate.objects.get(id=data['cid'])
        tag = Tags.objects.create(name=data['name'], cid=A, is_recommend=data['is_recommend'])
        return tag

    def update(self, instance, validated_data):
        # instance.name = validated_data['name']
        # instance.cid = validated_data['cid']
        # instance.is_recommend = validated_data['is_recommend']
        # instance.save()
        A = Cate.objects.get(id=validated_data['cid'])
        instance = Tags.objects.filter(id=validated_data['id']).update(name=validated_data['name'], cid=A,
                                                                       is_recommend=validated_data['is_recommend'])
        return instance


# 获取新闻列表
class NewModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


# 添加新闻
class NewSerializers(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    is_recommend = serializers.IntegerField()

    def create(self, data):
        new = News.objects.create(**data)
        return new

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.is_recommend = validated_data['is_recommend']
        instance.save()
        return instance


# 获取焦点图列表
class BannerModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


# 添加焦点图
class BannerSerializers(serializers.Serializer):
    name = serializers.CharField()
    is_show = serializers.IntegerField()
    type = serializers.IntegerField()
    sort = serializers.IntegerField()

    def create(self, data):
        ban = Banner.objects.create(**data)
        return ban

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.is_show = validated_data['is_show']
        instance.sort = validated_data['sort']
        instance.type = validated_data['type']
        instance.save()
        return instance


# 获取商品列表
class GoodsModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


# 添加商品
class GoodsSerializers(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    store = serializers.IntegerField()
    lock_store = serializers.IntegerField()
    pic = serializers.CharField()
    is_recommend = serializers.IntegerField()
    content = serializers.CharField()
    cid = serializers.IntegerField()
    tagid = serializers.IntegerField()
    t_comment = serializers.IntegerField()
    top_id = serializers.IntegerField()
    sales = serializers.IntegerField()

    def create(self, data):
        cid = Cate.objects.get(id=data['cid'])
        tagid = Tags.objects.get(id=data['tagid'])
        goods = Goods.objects.create(name=data['name'], cid=cid, tagid=tagid, description=data['description'],
                                     price=data['price'], store=data['store'], lock_store=data['lock_store'],
                                     pic=data['pic'], is_recommend=data['is_recommend'], content=data['content'],
                                     t_comment=data['t_comment'], top_id=data['top_id'], sales=data['sales'])
        return goods

    def update(self, instance, validated_data):
        cid = Cate.objects.get(id=validated_data['cid'])
        tagid = Tags.objects.get(id=validated_data['tagid'])
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.price = validated_data['price']
        instance.store = validated_data['store']
        instance.lock_store = validated_data['lock_store']
        instance.pic = validated_data['pic']
        instance.is_recommend = validated_data['is_recommend']
        instance.content = validated_data['content']
        instance.cid = cid
        instance.tagid = tagid
        instance.t_comment = validated_data['t_comment']
        instance.top_id = validated_data['top_id']
        instance.sales = validated_data['sales']
        instance.save()
        return instance


# 获取角色列表
class RoleModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


# 添加角色
class RoleSerializers(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.IntegerField()
    resource_role = serializers.CharField()

    def create(self, data):
        resource_role = data.pop('resource_role')
        role = Role.objects.create(**data)
        for x in resource_role:
            ro_re = Resource.objects.filter(id=int(x)).first()
            role.resource_role.add(ro_re)
            role.save()
        return role

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.status = validated_data['status']

        instance.save()
        return instance


# 获取资源列表
class ResourceModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


# 添加资源
class ResourceSerializers(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()
    status = serializers.IntegerField()

    def create(self, data):
        resource = Resource.objects.create(**data)
        return resource

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.status = validated_data['status']
        instance.url = validated_data['url']
        instance.save()
        return instance


# 获取管理员列表
class AAAModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Aaa
        fields = '__all__'


# 添加管理员
class AAASerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    is_admin = serializers.IntegerField()
    aa_id = serializers.IntegerField()

    def create(self, data):
        aaa = Aaa.objects.create(**data)
        return aaa

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.password = validated_data['password']
        instance.is_admin = validated_data['is_admin']
        instance.aa_id = validated_data['aa_id']
        instance.save()
        return instance


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# 反序列化user
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    token = serializers.CharField()

    def create(self, data):
        data['password'] = make_password(data['password'])

        us = User.objects.create(**data)
        return us

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.password = validated_data['password']
        instance.email = validated_data['email']
        instance.token = validated_data['token']
        instance.save()
        return instance


