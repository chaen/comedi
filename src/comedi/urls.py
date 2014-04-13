from django.conf.urls import patterns, url

from comedi import views

urlpatterns = patterns( '',
    url( r'^$', views.index, name = 'index' ),
    url( r'^test', views.index_loggedIn, name = 'index_loggedIn' ),
    url( r'^dyn_form', views.dyn_form, name = 'dyn_form' ),
    url( r'^list_subFamilies', views.list_subFamilies, name = 'list_subFamilies' ),

#     url( r'^logout', views.logout_view, {'next_page': 'comedi/'}, name = 'logout' ),
 )
