"""美多商城 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from suser import views


urlpatterns = [
    path('index', views.index),
    path('reg', views.reg),
    path('login', views.login),
    path('submitlogin', views.SubmitLogin.as_view()),
    path('showCate', views.showCate),
    path('cateList', views.CateList.as_view()),
    path('addcate', views.AddCate),
    path('submitaddcate', views.SubmitAddCate.as_view()),
    path('delete', views.delete),
    path('showTag', views.showTag),
    path('submitaddtag', views.SubmitAddTag.as_view()),
    path('addtag', views.AddTag),
    path('showCate', views.showTag),
    path('delete_tag', views.delete_tag),
    path('tagList', views.TagList.as_view()),
    path('showNew', views.showNew),
    path('submitaddnew', views.SubmitAddNew.as_view()),
    path('addnew', views.AddNew),
    path('newList', views.NewList.as_view()),
    path('delete_new', views.delete_new),
    path('showBanner', views.showBanner),
    path('bannerList', views.bannerList.as_view()),
    path('addbanner', views.AddBanner),
    path('submitaddbanner', views.SubmitAddBanner.as_view()),
    path('delete_banner', views.delete_banner),
    path('showGoods', views.showGoods),
    path('submitaddgoods', views.SubmitAddGoods.as_view()),
    path('addgoods', views.AddGoods),
    path('goodsList', views.GoodsList.as_view()),
    path('delete_goods', views.delete_goods),
    path('tags', views.Tagss.as_view()),
    path('showRole', views.showRole),
    path('roleList', views.RoleList.as_view()),
    path('addrole', views.AddRole),
    path('submitaddrole', views.SubmitAddRole.as_view()),
    path('delete_role', views.delete_role),
    path('showResource', views.showResource),
    path('resourceList', views.ResourceList.as_view()),
    path('addresource', views.AddResource),
    path('submitaddresource', views.SubmitAddResource.as_view()),
    path('delete_resource', views.delete_resource),
    path('showaaa', views.showaaa),
    path('aaaList', views.aaaList.as_view()),
    path('addaaa', views.AddAAA),
    path('submitaddaaa', views.SubmitAddAAA.as_view()),
    path('delete_aaa', views.delete_aaa),
    path('indexList', views.indexList.as_view()),

]
