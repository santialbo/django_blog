from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.blog'),
    url(r'^blog/((?P<page>[+-]?\d+)/)?$', 'blog.views.blog'),

    url(r'^blog/entry/(?P<entry_id>\d+)/$', 'blog.views.entry'),
    url(r'^blog/entry/(?P<entry_id>\d+)/comment/$', 'blog.views.post_comment'),
    url(r'^blog/author/(?P<author_name>[^/]+)/((?P<page>[+-]?\d+)/)?$', 'blog.views.author'),
    url(r'^blog/tag/(?P<tag_name>[^/]+)/((?P<page>[+-]?\d+)/)?$', 'blog.views.tag'),

    url(r'^blog/search/$', 'blog.views.search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
