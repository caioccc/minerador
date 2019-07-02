"""minerproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from minerador.views import IndexView, OrderListJson, ProductDetailView, ListBestView, ListBestJson

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^my/datatable/data/$', OrderListJson.as_view(), name='order_list_json'),
    url(r'^list/best/$', ListBestView.as_view(), name='list_best'),
    url(r'^best/datatable/data/$', ListBestJson.as_view(), name='best_list_json'),

]
