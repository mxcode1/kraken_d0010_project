"""
API URL routing for meter readings.
"""

from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from .api_views import FlowFileViewSet, MeterPointViewSet, MeterViewSet, ReadingViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r"flow-files", FlowFileViewSet, basename="flowfile")
router.register(r"meter-points", MeterPointViewSet, basename="meterpoint")
router.register(r"meters", MeterViewSet, basename="meter")
router.register(r"readings", ReadingViewSet, basename="reading")

urlpatterns = [
    # API endpoints
    path("", include(router.urls)),
    # API documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
