from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('kdd_matcher.views',
    url(r'^$','index'),
    url(r'^match$','match'),
    #url(r'^(?P<affiliation>.+)/(?P<name>.+)/(?P<interest>.+)/results/$','results'),
    url(r'^results/$','results'),
    # Examples:
    # url(r'^$', 'matcher.views.home', name='home'),
    # url(r'^matcher/', include('matcher.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
