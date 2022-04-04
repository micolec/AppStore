"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
import app.views


urlpatterns = [
    path('', app.views.index, name='index'),
    path('login', app.views.login, name='login'),
    path('loginseller', app.views.loginseller, name = 'loginseller'),
    path('logout', app.views.logout, name = 'logout'),

    path('openorders/<str:username>', app.views.openorders, name='openorders'),
    path('filtered_openorders/<str:username>/<str:shopname>', app.views.filtered_openorders, name = 'filtered_openorders'),
    path('viewindivorder/<str:id>', app.views.viewindivorder, name='viewindivorder'),
    path('topup/<str:id>', app.views.topup, name='topup'),
    path('addgrouporder/<str:username>', app.views.addgrouporder, name='addgrouporder'),
    path('addindivorder/<str:id>', app.views.addindivorder, name='addindivorder'),

    path('sellerorders', app.views.sellerorders, name='sellerorders'),
    path('sellerindex', app.views.sellerindex, name='sellerindex'),
    path('seller_orderid/<str:id>', app.views.seller_orderid, name='seller_orderid'),
    path('seller_menu', app.views.seller_menu, name='seller_menu'),
    path('edit_menu', app.views.edit_menu, name='edit_menu'),

    path('buyerindex', app.views.buyerindex, name='buyerindex'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
]
