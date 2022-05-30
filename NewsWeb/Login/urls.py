"""NewsWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login.html', views.login),
    path('register.html', views.register),
    path('recommend.html', views.recommend),
    path('yangshi.html', views.yangshi),
    path('xinghua.html', views.xinghua),
    path('renming.html', views.renming),
    path('zhongguo.html', views.zhongguo),
    path('alter.html', views.alter),
    path('qingnian.html', views.qingnian),
    path('detail.html/', views.detail),
    path('collect.html', views.collect),
    path('search.html', views.search),
    path('usercollect.html', views.UserCollect),
]
