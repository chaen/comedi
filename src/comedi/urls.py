from django.conf.urls import patterns, url

from comedi import views

urlpatterns = patterns( '',
    url( r'^$', views.index, name = 'index' ),
    url( r'^test', views.index_loggedIn, name = 'index_loggedIn' ),
#     url( r'^logout', views.logout_view, {'next_page': 'comedi/'}, name = 'logout' ),
 )
