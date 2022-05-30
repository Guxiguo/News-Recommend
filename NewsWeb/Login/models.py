
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bosonnlp(models.Model):
    word = models.CharField(max_length=20, blank=True, null=True)
    score = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bosonnlp'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class News(models.Model):
    news_id = models.IntegerField('id', primary_key=True)
    news_title = models.CharField('新闻标题', max_length=100)
    news_content = models.CharField('新闻内容', max_length=1000)
    news_link = models.CharField('新闻链接', unique=True, max_length=100, blank=True, null=True)
    news_author = models.CharField('新闻作者', max_length=10, blank=True, null=True)
    news_source = models.CharField('新闻来源', max_length=30, blank=True, null=True)
    news_date = models.DateField('新闻日期', blank=True, null=True)
    news_scan = models.IntegerField('浏览量', blank=True, null=True)
    news_comment = models.IntegerField('评论量', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'
        verbose_name = '新闻'
        verbose_name_plural = verbose_name



class Newsparticiple(models.Model):
    news_id = models.IntegerField('id', primary_key=True)
    news_title = models.CharField('新闻标题', max_length=100)
    news_participle = models.CharField('新闻分词', max_length=1000)
    emotion_score = models.DecimalField('情感得分', max_digits=10, decimal_places=7, blank=True, null=True)
    heat = models.DecimalField('新闻热度', max_digits=3, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newsparticiple'
        verbose_name = '新闻处理'
        verbose_name_plural = verbose_name


class Scan(models.Model):
    user = models.CharField('用户名', max_length=20)
    news_title = models.CharField('新闻标题', max_length=100)
    emotion_score = models.DecimalField('情感得分', max_digits=10, decimal_places=7)

    class Meta:
        managed = False
        db_table = 'scan'
        verbose_name = '浏览记录'
        verbose_name_plural = verbose_name


class Similarity(models.Model):
    news_id1 = models.IntegerField(blank=True, null=True)
    news_id2 = models.IntegerField(blank=True, null=True)
    similarity = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'similarity'




class User(models.Model):
    id = models.BigAutoField('id', primary_key=True)
    username = models.CharField('用户名', max_length=20)
    sex = models.CharField('性别', max_length=1, blank=True, null=True)
    password = models.CharField('密码', max_length=30)
    telephone = models.CharField('电话', unique=True, max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name



class Collect(models.Model):
    user = models.CharField('用户名', max_length=20)
    news_title = models.CharField('新闻标题', max_length=100)
    emotion_score = models.DecimalField('情感得分', max_digits=10, decimal_places=7)

    class Meta:
        managed = False
        db_table = 'collect'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


