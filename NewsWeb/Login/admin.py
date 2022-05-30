from django.contrib import admin

# Register your models here.

from .models import User
from .models import Scan
from .models import News
from .models import Newsparticiple
from .models import Collect

admin.site.site_header = '基于情感分析的新闻推荐系统'
class UserManage(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('password',)
        return readonly_fields
    list_display = ['id', 'username', 'sex', 'telephone']
    list_display_links = ['username']
    search_fields = ['username']


class ScanManage(admin.ModelAdmin):
    list_display = ['id', 'user', 'news_title', 'emotion_score']
    list_display_links = ['user']
    search_fields = ['user']
    list_filter = ['user']

class NewsManage(admin.ModelAdmin):
    list_display = ['news_id', 'news_title', 'news_content', 'news_link', 'news_author', 'news_source', 'news_date', 'news_scan', 'news_comment']
    list_display_links = ['news_title']
    list_filter = ['news_source']
    search_fields = ['news_title']

class NewsPariticipleManage(admin.ModelAdmin):
    list_display = ['news_id', 'news_title', 'news_participle', 'emotion_score', 'heat']
    search_fields = ['news_title']
    list_display_links = ['news_title']

class CollectManage(admin.ModelAdmin):
    list_display = ['id', 'user', 'news_title', 'emotion_score']
    search_fields = ['news_title']
    list_filter = ['user']
    list_display_links = ['user']


admin.site.register(User, UserManage)
admin.site.register(Scan, ScanManage)
admin.site.register(News, NewsManage)
admin.site.register(Newsparticiple, NewsPariticipleManage)
admin.site.register(Collect, CollectManage)

