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
from django.urls import path, include
from cart import views
from index import pay

urlpatterns = [
    path('cart/', views.CartAPIView.as_view()),
    path('mycartlist/', views.MyCartList.as_view()),
    path('addnumber/', views.AddNumber.as_view()),
    path('subnumber/', views.SubNumber.as_view()),
    path('order/', views.OrderAPIView.as_view()),
    path('createorder/', views.CreateOrderAPIView.as_view()),
    path('showorder/', views.ShowOrderAPIView.as_view()),
    path('showaddress/', views.ShowAddressAPIView.as_view()),
    path('getcit/', views.GetCit.as_view()),
    path('saveaddress/', views.SaveAddressAPIView.as_view()),
    path('is_default/', views.Is_default.as_view()),
    path('alipay/', pay.page1),
    path('getmyorder/', views.GetMyOrders.as_view()),
    path('comment/', views.CommentAPIView.as_view()),
    path('savecomment/', views.SaveCommentAPIView.as_view()),
    path('delete_cart/', views.DeleteCartAPIView.as_view()),

]
