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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('loginseller', app.views.loginseller, name = 'loginseller'),
    path('loginhome', app.views.loginhome, name='loginhome'),
    path('buyerindex', app.views.buyerindex, name='buyerindex'),
    path('sellerindex', app.views.sellerindex, name='sellerindex'),
    path('seller_orderid/<str:id>', app.views.seller_orderid, name='seller_orderid'),
    path('seller_menu', app.views.seller_menu, name='seller_menu'),
    #path('edit_menu', app.views.edit_menu, name='edit_menu'),
    path('openorders', app.views.openorders, name='openorders'),
    path('viewindivorder/<str:id>', app.views.viewindivorder, name='viewindivorder'),
    path('add', app.views.add, name='add'),
    path('addgrouporder', app.views.addgrouporder, name='addgrouporder'),
    path('view/<str:id>', app.views.view, name='view'),
    path('addindivorder/<str:id>', app.views.addindivorder, name='addindivorder'),
    path('edit/<str:id>', app.views.edit, name='edit'),
]
