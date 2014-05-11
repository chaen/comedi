from django.conf.urls import patterns, url

from comedi import views

urlpatterns = patterns( '',
    url( r'^$', views.index, name = 'index' ),
    url( r'^test', views.index_loggedIn, name = 'index_loggedIn' ),
    url( r'^dyn_form$', views.dyn_form, name = 'dyn_form' ),
#     url( r'^dyn_form_result/(?P<product_name>[a-zA-Z0-9]+)', views.dyn_form_result, name = 'dyn_form_result' ),
#     url( r'^dyn_form_result$', views.dyn_form_result, name = 'dyn_form_result' ),
    url( r'^dyn_form_result$', views.dyn_form_result2.as_view(), name = 'dyn_form_result' ),
#     url( r'^dyn_form_result/page(?P<page>[0-9]+)$', views.dyn_form_result2.as_view(), name = 'dyn_form_result' ),
    url( r'^ajax_getSubFamilyNamesFromFamily', views.ajax_getSubFamilyNamesFromFamily, name = 'ajax_getSubFamilyNamesFromFamily' ),
    url( r'^ajax_getProductNamesFromSubFamily', views.ajax_getProductNamesFromSubFamily, name = 'ajax_getProductNamesFromSubFamily' ),
    url( r'^ajax_productAutocomplete', views.ajax_productAutocomplete, name = 'ajax_productAutocomplete' ),

    url( r'^order/search$', views.orderSearch_view, name = 'order_search' ),
    url( r'^order/list$', views.orderList_view.as_view(), name = 'order_list' ),
    url( r'^order/detail/(?P<pk>\d+)$', views.orderDetail_view.as_view(), name = 'order_detail' ),
    url( r'^ajax_clientAutocomplete', views.Ajax.ajax_clientAutocomplete, name = 'ajax_clientAutocomplete' ),
#     url( r'^logout', views.logout_view, {'next_page': 'comedi/'}, name = 'logout' ),
 )

