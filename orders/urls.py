from django.conf.urls import patterns, url
from orders import views

urlpatterns = patterns('',
    url(r'^client/(\d+)/menu$', views.menu, name='menu'),
    url(r'^menu/(\w+)/(\d+)$', views.section, name='section'),
    url(r'^item/(\w+)$', views.dish, name='item'),
)
