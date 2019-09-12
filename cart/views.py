import uuid, json

from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from cart.serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db import transaction
from django_redis import get_redis_connection
# Create your views here.


from rest_framework.generics import RetrieveAPIView

permission_classes = [IsAuthenticated]
authentication_classes = [JSONWebTokenAuthentication]

coon = get_redis_connection('default')


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        mes = {}
        content = request.data
        user_id = content['user_id']
        goods_id = content['goods_id']
        try:
            one_cart = coon.hget('cart' + user_id, goods_id).decode('utf-8')
            one_cart = json.loads(one_cart)
            one_cart['count'] += int(content['count'])
            coon.hset('cart' + user_id, goods_id, json.dumps(one_cart))
            print(one_cart['count'])

            all_cart = coon.hgetall('cart' + user_id)
            print(all_cart)
            mes['code'] = 200
            mes['message'] = '增加成功'

        except:
            coon.hset('cart' + user_id, goods_id, json.dumps(
                {'count': content['count'], 'is_check': 0, 'goods_name': content['goods_name'],
                 'goods_price': content['goods_price'], 'pic': content['pic'], 'goods_id': goods_id}))
            print(coon.hgetall('cart' + user_id))
            mes['code'] = 200
            mes['message'] = '添加成功'

        # one_cart = Cart.objects.filter(user_id=user_id, goods_id=goods_id).first()
        # if one_cart:
        #     one_cart.count += int(content['count'])
        #     one_cart.save()
        # else:
        #     c = CartSerializers(data=content)
        #     if c.is_valid():
        #         c.save()

        return Response(mes)


class MyCartList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        content = request.data
        print(content)
        user_id = content['user_id']

        my_cartlist = coon.hvals('cart' + user_id)
        c_list = []
        for x in my_cartlist:
            c_list.append(json.loads(x))
        # mycart = my_cartlist.decode('utf-8')
        # print(mycart)
        # cart = Cart.objects.filter(user_id=user_id).all()
        # c = CartModelSerializers(cart, many=True)
        mes = {}
        mes['code'] = 200
        mes['cartlist'] = c_list
        return Response(mes)


class AddNumber(APIView):
    def post(self, request):
        content = request.data
        user_id = content['user_id']
        goods_id = content['goods_id']
        one_cart = coon.hget('cart' + user_id, goods_id).decode('utf-8')
        one_cart = json.loads(one_cart)  # 将字符串转成字典
        one_cart['count'] += 1
        coon.hset('cart' + user_id, goods_id, json.dumps(one_cart))  # 将字典转成json对象字符串
        # one_cart = Cart.objects.filter(user_id=content['user_id'], goods_id=content['goods_id']).first()
        # one_cart.count += 1
        # one_cart.save()
        mes = {}
        mes['code'] = 200
        return Response(mes)


class SubNumber(APIView):
    def post(self, request):
        content = request.data
        user_id = content['user_id']
        goods_id = content['goods_id']
        print(content)
        one_cart = coon.hget('cart' + user_id, goods_id).decode('utf-8')
        one_cart = json.loads(one_cart)
        one_cart['count'] -= 1
        coon.hset('cart' + user_id, goods_id, json.dumps(one_cart))
        # one_cart = Cart.objects.filter(user_id=content['user_id'], goods_id=content['goods_id']).first()
        # one_cart.count -= 1
        # one_cart.save()
        mes = {}
        mes['code'] = 200
        return Response(mes)


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        mes = {}
        content = request.data
        goods_id = content['goods_id']
        user_id = content['user_id']
        cart = coon.hgetall('cart' + user_id)
        for x in cart:
            one_cart = coon.hget('cart' + user_id, x).decode('utf-8')
            one_cart = json.loads(one_cart)
            one_cart['is_check'] = 0
            coon.hset('cart' + user_id, x, json.dumps(one_cart))
        for i in goods_id:
            carts = coon.hget('cart' + user_id, i).decode('utf-8')
            carts = json.loads(carts)
            carts['is_check'] = 1
            coon.hset('cart' + user_id, i, json.dumps(carts))

        #     x['is_check'] = 1
        #     coon.hset('cart'+user_id,x['goods_id'],x)
        # print(cart)
        # cart['is_check'] = 1
        # print(coon.hgetall('cart'+user_id))

        # Cart.objects.filter(user_id=user_id).update(is_check=0)
        # Cart.objects.filter(id__in=cart_id).update(is_check=1)
        mes['code'] = 200
        mes['message'] = '修改成功'
        return Response(mes)


class ShowOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        print(request.data['user_id'])
        mes = {}
        content = request.data
        user_id = content['user_id']
        carts = coon.hgetall('cart' + user_id)
        c_list = []
        for x in carts:
            cat = coon.hget('cart' + user_id, x).decode('utf-8')
            c_list.append(cat)
        cat_list = []
        for i in c_list:
            i = json.loads(i)
            if i['is_check'] == 1:
                cat_list.append(i)
        default_address = Address.objects.filter(user_id=content['user_id'], is_default=1).first()
        d = AddressModelSerializers(default_address, many=False)
        mes['code'] = 200
        mes['default_address'] = d.data
        mes['cartlist'] = cat_list

        return Response(mes)


class ShowAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        mes = {}
        citys = City.objects.filter(pid=1).all()
        cty = CityModelSerializers(citys, many=True)
        address = Address.objects.all()
        a = AddressModelSerializers(address, many=True)

        mes['code'] = 200
        mes['add_list'] = a.data
        mes['provinces'] = cty.data
        return Response(mes)


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        user_id = content['user_id']
        # 生成order_code
        order_sn = uuid.uuid1()
        # 生成订单
        # 根据address_id去address表查询地址详情信息
        # 建立事务开始的节点
        sid = transaction.savepoint()
        # 构造订单数据
        carts = coon.hgetall('cart' + user_id)
        c_list = []
        for x in carts:
            cat = coon.hget('cart' + user_id, x).decode('utf-8')
            c_list.append(cat)
        cat_list = []
        for i in c_list:
            i = json.loads(i)
            if i['is_check'] == 1:
                cat_list.append(i)
                coon.hdel('cart' + user_id, i['goods_id'])
        # carts = Cart.objects.filter(user_id=content['user_id'], is_check=1).all()
        Order.objects.create(order_sn=order_sn, tmoney=0, address=content['address'], status=0,
                             pay_type=content['pay_method'], code='', user_id=content['user_id'])
        # 判断库存
        tprice = 0
        for x in cat_list:
            print(x['goods_name'])
            tprice += int(x['count']) * float(x['goods_price'])
            # print(tprice)
            goods = Goods.objects.get(id=x['goods_id'])

            if x['count'] > goods.store - goods.lock_store:
                transaction.rollback(sid)
                mes['code'] = 1010
                mes['message'] = '失败'
            else:
                transaction.commit(sid)
                # 构造详情表数据，进行添加
                OrderDetail.objects.create(name=x['goods_name'], price=x['goods_price'], count=x['count'], order_sn_id=order_sn,
                                           user_id=user_id, image=x['pic'], goods_id=x['goods_id'])
                # 更行商品表中的锁定库存
                Goods.objects.filter(id=x['goods_id']).update(lock_store=int(goods.lock_store) + int(x['count']))

            mes['code'] = 200
            mes['message'] = '提交成功'
        Order.objects.filter(order_sn=order_sn).update(tmoney=tprice)

        return Response(mes)


class GetCit(APIView):

    def post(self, request):
        mes = {}
        cityid = request.data['cityid']

        one_city = City.objects.get(id=int(cityid))

        city = City.objects.filter(pid=cityid).all()

        c = CityModelSerializers(city, many=True)
        if one_city.type == 1:
            mes['code'] = 200
            mes['cities'] = c.data
        else:
            mes['code'] = 200
            mes['districts'] = c.data
        return Response(mes)


class SaveAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        mes = {}
        content = request.data.copy()
        sheng = City.objects.get(id=content['province_id'])
        shi = City.objects.get(id=content['city_id'])
        xian = City.objects.get(id=content['district_id'])
        address = str(sheng.cityname) + str(shi.cityname) + str(xian.cityname) + str(content['detail_address'])
        content['address'] = address

        print(content)
        a = AddressSerializers(data=content)
        if a.is_valid():
            a.save()
            mes['code'] = 200
            mes['message'] = '添加成功'
        else:
            mes['code'] = 1010
            mes['message'] = '添加失败'
        return Response(mes)


class Is_default(APIView):
    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        Address.objects.filter(user_id=content['user_id']).update(is_default=0)
        Address.objects.filter(id=content['ad_id']).update(is_default=1)
        mes['code'] = 200
        mes['message'] = '设置成功'
        return Response(mes)


class GetMyOrders(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        mes = {}
        content = request.data
        user_id = request.GET.get('user_id')

        p = request.GET.get('p')
        print(p)
        if p == 'undefined':
            p = 1
        ods = Order.objects.filter(user_id=user_id).all()
        paginator = Paginator(ods, 1)
        currentPage = paginator.page(int(p))
        o = OrderModelSerializers(currentPage, many=True)
        totalPage = paginator.num_pages
        mes['code'] = 200
        mes['currentPage'] = p
        mes['totalPage'] = totalPage
        mes['order_list'] = o.data
        print(mes)
        return Response(mes)


class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        order_sns = OrderDetail.objects.get(id=content['id'])
        o = OrderDetailModelSerializers(order_sns, many=False)
        mes['code'] = 200
        mes['goods_list'] = o.data
        return Response(mes)


class SaveCommentAPIView(APIView):
    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        if content['is_anonymity'] == False:
            content['is_anonymity'] = 0
        else:
            content['is_anonymity'] = 1
        c = CommentSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = 200
            mes['message'] = '评论成功'
            OrderDetail.objects.filter(id=content['id']).update(is_comment=1)

        else:
            mes['code'] = 1020
            mes['message'] = '评论失败'
        return Response(mes)


class DeleteCartAPIView(APIView):
    def post(self, request):
        content = request.data
        print(content)
        user_id = content['user_id']
        goods_id = content['goods_id']
        print(user_id)
        coon.hdel('cart' + user_id, goods_id)
        mes = {}

        mes['code'] = 200
        mes['message'] = '删除成功'
        return Response(mes)
