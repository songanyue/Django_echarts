"""map URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import mapper.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', mapper.views.home),
    path('admin/', admin.site.urls),
    path('home/', mapper.views.home),
    path('select_Country_with_type/', mapper.views.select_Country_with_type),
    path('select_Country_with_relation/', mapper.views.select_Country_with_relation),
    path('select_Country/', mapper.views.select_Country),
    path('tune/', mapper.views.tune),
    path('map1/', mapper.views.map1),
    path('map2/', mapper.views.map2),
    path('map3D/', mapper.views.map3D),
    path('aid/', mapper.views.aid),
    path('select_aid/', mapper.views.select_aid)
]