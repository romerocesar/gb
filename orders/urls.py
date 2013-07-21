from django.conf.urls import patterns, url
from orders import views

urlpatterns = patterns('',
    url(r'^$', views.menu, name='menu')
)
