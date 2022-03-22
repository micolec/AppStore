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
    path('login', auth_views.LoginView.as_view(template_name='AppHONUSupper/login.html'), name='login'),
	path('logout', auth_views.LogoutView.as_view(template_name='AppHONUSupper/logout.html'), name='logout'),
    path(r'ride', app.views.ride, name='ride'),
	path(r'driver', app.views.driver, name='driver'),
	path(r'loginhome', app.views.loginhome, name='loginhome'),
	re_path(r'register', app.views.register, name='register'),
	re_path(r'profile', app.views.profile, name='profile'),
	re_path(r'advertise', app.views.advertise, name='advertise'),
	re_path(r'bid', app.views.bid, name='bid'),
	re_path('acceptance', app.views.acceptance, name='acceptance'),
 
    path('buyerindex', app.views.buyerindex, name='buyerindex'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
]
