from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'books.views.index'),
	url(r'brooks/$', 'books.views.brooks'),
    url(r'register/$', 'books.views.register'),
	url(r'login/$', login, {'template_name': 'login.html'}),
	url(r'logout/$', logout, {'next_page': '/'}),
    url(r'brook/(?P<brook_id>\d+)/$', 'books.views.brook'),
    url(r'brook/add_brook/$', 'books.views.add_brook'),
    url(r'brook/add_quote/(?P<brook_id>\d+)/$', 'books.views.add_quote'),
    url(r'brook/add_note/(?P<brook_id>\d+)/$', 'books.views.add_note'),
    url(r'brook/add_review/(?P<brook_id>\d+)/$', 'books.views.add_review'),
    url(r'brook/edit_review/(?P<brook_id>\d+)/$', 'books.views.edit_review'),
    url(r'brook/change_dates/(?P<brook_id>\d+)/$', 'books.views.change_brook_dates'),
    # Examples:
    # url(r'^$', 'booklog.views.home', name='home'),
    # url(r'^booklog/', include('booklog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
