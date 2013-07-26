from django.conf.urls import patterns, url
from orders import views

urlpatterns = patterns('',
    url(r'^menu/(\d+)$', views.menu, name='menu'),
    url(r'^dish/(\d+)$', views.dish, name='dish'),
)
