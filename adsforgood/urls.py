from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^projectify/', include('apps.users.urls')),
    re_path(r'^projectify/', include('apps.projects.urls')),
    re_path(r'^projectify/', include('apps.reports.urls'))

]
