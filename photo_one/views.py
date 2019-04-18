from django.shortcuts import render,redirect
# Create your views here.
# coding=utf-8
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
import json
import os
from photo_one.models import Datas,RecongnizeUser,MenunameInformation,Question,Request,ManageInformation,BannerIndex, SelectMenu
import pytesseract
from pytesseract import *
from PIL import Image, ImageEnhance, ImageFilter
import os
import fnmatch
import re, time
import urllib, random
from django import forms
from django.forms import fields
from django.forms import widgets
from photo_one import models
import datetime
from django.utils import timezone
import json
# import hashlib
class User(forms.Form):
    # 登录界面的用户名框，error_messages为fields包的参数，输入为空时的提示，widget为该input标签的属性
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    # 密码框的定制
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"}))

class Newuser(forms.Form):
    # 注册界面用户名框最长长度不能超过9，最小不能小于3，且不能为空
    username = fields.CharField(max_length=9, min_length=3,
                                error_messages={'required': '用户名不能为空', 'max_length': '用户名长度不能大于9',
                                                'min_length': '用户名长度不能小于3'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    # 注册界面密码框最长长度不能超过12，最小不能小于6，且不能为空
    password = fields.CharField(max_length=12, min_length=6,
                                error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                                'min_length': '密码长度不能小于6'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )
    # 注册界面再次输入密码框最长长度不能超过9，并与前一个密码框内容比较，两次不一致提示“两次密码不一致”，最小不能小于3，且不能为空
    confirm_password = fields.CharField(max_length=12, min_length=6,
                                        error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                                        'min_length': '两次密码不一致'},
                                        widget=widgets.Input(
                                            attrs={'type': "password", 'class': "form-control",
                                                   'name': "confirm_password",
                                                   'id': "confirm_password",
                                                   'placeholder': "请重新输入密码"})
                                        )

def login(request):
    """
        登陆
        :param request:
        :return:
        """
    # 定义空字符串，以便向前端页面提示错误
    s = ''
    # Get请求，返回login.html界面，输入框规则参照制定的User()并实列化
    if request.method == 'GET':
        obj = User()
        return render(request, 'login.html', {'obj': obj})
        #return render(request,"用户管理.htm")
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        obj = User(request.POST)
        u = request.POST.get('username')
        t1 = models.RecongnizeUser.objects.filter(username=u)
        if t1:
            pwd = request.POST.get('password')
            if pwd == t1[0].pwd:
                request.session['user'] = u
                request.session['is_login'] = True
                s = '''
                    <script>document.cookie="user='''+ u +''';path=/";setTimeout(function(){location.href='/index/'},300)</script>
                '''
                # return redirect('/index/', {'s': 'wedasd'})
                return render(request, 'login.html', {'s': s})
            else:
                s = '''
                      <script>alert('密码错误!!!请重新输入!!!');</script>
                  '''
        # 输入的用户名不存在
        else:
            s = '''
               <script>alert('该用户名不存在!!!请检查是否正确!!!');</script>
                                    '''
        return render(request, 'login.html', {'obj': obj, 's': s})

def register(request):
    """
       注册
       :param request:
       :return:
       """
    # 定义空字符串，以便向前端页面提示错误
    er = ''
    # 如果是GET请求，实例化类Newuser(),即进行注册的表单验证
    if request.method == 'GET':
        obj = Newuser()
        return render(request, 'register.html', {'obj': obj, 'er': er})
    if request.method == 'POST':
        # form表单验证
        obj = Newuser(request.POST)
        # 该方法表示输入框的值是否都符合定制的规范，是则返回True，否则False
        r = obj.is_valid()
        if r:
            # 获取用户名框中内容并与数据库比较，若存在该用户，向像前端返回s，提示用户已经存在，不存在则继续验证
            user = request.POST.get('username')
            u = models.RecongnizeUser.objects.filter(username=user)
            if u:
                s = '''
                       <script>alert('用户名已经存在，请从新输入用户名！');
                   </script>
                       '''
            else:
                # 验证输入框两次密码是否相同，不相同则提示不一致
                pwd1 = request.POST.get('password')
                pwd2 = request.POST.get('confirm_password')
                if pwd1 != pwd2:
                    s = '''
                           <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                # 两次密码相同且用户不存在，注册成功，向前端提示成功
                else:
                    models.RecongnizeUser.objects.create(username=user, pwd=pwd1)
                    s = '''
                           <script>alert('注册成功！');
                           </script>'''
            return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
            # 输入不符合定制的form表单验证，提示格式不正确
        else:
            s = '''
               <script>alert('信息格式不正确,注册失败！');
                   </script>'''
            return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
def index(request):
    if request.method =='GET':
        banner = BannerIndex.objects.last().index_image.url
        return render(request, 'index.html', {'banner': banner})
    if request.method =='GET':
        u = request.POST.get()

def menu(request):
    if request.method =='GET':
        arr = []
        menus = MenunameInformation.objects.all()
        for menu in menus:
            arr.append({
                'menuname': menu.menuname
            })
            data = {
                'data': arr
            }
        return render(request, 'menu.html', data)

def information(request):
    if request.method == 'GET':
        arr = []
        data = {}
        for i in MenunameInformation.objects.all():
            arr.append({
                'menuname': i.menuname,
                'cuisine_field': i.cuisine_field,
                'introduce_field': i.introduce_field
            })
        data = {
            'data': arr
        }
        return render(request, 'information.html', data)
        #return render(request,"用户管理.htm")
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        u = request.POST.get('username')
        print(u)

        t1 = models.RecongnizeUser.objects.filter(username=u)


def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
    if request.method == 'POST':
        u = request.POST.get('datas')
        user = request.POST.get('user')
        print(u)
        answer = u.split(",")
        models.Request.objects.create(user=user,the_most_nice=answer[0],the_demost_dence=answer[1], date=timezone.now().strftime("%Y-%m-%d"))
        return HttpResponse('{"data":1}')



def question(request):
    if request.method =='GET':
        return render(request, 'questionnaire.html')
    if request.method =='POST':
        u = request.POST.get('answer')
        user = request.POST.get('user')
        print(u)
        answer = u.split(",")
        print(answer)
        # 一个月内只能提交一次
        for obj in models.Question.objects.filter(user=user):
            if obj.date.strftime("%Y-%m") == timezone.now().strftime("%Y-%m"):
                return HttpResponse('{"data":0}')

        models.Question.objects.create(user=user,anser1=answer[0],anser2=answer[1]
                                       ,anser3=answer[2],anser4=answer[3],anser5=answer[4]
                                       ,anser6=answer[5],anser7=answer[8],anser8=answer[7],anser9=answer[8]
                                       ,anser10=answer[9],anser11=answer[10],anser12=answer[11],anser13=answer[12]
                                       ,anser14=answer[13],anser15=answer[14],anser16=answer[15],anser17=answer[16]
                                       ,anser18=answer[17],anser19=answer[18],anser20=answer[19],anser21=answer[20]
                                       ,anser22=answer[21], date=timezone.now().strftime("%Y-%m-%d"))
        return HttpResponse('{"data":1}')


def manager_login(request):
    """
        登陆
        :param request:
        :return:
        """
    # 定义空字符串，以便向前端页面提示错误
    s = ''
    # Get请求，返回login.html界面，输入框规则参照制定的User()并实列化
    if request.method == 'GET':
        return render(request, 'manage_login.html')
        #return render(request,"用户管理.htm")
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        print(11111111111)
        u = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = models.ManageInformation.objects.filter(manager_name=u, manager_password=pwd)
        if obj:
            return redirect('/index1/index1.html')
        else:
            s = '''
               <script>alert('该用户名不存在或者密码错误!!!请检查是否正确!!!');</script>
                                    '''
        return render(request, 'manage_login.html', { 's': s})

def index1(request):
    if request.method == 'GET':
        arr = []
        data = {}
        for i in MenunameInformation.objects.all():
            arr.append({
                'menuname': i.menuname,
                'cuisine_field': i.cuisine_field,
                'introduce_field': i.introduce_field
            })
        data = {
            'data': arr
        }
        return render(request, 'index1.html', data)
        # return render(request,"用户管理.htm")
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        u = request.POST.get('menu_name')
        print(u)
        if u:
            models.MenunameInformation.objects.filter(menuname=u).delete()
        else:
            s1 = request.POST.get('name')
            s2 = request.POST.get('cuisine')
            s3 = request.POST.get('describe')
            models.MenunameInformation.objects.create(menuname=s1,cuisine_field =s2,introduce_field=s3)
    return HttpResponse('{"data":1}')

def index_menu(request):
    if request.method == 'GET':
        return render(request, 'index_menu.html')
        # return render(request,"用户管理.htm")
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        if request.method == 'POST':
            if request.FILES.get('photo'):
                new_img = BannerIndex(
                    index_image=request.FILES.get('photo')
                )
                new_img.save()
        s = '''
                       <script>alert('提交成功');</script>
                                            '''
        return render(request, 'index_menu.html', {'s': s})


def index_wj(request):
    if request.method == 'GET':
        arr = []
        data = []
        for obj in models.Question.objects.all():
            if obj.date.strftime("%Y-%m") not in arr:
                arr.append(obj.date.strftime("%Y-%m"))
                data.append({
                    'month': obj.date.strftime("%Y-%m"),
                    'amount': 0
                })
        for obj in models.Question.objects.all():
            if obj.date.strftime("%Y-%m") in arr:
                index = arr.index(obj.date.strftime("%Y-%m"))
                if obj.anser1 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser2 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser3 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser4 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser5 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser6 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser7 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser8 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser9 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser10 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser11 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser12 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser13 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser14 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser15 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser16 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser17 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser18 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser19 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser20 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser21 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;
                if obj.anser22 == '不满意':
                    data[index]['amount'] = data[index]['amount'] + 1;


            else:
                arr.append(obj.date.strftime("%Y-%m"))
                data.append({
                    'month':obj.date.strftime("%Y-%m"),
                    'amount': 0
                })
        print(data)
        return render(request, 'index_wj.html', {'data': data})
    if request.method == 'POST':
        l = models.Request.objects.filter(user='chenxi007')
        print(l[0])
        s = {}
        s.update({'满意':46})
        s.update({'比较满意':34})
        s.update({'一般':10})
        s.update({'不满意':10})
        print(s)
    return HttpResponse(s)

def index_fk(request):
    if request.method == 'GET':
        obj = models.Request.objects.filter(date=timezone.now().strftime("%Y-%m-%d"))
        menus = models.MenunameInformation.objects.all()
        menus_arr = []
        for menu in menus:
            menus_arr.append(menu.menuname)
        print(menus_arr)
        data = []
        for x in menus_arr:
            data.append({
                'name': x,
                'haochi_amount': 0,
                'youdai_amount': 0
            })
        print(data)
        print(len(obj))
        for i in obj:
            for index in range(len(menus_arr)):
                if i.the_most_nice == menus_arr[index]:
                    data[index]['haochi_amount'] = data[index]['haochi_amount'] + 1
                if i.the_demost_dence == menus_arr[index]:
                    data[index]['youdai_amount'] = data[index]['youdai_amount'] + 1
        print(data)
        data = {
            'data':data
        }
        return render(request, 'index_fk.html', data)
    if request.method == 'POST':
        l = models.Request.objects.filter(user='chenxi007')
        print(l[0])
        s = {}
        s.update({'最好吃的：':46})
        s.update({'味道普通的：':34})
        s.update({'今天整體味道：':10})
        s.update({'員工期望：':10})
    return HttpResponse(str(s))


def uploadImg(request):
    if request.method == 'POST':
        if request.FILES.get('photo'):
            new_img = BannerIndex(
                index_image=request.FILES.get('photo')
            )
            new_img.save()
    s = '''
                   <script>alert('提交成功');</script>
                                        '''
    return render(request, 'index_menu.html',{'s':s})


def save_selected_menu(request):
    names = request.POST.get('names')
    login_user = request.POST.get('login_user')
    print (names)
    models.SelectMenu.objects.create(name=names, user=login_user, date=timezone.now().strftime("%Y-%m-%d"))
    return HttpResponse(json.dumps({'success':1}), content_type='application/json')


def check_selectedmenu(request):
    login_user = request.POST.get('login_user')
    print(login_user)
    object = models.SelectMenu.objects.filter(user=login_user).last()
    if object:
        data = {
            'data': object.name
        }
    else:
        data = {}
    return HttpResponse(json.dumps(data), content_type='application/json')


def search_menu(request):
    text = request.POST.get('data')
    print(text)
    menus = models.MenunameInformation.objects.filter(menuname__contains=text)
    arr = []
    for i in menus:
        arr.append({
            'menuname': i.menuname,
            'cuisine_field': i.cuisine_field,
            'introduce_field': i.introduce_field
        })
        data = {
            'data': arr
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


def menu_result(request):
    obj = models.SelectMenu.objects.filter(date=timezone.now().strftime("%Y-%m-%d"))
    arr = []
    key = []
    val = []
    for i in obj:
        menus = i.name.split(',')
        for j in menus:
            if j in key:
                index = key.index(j)
                val[index] = val[index] + 1
            else:
                key.append(j)
                val.append(1)
    print(key)
    print(val)
    print(len(key))
    for index in range(len(key)):
        arr.append({
            'name': key[index],
            'amount': val[index]
        })
    return render(request, 'menu_result.html', {'data':arr})


def chongzhicaidan(request):
    login_user = request.POST.get('login_user')
    print(login_user)
    models.SelectMenu.objects.filter(user=login_user).delete()
    return HttpResponse(json.dumps({'success':1}), content_type='application/json')