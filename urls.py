from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^data/', 'dashboard.views.data'),
    (r'^add_task/', 'dashboard.views.add_task'),
    (r'^update/', 'dashboard.views.update'),
    (r'^admin/', include(admin.site.urls)),
    (r'^', 'dashboard.views.index'),
)
