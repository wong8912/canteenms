"""image_recongnize URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from photo_one import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('index/index.html', views.index),
    path('index/menu.html',views.menu),
    path('index/information.html',views.information),
    path('index/contact.html',views.contact),
    path('index/questionnaire.html',views.question),
    path('manage_login/',views.manager_login),
    path('index1/', views.index1),
    path('index1/index_menu.html',views.index_menu),
    path('index1/index1.html',views.index1),
    path('index1/index_wj.html',views.index_wj),
    path('index1/menu_result.html',views.menu_result),
    path('index1/index_fk.html',views.index_fk),
    path('uploadImg/', views.uploadImg),
    path('save_selected_menu', views.save_selected_menu),
    path('check_selectedmenu', views.check_selectedmenu),
    path('search_menu', views.search_menu),
    path('chongzhicaidan', views.chongzhicaidan)
#    path('register1',views.register),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
