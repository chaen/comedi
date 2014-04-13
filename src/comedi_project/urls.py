from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comedi_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url( r'^comedi/', include( 'comedi.urls' ) ),

    # The login page
    url( r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'comedi/login.html'} ),
    ( r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/comedi'} )

)
