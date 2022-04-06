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
    path('basebuyer/<str:username>', app.views.basebuyer, name='basebuyer'),
    path('baseseller/<str:username>', app.views.baseseller, name='baseseller'),

    #LOGIN/OUT
    path('', app.views.index, name='index'),
    path('login', app.views.login, name='login'),
    path('loginseller', app.views.loginseller, name = 'loginseller'),
    path('logout', app.views.logout, name = 'logout'),

    #BUYERS
    path('openorders/<str:username>', app.views.openorders, name='openorders'),
    path('filtered_openorders/<str:username>/<str:shopname>', app.views.filtered_openorders, name = 'filtered_openorders'),
    path('viewindivorder/<str:id>', app.views.viewindivorder, name='viewindivorder'),
    path('deliverystatus/<str:username>', app.views.deliverystatus, name = 'deliverystatus'),
    path('topup/<str:id>', app.views.topup, name='topup'),
    path('addgrouporder/<str:username>', app.views.addgrouporder, name='addgrouporder'),
    path('addindivorder/<str:id>', app.views.addindivorder, name='addindivorder'),
    path('promo', app.views.promo, name='promo'),
    path('buyerstats/<str:username>', app.views.buyerstats, name='buyerstats'),
    path('buyer_menu_choice/<str:username>', app.views.buyer_menu_choice, name='buyer_menu_choice'),
    path('buyer_menu', app.views.buyer_menu, name='buyer_menu'),
    

    #SELLERS
 #   path('sellerorders/<str:username>', app.views.sellerorders, name='sellerorders'),
    path('sellerindex/<str:shopname>', app.views.sellerindex, name='sellerindex'),
    path('sellerindex/seller_orderid/<str:id>', app.views.seller_orderid, name='seller_orderid'),
    path('seller_menu/<str:shopname>', app.views.seller_menu, name='seller_menu'),
    path('seller_menu/edit_menu/<str:item>', app.views.edit_menu, name='edit_menu'),
    path('seller_menu/add_menu/<str:shopname>', app.views.add_menu, name='add_menu'),

    #SUPERADMIN
    path('buyerindex', app.views.buyerindex, name='buyerindex'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:username>', app.views.edit, name='edit'),
    path('ordersindex', app.views.ordersindex, name='ordersindex'),
    path('orderadd', app.views.orderadd, name='orderadd'),
    path('orderedit/<str:group_order_id>', app.views.orderedit, name='orderedit'),
    path('stats', app.views.stats, name='stats'),
    path('indivorderindex/<str:group_order_id>', app.views.indivorderindex, name='indivorderindex'),
    path('indivorderadd/<str:group_order_id>', app.views.indivorderadd, name='indivorderadd'),
    path('indivorderedit/<str:group_order_id>/<str:username>/<str:item>', app.views.indivorderedit, name='indivorderedit')
]
