from django.conf.urls import patterns, url

from comedi import views

urlpatterns = patterns( '',
    url( r'^$', views.index, name = 'index' ),
    url( r'^test', views.index_loggedIn, name = 'index_loggedIn' ),
    url( r'^dyn_form', views.dyn_form, name = 'dyn_form' ),
    url( r'^ajax_getSubFamilyNameFromFamily', views.ajax_getSubFamilyNameFromFamily, name = 'ajax_getSubFamilyNameFromFamily' ),
    url( r'^ajax_getProductNamesFromSubFamily', views.ajax_getProductNamesFromSubFamily, name = 'ajax_getProductNamesFromSubFamily' ),
    url( r'^ajax_productAutocomplete', views.ajax_productAutocomplete, name = 'ajax_productAutocomplete' ),

#     url( r'^logout', views.logout_view, {'next_page': 'comedi/'}, name = 'logout' ),
 )
