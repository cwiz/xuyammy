from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^data/', 'dashboard.views.data'),
    (r'^task/save/', 'dashboard.views.task_save'),
    (r'^update/', 'dashboard.views.update'),
    (r'^admin/', include(admin.site.urls)),
    (r'^', 'dashboard.views.index'),
)
