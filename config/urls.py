"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from blog.views import post_list, post_detail, post_add, post_delete, serving_half_plus_two

urlpatterns = [
    path('admin/', admin.site.urls),
    path('serving/', serving_half_plus_two, name='serving_half_plus_two'),
    url(r'^$', post_list),
    url(r'^post/(?P<pk>\d+)/$', post_detail),
    url(r'^post/add/$', post_add, name='post_add'),
    url(r'^post/(?P<pk>\d+)/delete/$', post_delete, name='post_delete'),
]
