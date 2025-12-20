"""URL configuration for meter_readings app."""

from django.urls import path

from . import views

app_name = "meter_readings"

urlpatterns = [
    path("", views.index, name="index"),
]
