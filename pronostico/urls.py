from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.ingresar'),
    url(r'^registro/$', 'principal.views.index'),
    url(r'^logout/$', 'principal.views.cerrar'),
    url(r'^dashboard/$', 'principal.views.dashboard'),
    url(r'^pronostico/$', 'principal.views.formpronostico'),
    url(r'^search/$', 'principal.views.searchs'),
    url(r'^viewpronostico/$', 'principal.views.viewpronostico'),
    url(r'^errorpronostico/$', 'principal.views.errorpronostico'),
    url(r'^savepronostico/$', 'principal.views.savepronostico'),
    url(r'^resultado/$', 'principal.views.restotal'),
    url(r'^condiciones/$', 'principal.views.condiciones'),
    #url(r'^usuario/(?P<user_name>\w+)/$', 'principal.views.edituser'),
    url(r'^usuario/(?P<user_name>.*)$', 'principal.views.edituser'),
    url(r'^juegos/detjuego/(?P<id_juego>\d+)/$','principal.views.detjuego'),
    # url(r'^app1/', include('app1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
