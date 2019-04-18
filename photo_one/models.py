# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import timezone

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Datas(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    img = models.TextField(unique=True)
    detail_url = models.TextField(blank=True, null=True)
    raw_title = models.TextField(blank=True, null=True)
    view_price = models.TextField(blank=True, null=True)
    view_fee = models.TextField(blank=True, null=True)
    item_loc = models.TextField(blank=True, null=True)
    view_sales = models.TextField(blank=True, null=True)
    comment_count = models.TextField(blank=True, null=True)
    nick = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datas'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(unique=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ManageInformation(models.Model):
    manager_name = models.TextField(blank=True, null=True)
    manager_password = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manage_information'


class MenunameInformation(models.Model):
    menuname = models.TextField(blank=True, null=True)
    cuisine_field = models.TextField(db_column='Cuisine ', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    introduce_field = models.TextField(db_column='introduce ', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'menuname_information'


class Question(models.Model):
    user = models.TextField(blank=True, null=True)
    anser1 = models.TextField(blank=True, null=True)
    anser2 = models.TextField(blank=True, null=True)
    anser3 = models.TextField(blank=True, null=True)
    anser4 = models.TextField(blank=True, null=True)
    anser5 = models.TextField(blank=True, null=True)
    anser6 = models.TextField(blank=True, null=True)
    anser7 = models.TextField(blank=True, null=True)
    anser8 = models.TextField(blank=True, null=True)
    anser9 = models.TextField(blank=True, null=True)
    anser10 = models.TextField(blank=True, null=True)
    anser11 = models.TextField(blank=True, null=True)
    anser12 = models.TextField(blank=True, null=True)
    anser13 = models.TextField(blank=True, null=True)
    anser14 = models.TextField(blank=True, null=True)
    anser15 = models.TextField(blank=True, null=True)
    anser16 = models.TextField(blank=True, null=True)
    anser17 = models.TextField(blank=True, null=True)
    anser18 = models.TextField(blank=True, null=True)
    anser19 = models.TextField(blank=True, null=True)
    anser20 = models.TextField(blank=True, null=True)
    anser21 = models.TextField(blank=True, null=True)
    anser22 = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True, auto_now=False)

    class Meta:
        db_table = 'question'


class RecongnizeUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'recongnize_user'


class Request(models.Model):
    user = models.TextField(blank=True, null=True)
    the_most_nice = models.TextField(blank=True, null=True)
    the_demost_dence = models.TextField(blank=True, null=True)
    all_motion = models.TextField(blank=True, null=True)
    wishes = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True,null=True,auto_now=False)

    class Meta:
        db_table = 'request'


class BannerIndex(models.Model):
    name = models.CharField(max_length=120, verbose_name='名字')
    index_image = models.ImageField(blank=True, upload_to='products_images/%Y%m%d', verbose_name='banner图')

    class Meta:
        db_table = 'banner'


class SelectMenu(models.Model):
    name = models.CharField(max_length=120, verbose_name='已选菜单')
    user = models.CharField(max_length=120, verbose_name='选择人')
    date = models.DateField(blank=True, null=True, auto_now=False)

    class Meta:
        db_table = 'selectmenu'