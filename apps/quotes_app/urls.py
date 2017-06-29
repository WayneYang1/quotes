from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^quotes$', views.quotes, name='quotes'),
    url(r'^add$', views.add, name='add'),
    url(r'^favorite/(?P<quote_id>\d)$', views.favorite, name='favorite'),
    url(r'^unfavorite/(?P<quote_id>\d)$', views.unfavorite, name='unfavorite'),
    url(r'^users/(?P<user_id>\d+)$', views.user, name='user'),
    url(r'^logout$', views.logout, name='logout')
]