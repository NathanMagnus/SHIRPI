from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^cs215/admin/', include(admin.site.urls)),
    (r'^cs215/shirpi/?', include('project.SHIRPI.urls')),
    

    (r'^cs215/populate/', 'project.populateDB.views.populate'),

    (r'^cs215/shirpi/accounts/?', include('registration.urls')),
    #(r'^cs215/SHIRPI|shirpi/?', 'project.SHIRPI.views.index') # not catch-all
)
