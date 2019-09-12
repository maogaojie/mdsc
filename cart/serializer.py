from rest_framework import serializers
from cart.models import *


class CartModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartSerializers(serializers.Serializer):
    user_id = serializers.IntegerField()
    goods_id = serializers.IntegerField()
    count = serializers.IntegerField()
    goods_name = serializers.CharField()
    goods_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    pic = serializers.CharField()

    def create(self, data):
        cart = Cart.objects.create(**data)
        return cart

    def update(self, instance, validated_data):
        instance.user_id = validated_data['user_id']
        instance.goods_id = validated_data['goods_id']
        instance.count = validated_data['count']
        instance.goods_name = validated_data['goods_name']
        instance.goods_price = validated_data['goods_price']


class CityModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AddressModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AddressSerializers(serializers.Serializer):
    username = serializers.CharField()
    user_id = serializers.IntegerField()
    province_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    district_id = serializers.IntegerField()
    detail_address = serializers.CharField()
    phone = serializers.CharField()
    fix_phone = serializers.CharField(default='')
    e_mail = serializers.CharField(default='')
    address = serializers.CharField()

    def create(self, data):
        cart = Address.objects.create(**data)
        return cart

    def update(self, instance, validated_data):
        instance.user = validated_data['user']
        instance.province_id = validated_data['province_id']
        instance.city_id = validated_data['city_id']
        instance.district_id = validated_data['district_id']
        instance.detail_address = validated_data['detail_address']
        instance.phone = validated_data['phone']
        instance.fix_phone = validated_data['fix_phone']
        instance.e_mail = validated_data['e_mail']
        instance.is_default = validated_data['is_default']
        instance.address = validated_data['address']


class OrderModelSerializers(serializers.ModelSerializer):
    order_goods = serializers.SerializerMethodField()

    def get_order_goods(self, row):
        # 一个参数是row，代表的是当前行的记录
        order_goods = OrderDetail.objects.filter(order_sn=row.order_sn).all()
        order_goods_detail = OrderDetailModelSerializers(order_goods, many=True).data
        return order_goods_detail

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class CommentSerializers(serializers.Serializer):
    comment = serializers.CharField()  # 评论内容
    satisfaction = serializers.IntegerField()  # 评论满意度
    user_id = serializers.IntegerField()  # 用户评论
    is_anonymity = serializers.IntegerField(default=0)  # 是否匿名

    def create(self, validated_data):
        c = Comment.objects.create(**validated_data)
        return c
