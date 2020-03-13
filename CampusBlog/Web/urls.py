
from django.contrib import admin
from django.urls import path,re_path
from Web.views import account,home,test

urlpatterns = [
    # re_path(r'^test.html',test.login),
    # re_path(r'^yonghu.html$', test.index),
    #re_path(r'^logout2.html$', test.logout),

    re_path(r'^check_code.html$', account.check_code, name='check_code'),
    re_path(r'^register.html$', account.register),
    re_path(r'^login.html',account.login),
    re_path(r'^logout.html$', account.logout),
    re_path(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$',home.filter),
    re_path(r'^all/(?P<article_type_id>\d+).html$',home.index,name='index'),
    re_path(r'^(?P<site>\w+).html$', home.home),
    re_path(r'^(?P<site>\w+)/(?P<nid>\d+).html$',home.detail),
    re_path(r'^',home.index),


]
