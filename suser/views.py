import json, os
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from suser import models
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from utils.response_code import RET, error_map
from suser.models import Sadmin, Cate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from 美多商城.settings import UPLOAD_IMG, STATICFILES_DIRS
from django.core.paginator import Paginator


# Create your views here.
# 展示首页
def index(request):
    id = request.session.get('id')
    name = request.session.get('name')
    if id:
        admin1 = Sadmin.objects.filter(id=id, username=name).first()
        return render(request, 'admin/index.html', {'admin': admin1})
    else:
        admin2 = Aaa.objects.filter(id=id, username=name).first()
        return render(request, 'admin/index.html', {'admin': admin2})


# 分类列表
class indexList(APIView):
    def get(self, request):
        id = request.session.get('id')
        print(id)
        res = Role.objects.all()
        c = ResourceModelSerializers(res, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['indexlist'] = c.data
        return Response(mes)


# 登录
def login(request):
    return render(request, 'admin/login.html')


# 初始化管理员
def reg(request):
    password = make_password('123')
    reg = models.Sadmin(username='admin', password=password)
    reg.save()
    return HttpResponse('ok')


class SubmitLogin(View):
    def post(self, request):
        mes = {}
        # data = json.loads(request.body.decode())
        name = request.POST.get('name')
        password = request.POST.get('password')
        # one_user = Aaa.objects.filter(username=name, password=password).first()
        # if one_user:
        #     request.session['id'] = one_user.id
        #     request.session['username'] = one_user.username
        #     mes['code'] = 200
        #     mes['message'] = '登陆成功'

        if not all([name, password]):
            mes['code'] = RET.UPDATERROR
            mes['message'] = error_map[RET.NODATA]
        else:
            # 查询name
            admin = Sadmin.objects.filter(username=name).first()
            if admin:
                # 比较密码
                if check_password(password, admin.password):
                    request.session['id'] = admin.id
                    request.session['name'] = admin.name
                    mes['code'] = RET.OK
                    mes['message'] = error_map[RET.OK]
                else:
                    mes['code'] = RET.PWDERR
                    mes['message'] = error_map[RET.PWDERR]
            else:
                name = Aaa.objects.filter(username=name,password=password).first()
                if name:
                    request.session['id'] = name.id
                    request.session['name'] = name.username
                    mes['code'] = RET.OK
                    mes['message'] = error_map[RET.OK]
                else:
                    mes['code'] = RET.USERERR
                    mes['message'] = error_map[RET.USERERR]
        return Response(mes)


# 展示分类页面
def showCate(request):
    return render(request, 'admin/cates_type.html', locals())


# 分类列表
class CateList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        cate = Cate.objects.all()
        page_count = 1
        # 每页显示多少条
        page = Paginator(cate, 2)
        # 实例化分页对象
        cate_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = CateModelSerializers(cate_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['catelist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 展示添加分类页面
def AddCate(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Cate.objects.get(id=id)
        print(id)
    except:
        id = ''
    cate1 = Cate.objects.filter(pid=0).all()
    cate2 = Cate.objects.filter(pid=1).all()
    return render(request, 'admin/add_cate.html', locals())  # locals()传递所有参数


# 上传图片的方法
def upload_img(img):
    if img:
        # 打开这个目录下的文件如果没有就创建，二进制写入
        path = datetime.now().strftime('%Y%m%d%H%M%S%f') + img.name
        f = open(os.path.join(STATICFILES_DIRS[0], path), 'wb')
        for chunk in img.chunks():
            f.write(chunk)
        f.close()
        a = 'http://127.0.0.1:8000/static/' + path

        print(a)
        return a
    return ''


# 添加分类
class SubmitAddCate(APIView):

    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        # 通过pid构造top_id,type
        try:
            pid = int(content['pid'])
        except:
            pid = 0
        if pid == 0:
            type = 1
            top_id = 0
        else:
            cate = Cate.objects.get(id=pid)
            type = cate.type + 1
            if cate.top_id == 0:
                top_id = cate.id
            else:
                top_id = cate.top_id
        content['type'] = type
        content['top_id'] = top_id

        # 上传图片
        img = request.FILES.get('pic')
        path = upload_img(img)
        content['pic'] = path
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Cate.objects.get(id=id)
            c = CateSerializers(one_cate, data=content)
        else:
            c = CateSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除分类
def delete(request):
    id = request.GET.get('id')
    Cate.objects.filter(id=id).delete()
    return redirect('/suser/showCate')


# 展示标签
def showTag(request):
    return render(request, 'admin/tags_type.html', locals())


# 添加标签
class SubmitAddTag(APIView):
    def post(self, request):
        mes = {}
        content = request.data
        print(content)

        if not all([content['name'], content['cid'], content['is_recommend']]):
            mes['code'] = 10010
            mes['message'] = '信息不全'
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Tags.objects.get(id=id)
            c = TagSerializers(one_cate, data=content)
        else:
            c = TagSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 展示添加标签页面
def AddTag(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Tags.objects.get(id=id)
        print(id)
    except:
        id = ''
    cate1 = Cate.objects.filter(pid=0).all()
    return render(request, 'admin/add_tag.html', locals())  # locals()传递所有参数


# 标签列表
class TagList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        tag = Tags.objects.all()

        # 每页显示多少条
        page = Paginator(tag, 1)
        # 实例化分页对象
        tag_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = TagModelSerializers(tag_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['taglist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 删除标签
def delete_tag(request):
    id = request.GET.get('id')
    Tags.objects.filter(id=id).delete()
    return redirect('/suser/showTag')


# 展示新闻页
def showNew(request):
    return render(request, 'admin/news_type.html', locals())


# 添加新闻
class SubmitAddNew(APIView):
    def post(self, request):
        mes = {}
        content = request.data
        print('***********')
        print(content)
        if not all([content['title'], content['content'], content['is_recommend']]):
            mes['code'] = 10010
            mes['message'] = '信息不全'
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = News.objects.get(id=id)
            c = NewSerializers(one_cate, data=content)
        else:
            c = NewSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 展示添加新闻页面
def AddNew(request):
    try:
        id = request.GET.get('id')
        one_news = News.objects.get(id=id)
        print(id)
    except:
        id = ''
    return render(request, 'admin/add_news.html', locals())  # locals()传递所有参数


# 新闻列表
class NewList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        tag = News.objects.all()

        # 每页显示多少条
        page = Paginator(tag, 1)
        # 实例化分页对象
        news_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = NewModelSerializers(news_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['newslist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 删除新闻
def delete_new(request):
    id = request.GET.get('id')
    News.objects.filter(id=id).delete()
    return redirect('/suser/showNew')


# 展示焦点图
def showBanner(request):
    return render(request, 'admin/ban_type.html', locals())


# 焦点图列表
class bannerList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        ban = Banner.objects.all()
        page_count = 1
        # 每页显示多少条
        page = Paginator(ban, 2)
        # 实例化分页对象
        ban_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = BannerModelSerializers(ban_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['bannerlist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 展示添加焦点图页面
def AddBanner(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Banner.objects.get(id=id)
        print(id)
    except:
        id = ''
    return render(request, 'admin/add_ban.html', locals())  # locals()传递所有参数


# 添加焦点图
class SubmitAddBanner(APIView):
    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        if not all([content['name'], content['is_show'], content['sort'], content['type']]):
            mes['code'] = 10010
        # 上传图片
        img = request.FILES.get('name')
        path = upload_img(img)
        content['name'] = path

        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Banner.objects.get(id=id)
            c = BannerSerializers(one_cate, data=content)
        else:
            c = BannerSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除焦点图
def delete_banner(request):
    id = request.GET.get('id')
    Banner.objects.filter(id=id).delete()
    return redirect('/suser/showBanner')


# 展示商品页面
def showGoods(request):
    return render(request, 'admin/goods_type.html', locals())


# 商品列表
class GoodsList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        goods = Goods.objects.all()
        page_count = 1
        # 每页显示多少条
        page = Paginator(goods, 2)
        # 实例化分页对象
        goods_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = GoodsModelSerializers(goods_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['goodslist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 展示添加商品页面
def AddGoods(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Goods.objects.get(id=id)
        print(id)
    except:
        id = ''

    cate2 = Cate.objects.filter(type=2).all()
    tags = Tags.objects.all()
    return render(request, 'admin/add_goods.html', locals())  # locals()传递所有参数


# 添加商品
class SubmitAddGoods(APIView):

    def post(self, request):
        mes = {}
        content = request.data

        print(content)
        if not all([content['name'], content['description'], content['price'], content['store'], content['lock_store'],
                    content['pic'], content['is_recommend'], content['content'], content['cid'], content['tagid']]):
            mes['code'] = 1010
        # 通过pid构造top_id,type

        cid = Cate.objects.filter(id=content['cid']).first()
        content['top_id'] = cid.top_id
        content['sales'] = 0
        content['t_comment'] = 0

        # 上传图片
        img = request.FILES.get('pic')
        path = upload_img(img)
        content['pic'] = path
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Goods.objects.get(id=id)
            c = GoodsSerializers(one_cate, data=content)
        else:
            c = GoodsSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除商品
def delete_goods(request):
    id = request.GET.get('id')
    Goods.objects.filter(id=id).delete()
    return redirect('/suser/showGoods')


# 添加标签是动态加载
class Tagss(APIView):
    def get(self, request):
        mes = {}
        cid = request.GET.get('cid')
        cate = Cate.objects.get(id=cid)
        id = cate.top_id
        print('***********************')
        print(id)
        content = Tags.objects.filter(cid_id=id).all()
        print(content)
        c = TagModelSerializers(content, many=True)
        mes['code'] = 200
        mes['message'] = c.data
        return Response(mes)


# 展示角色页面
def showRole(request):
    return render(request, 'admin/role_type.html', locals())


# 角色列表
class RoleList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        role = Role.objects.all()
        page_count = 1
        # 每页显示多少条
        page = Paginator(role, 2)
        # 实例化分页对象
        role_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = RoleModelSerializers(role_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['rolelist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 展示添加角色页面
def AddRole(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Role.objects.get(id=id)
        print(id)
    except:
        id = ''
        resource = Resource.objects.all()
    return render(request, 'admin/add_role.html', locals())  # locals()传递所有参数


# 添加角色
class SubmitAddRole(APIView):

    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        if not all([content['name'], content['status'], content['resource_role']]):
            mes['code'] = 1010
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Role.objects.get(id=id)
            c = RoleSerializers(one_cate, data=content)
        else:
            c = RoleSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除角色
def delete_role(request):
    id = request.GET.get('id')
    Role.objects.filter(id=id).delete()
    return redirect('/suser/showRole')


# 展示资源页面
def showResource(request):
    return render(request, 'admin/resource_type.html', locals())


# 资源列表
class ResourceList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        role = Resource.objects.all()
        page_count = 1
        # 每页显示多少条
        page = Paginator(role, 2)
        # 实例化分页对象
        resource_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = ResourceModelSerializers(resource_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['resourcelist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 展示添加资源页面
def AddResource(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Resource.objects.get(id=id)
        print(id)
    except:
        id = ''
        role = Role.objects.all()
    return render(request, 'admin/add_resource.html', locals())  # locals()传递所有参数


# 添加资源
class SubmitAddResource(APIView):

    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        if not all([content['name'], content['status'], content['url']]):
            mes['code'] = 1010
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Resource.objects.get(id=id)
            c = ResourceSerializers(one_cate, data=content)
        else:
            c = ResourceSerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除资源
def delete_resource(request):
    id = request.GET.get('id')
    Resource.objects.filter(id=id).delete()
    return redirect('/suser/showResource')


# 展示管理员页面
def showaaa(request):
    return render(request, 'admin/aaa_type.html', locals())


# 管理员列表
class aaaList(APIView):
    def get(self, request):
        try:
            p = int(request.GET.get('p'))
        except:
            p = 1
        # 获取所有数据
        role = Aaa.objects.all()
        page_count = 1
        # 每页显示多少条
        page = Paginator(role, 2)
        # 实例化分页对象
        user_list = page.get_page(p)
        # 获取总页数
        totalPage = page.num_pages
        c = AAAModelSerializers(user_list, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['userlist'] = c.data
        mes['totalpage'] = totalPage
        mes['currentpage'] = p
        return Response(mes)


# 展示添加管理员页面
def AddAAA(request):
    # 获取一级分类
    try:
        id = request.GET.get('id')
        one_cate = Aaa.objects.get(id=id)
        roles = Role.objects.all()

        print(id)
    except:
        id = ''
        roles = Role.objects.all()
        print(roles)
    return render(request, 'admin/add_aaa.html', locals())  # locals()传递所有参数


# 添加资源
class SubmitAddAAA(APIView):

    def post(self, request):
        mes = {}
        content = request.data
        print(content)
        if not all([content['username'], content['password'], content['is_admin']]):
            mes['code'] = 1010
        try:
            id = int(request.POST.get('id'))
            print(id)
            print('*****************')
        except:
            id = ''
        if id:
            one_cate = Aaa.objects.get(id=id)
            c = AAASerializers(one_cate, data=content)
        else:
            c = AAASerializers(data=content)
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK
        else:
            print(c.errors)
            mes['code'] = 10020
        return Response(mes)


# 删除管理员
def delete_aaa(request):
    id = request.GET.get('id')
    Aaa.objects.filter(id=id).delete()
    return redirect('/suser/showaaa')
