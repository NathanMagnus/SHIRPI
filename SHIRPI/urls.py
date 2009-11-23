from django.conf.urls.defaults import *
import  project.SHIRPI

urlpatterns = patterns('',
    (r'^browse/?(?P<restaurant_name>[^/]+)?/?(?P<restaurant_address>[^/]+)?/?$', 'project.SHIRPI.views.browse'),
    (r'^view/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?$', 'project.SHIRPI.views.view_restaurant'),
    (r'^(?P<api_flag>api)/?(?P<restaurant_name>[^/]+)?/?(?P<restaurant_address>[^/]+)?/?$', 'project.SHIRPI.views.browse'),
    
    (r'^view_profile/(?P<user_name>[^/]+)/?$', 'project.SHIRPI.views.view_profile'),
    (r'^edit_profile/?', 'project.SHIRPI.views.edit_profile'),
    
    (r'^add_favourite/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.favourite_views.add_favourite'),
    (r'^view_favourites/(?P<user_name>[^/]+)/?$', 'project.SHIRPI.favourite_views.view_favourites'),
    (r'^edit_favourites/?$', 'project.SHIRPI.favourite_views.edit_favourites'),
    (r'^delete_favourite/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.favourite_views.delete_favourite'),
    
    (r'^comment/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.comment_views.comment'),
    (r'^edit_comment/(?P<comment_id>\d+)/$', 'project.SHIRPI.comment_views.edit_comment'),
    (r'^view_comments/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?$', 'project.SHIRPI.comment_views.view_comments'),
    (r'^save/(?P<restaurant_name>[^/]+)/(?P<restaurant_address>[^/]+)/?', 'project.SHIRPI.comment_views.save'),
    (r'^save/(?P<comment_id>\d+)/?', 'project.SHIRPI.comment_views.save_edit'),
    (r'^delete_comment/(?P<comment_id>\d+)/?', 'project.SHIRPI.comment_views.delete_comment'),
    
    (r'^accounts/?', include('registration.urls')),
    (r'$', 'project.SHIRPI.views.index')
    
)