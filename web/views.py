import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from suser.models import *
from suser.serializer import *
from django.http import HttpResponse
from django.core.mail import EmailMessage
from 美多商城.settings import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.generics import RetrieveAPIView



# Create your views here.F

# 获取一级分类下的数据

class GetCateGoods(APIView):
    def get(self, request):
        cate = Cate.objects.filter(pid=0).all()  # 获取一级分类
        clist = []
        for x in cate:
            cdict = {}
            cdict['id'] = x.id
            cdict['name'] = x.name
            cdict['pic'] = x.pic
            # 获取一级下面的二级
            cate2 = Cate.objects.filter(pid=x.id).all()
            c2 = CateModelSerializers(cate2, many=True)
            cdict['sublist'] = c2.data
            # 获取一级分类下的标签
            tags = Tags.objects.filter(cid_id=x.id).all()
            t = TagModelSerializers(tags, many=True)
            cdict['tags'] = t.data
            # 获取一级分类下的产品
            goods = Goods.objects.filter(top_id=x.id).all()
            g = GoodsModelSerializers(goods, many=True)
            cdict['goods'] = g.data
            clist.append(cdict)

        mes = {}
        mes['code'] = 200
        mes['catelist'] = clist
        return Response(mes)


class GetGoodsByTags(APIView):
    def get(self, request):
        tid = request.GET.get('tid')
        cid = request.GET.get('cid')
        print(tid)
        goods = Goods.objects.filter(tagid=tid, top_id=cid).all()
        print(tid)
        print(goods)
        g = GoodsModelSerializers(goods, many=True)
        mes = {}
        mes['code'] = 200
        mes['catelist'] = g.data
        return Response(mes)


class GetGoodsById(APIView):
    def get(self, request):
        id = request.GET.get('id')
        good = Goods.objects.get(id=id)
        good_list = Goods.objects.all().order_by('-sales')
        print('*****************')
        print(good)
        print(good_list)
        print('*****************')
        g = GoodsModelSerializers(good, many=False)
        g_list = GoodsModelSerializers(good_list, many=True)
        mes = {}
        mes['code'] = 200
        mes['good'] = g.data
        mes['good_list'] = g_list.data

        return Response(mes)


# 导入图片验证码包
from utils.captcha.captcha import captcha


# 获取图片验证码
def getImageCode(request):
    name, text, image = captcha.generate_captcha()
    # image = image.load_default().font

    # 存入session,用户提交的时候对比
    request.session['img_code'] = text
    return HttpResponse(image, 'image/jpg')


class Reg(APIView):
    def post(self, request):
        mes = {}
        # 获取用户输入
        content = request.data.copy()
        print(content)
        # 验证图片验证码是否一样
        text = request.session.get('img_code')
        print(text)
        # 判断用户名是否唯一
        name = User.objects.filter(username=content['username']).first()
        if name:
            mes['code'] = 10010
            mes['message'] = '用户已存在'
        # 生成token
        token1 = str(uuid.uuid1())
        content['token'] = token1
        u = UserSerializer(data=content)
        if u.is_valid():
            # 写入数据库
            u.save()
            email = content['email']
            print(email)
            send_m = EmailMessage('欢迎注册', '<a href="http://localhost:8000/web/valid_email/?token=' + token1 + '">点击</a>',
                                  DEFAULT_FROM_EMAIL, [email])
            print('发送完毕')
            send_m.content_subtype = 'html'
            send_m.send()
            mes['code'] = 200
            mes['message'] = '注册成功'
        else:
            print(u.errors)
        return Response(mes)


class ActivView(APIView):
    def get(self, request):
        mes = {}
        token = request.GET.get('token')
        print(token)
        user = User.objects.filter(token=token).first()
        if user:
            user.is_valide = 1
            user.save()
            mes['code'] = 200
            mes['message'] = '激活成功'
        else:
            mes['code'] = 1001
            mes['message'] = '激活失败'
        return Response(mes)


class login(APIView):
    def post(self,request):
        mes={}
        content = request.data
        print(content)
        username = content['username']
        one_user = User.objects.filter(username=username).first()
        print(one_user)
        u = UserModelSerializer(one_user,many=False)
        mes['code']=200
        mes['message']=u.data
        return Response(mes)


