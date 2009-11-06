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
    #(r'^cs215/hello/register/$', 'project.hello.views.register'),
    #(r'^cs215/hello/profile/(?P<user_name>[^/]+)/edit_favourites/$', 'project.hello.views.edit_favourites'),
    #(r'^cs215/hello/profile/(?P<user_name>[^/]+)/$', 'project.hello.views.userProfile'),
    #(r'^cs215/hello/edit_comment/(?P<comment_id>\d+)/$', 'project.hello.views.edit_comment'),
    (r'^cs215/populateDB/(?P<password>[^/]+)/$', 'project.populateDB.views.populate'),
    (r'^cs215/kwiki/(?P<page_name>[^/]+)/edit/$', 'project.kwiki.views.edit_page'),
    (r'^cs215/kwiki/(?P<page_name>[^/]+)/save/$', 'project.kwiki.views.save_page'),
    (r'^cs215/kwiki/(?P<page_name>[^/]+)/$', 'project.kwiki.views.view_page'),

    (r'^cs215/SHIRPI/$', 'project.SHIRPI.views.index'),
    (r'^cs215/shirpi/$', 'project.SHIRPI.views.index'),
    (r'^cs215/SHIRPI/browse/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/$', 'project.SHIRPI.views.browse'),
    (r'^cs215/SHIRPI/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    (r'^cs215/SHIRPI/logout/$', 'project.SHIRPI.views.logout'),
    (r'^cs215/SHIRPI/comment/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/', 'project.SHIRPI.views.comment'),
    (r'^cs215/SHIRPI/save/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/', 'project.SHIRPI.views.save'),
    (r'^cs215/SHIRPI/save/(?P<comment_id>\d+)/', 'project.SHIRPI.views.save_edit'),
    (r'^cs215/SHIRPI/add_favourite/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/', 'project.SHIRPI.views.add_favourite'),
    (r'^cs215/SHIRPI/browse/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)$', 'project.SHIRPI.views.browse'),
    (r'^cs215/SHIRPI/view_favourites/(?P<user_name>[^/]+)/$', 'project.SHIRPI.views.view_favourites'),
    (r'^cs215/SHIRPI/view_profile/(?P<user_name>[^/]+)/$', 'project.SHIRPI.views.view_profile'),
    (r'^cs215/SHIRPI/edit_comment/(?P<comment_id>\d+)/$', 'project.SHIRPI.views.edit_comment'),
    (r'^cs215/SHIRPI/view_comments/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/$', 'project.SHIRPI.views.view_comments'),
    (r'^cs215/SHIRPI/edit_favourites/$', 'project.SHIRPI.views.edit_favourites'),
    (r'^cs215/SHIRPI/delete_favourite/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/', 'project.SHIRPI.views.delete_favourite'),
    
    (r'^cs215/SHIRPI/', include('registration.urls')),
)
