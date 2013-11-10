from django.conf.urls import patterns, url
from orders import views

urlpatterns = patterns('',
    url(r'^client/(\w+)/seat/(\w+)$', views.init_session),
    url(r'^item/(\w+)$', views.item, name='item'),
    url(r'^manager/(\w+)/items$', views.manager_items),
    url(r'^manager/(\w+)/menus$', views.manager_menus),
    url(r'^menu$', views.back_to_menu, name='back_to_menu'),
    url(r'^menu/(\w+)/(.+)$', views.menu, name='menu'),
    url(r'^menu/(\w+)/(.+)/(.+)$', views.section, name='section'),
    url(r'^myorders$', views.myorders, name='myorders'),
    url(r'^myorders/bill$', views.bill, name='mybill'),
    url(r'^order/item/(\w+)/client/(\w+)$', views.place_order, name='order'),
    url(r'^order/(\w+)$', views.order, name='order_details'),
    url(r'^order/(\w+)/cancel$', views.cancel_order, name='cancel_order'),
    url(r'^order/(\w+)/update$', views.update_order, name='update_order'),
    url(r'^orders/filter$', views.filter_orders, name='filter_orders'),
    url(r'^orders/(\w+)$', views.list_orders, name='orders'),
)
