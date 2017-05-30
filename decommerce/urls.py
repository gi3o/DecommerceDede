"""Decommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.views import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /category/1/
    url(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='category'),
    # ex: /product/12/
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name='product'),
    # ex: /search/
    url(r'^search/$', views.search, name='search'),
    # ex: /logout/
    url(r'^logout/$', views.logout, name='logout'),
    # used to handle login
    url(r'^login/$', views.login, name='login'),
    # used to handle registration
    url(r'^register/$', views.register, name = 'register'),
    # used to get media files
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]