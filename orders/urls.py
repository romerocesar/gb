from django.conf.urls import patterns, url
from orders import views

urlpatterns = patterns('',
    url(r'^client/(\w+)/seat/(\w+)$', views.menu, name='menu'),
    url(r'^manager/(\w+)$', views.managerview),
    url(r'^menu/(\w+)/(.+)/(.+)$', views.section, name='section'),
    url(r'^myorders/(\w+)$', views.myorders, name='myorders'),    
    url(r'^item/(\w+)$', views.item, name='item'),
    url(r'^order/item/(\w+)/client/(\w+)$', views.place_order, name='order'),
    url(r'^order/(\w+)$', views.order, name='order_details'),
    url(r'^order/(\w+)/update$', views.update_order, name='update_order'),
    url(r'^orders/(\w+)$', views.list_orders, name='orders'),
)
