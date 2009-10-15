from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from hello.admin import *
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^cs215/admin/', include(admin.site.urls)),
    (r'^cs215/hello/$', 'project.hello.views.index'),
    (r'^cs215/hello/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    (r'^cs215/hello/browse/(?P<rest_name>[^/]+)', 'project.hello.views.browse'),
    (r'^cs215/hello/comment/(?P<rest_name>[^/]+)', 'project.hello.views.comment'),
    (r'^cs215/hello/save/(?P<rest_name>[^/]+)', 'project.hello.views.save'),
    (r'^cs215/hello/register/$', 'project.hello.views.register'),
    (r'^cs215/hello/logout/$', 'project.hello.views.logout'),
    (r'^cs215/hello/profile/(?P<user_name>[^/]+)/edit_favourites/$', 'project.hello.views.edit_favourites'),
    (r'^cs215/hello/profile/(?P<user_name>[^/]+)/$', 'project.hello.views.userProfile'),
    (r'^cs215/hello/edit_comment/(?P<comment_id>\d+)/$', 'project.hello.views.edit_comment'),
#   (r'^cs215/hello/save_edit_comment/(?P<comment_id>\d+)/$', 'project.hello.views.save_edit_comment'),
)
