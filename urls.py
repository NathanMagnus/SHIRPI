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
     
    (r'^cs215/shirpi/browse/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?$', 'project.SHIRPI.views.browse'),
    (r'^cs215/shirpi/view_profile/(?P<user_name>[^/]+)/?$', 'project.SHIRPI.views.view_profile'),
    
    (r'^cs215/shirpi/add_favourite/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/', 'project.SHIRPI.views.add_favourite'),
    (r'^cs215/shirpi/view_favourites/(?P<user_name>[^/]+)/?$', 'project.SHIRPI.views.view_favourites'),
    (r'^cs215/shirpi/edit_favourites/$', 'project.SHIRPI.views.edit_favourites'),
    (r'^cs215/shirpi/delete_favourite/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.views.delete_favourite'),
    
    (r'^cs215/shirpi/comment/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.views.comment'),
    (r'^cs215/shirpi/edit_comment/(?P<comment_id>\d+)/$', 'project.SHIRPI.views.edit_comment'),
    (r'^cs215/shirpi/view_comments/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?$', 'project.SHIRPI.views.view_comments'),
    (r'^cs215/shirpi/save/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.views.save'),
    (r'^cs215/shirpi/save/(?P<comment_id>\d+)/?', 'project.SHIRPI.views.save_edit'),
    
    (r'^cs215/shirpi/accounts/?', include('registration.urls')),
    (r'^cs215/SHIRPI|shirpi/?', 'project.SHIRPI.views.index') # not catch-all
    #(r'^cs215.+', 'project.SHIRPI.views.index'), # catch all. may or may not want this during development
)
