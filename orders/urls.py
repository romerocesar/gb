from django.conf.urls import patterns, url
from orders import views

urlpatterns = patterns('',
    url(r'^client/(\w+)/menu$', views.menu, name='menu'),
    url(r'^menu/(\w+)/(.+)/(.+)$', views.section, name='section'),
    url(r'^manager/(\w+)$', views.managerview),
    url(r'^item/(\w+)$', views.item, name='item'),
    url(r'^order/item/(\w+)/client/(\w+)$', views.place_order, name='order'),
    url(r'^orders/(\w+)$', views.list_orders, name='orders'),
)
