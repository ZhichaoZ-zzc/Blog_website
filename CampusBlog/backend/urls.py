
from django.contrib import admin
from django.urls import path,re_path
from Web.views import account,home
from .views import user,trouble


urlpatterns = [
    re_path(r'^index.html$', user.index),
    re_path(r'^base-info.html$', user.base_info),
    re_path(r'^tag.html$', user.tag),
    re_path(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$',user.article,name='article'),
    re_path(r'^add-article.html$', user.add_article),
    re_path(r'^edit-article-(?P<nid>\d+).html$', user.edit_article),
    re_path(r'^upload-avatar.html$', user.upload_avatar),
    re_path(r'^category.html$', user.category),
    #一般用户创建问题
    re_path(r'^trouble-list.html$', trouble.trouble_list),
    re_path(r'^trouble-create.html$', trouble.trouble_create),
    re_path(r'^trouble-edit-(\d+).html$', trouble.trouble_edit),
    #管理员解决问题
    re_path(r'^trouble-kill-list.html$', trouble.trouble_kill_list),
    re_path(r'^trouble-kill-(\d+).html$', trouble.trouble_kill),

]
