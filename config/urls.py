"""
URL configuration for config.
"""

from django.contrib import admin
from django.urls import path, include
from meter_readings.admin_views import testing_dashboard

urlpatterns = [
    path("admin/testing/", testing_dashboard, name="testing_dashboard"),
    path("admin/", admin.site.urls),
    path("api/", include("meter_readings.api_urls")),
    path("", include("meter_readings.urls")),
]
