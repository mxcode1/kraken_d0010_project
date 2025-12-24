"""
API views for meter readings.
Provides REST endpoints for querying meter data.
"""

import os
import tempfile
from typing import Any, Dict, Optional, Type

from django.core.management import call_command
from django.db.models import Count, Max, Min, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import FlowFile, Meter, MeterPoint, Reading
from .serializers import (
    FlowFileSerializer,
    FlowFileUploadSerializer,
    MeterPointDetailSerializer,
    MeterPointSerializer,
    MeterSerializer,
    ReadingDetailSerializer,
    ReadingSerializer,
    ReadingSummarySerializer,
)


class FlowFileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing imported D0010 files.

    List all imported files with their metadata.
    """

    queryset = FlowFile.objects.all().order_by("-imported_at")
    serializer_class = FlowFileSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["imported_at"]
    search_fields = ["filename", "file_reference"]
    ordering_fields = ["imported_at", "filename", "record_count"]
    ordering = ["-imported_at"]

    @extend_schema(
        summary="List all imported D0010 flow files",
        description=(
            "Retrieve a list of all imported D0010 flow files with metadata "
            "including filename, record count, and import timestamp."
        ),
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get details for a specific flow file",
        description=(
            "Retrieve detailed information about a specific "
            "imported D0010 flow file."
        ),
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Upload a D0010 file",
        description=(
            "Upload and import a D0010 .uff file. The file will be "
            "validated and imported into the system."
        ),
        request=FlowFileUploadSerializer,
        responses={
            201: FlowFileSerializer,
            400: {"description": "Invalid file or import error"},
        },
    )
    @action(detail=False, methods=["post"])
    def upload(self, request: Request) -> Response:
        """Upload and import a D0010 file."""
        serializer = FlowFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["file"]

        # Save uploaded file to temporary location with original filename
        temp_dir = tempfile.gettempdir()
        tmp_file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(tmp_file_path, "wb") as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)

        try:
            # Call the import command
            call_command("import_d0010", tmp_file_path)

            # Get the imported flow file (most recent with this filename)
            flow_file = (
                FlowFile.objects.filter(filename=uploaded_file.name)
                .order_by("-imported_at")
                .first()
            )

            if flow_file:
                return Response(
                    FlowFileSerializer(flow_file).data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "File imported but not found in database"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Import failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)


class MeterPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing meter points (MPANs).

    Retrieve:
    - List all meter points
    - Get details for a specific MPAN
    - Filter by MPAN pattern

    Custom Actions:
    - `/api/v1/meter-points/{id}/readings/` - Get all readings for a meter point
    """

    queryset = MeterPoint.objects.annotate(
        meter_count=Count("meters", distinct=True),
        reading_count=Count("meters__readings", distinct=True),
    ).order_by("mpan")

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["mpan"]
    ordering_fields = ["mpan", "created_at", "meter_count", "reading_count"]
    ordering = ["mpan"]

    def get_serializer_class(self) -> Type[Serializer]:
        """Use detailed serializer for retrieve action."""
        if self.action == "retrieve":
            return MeterPointDetailSerializer
        return MeterPointSerializer

    @extend_schema(
        summary="List all meter points (MPANs)",
        description=(
            "Retrieve a list of all meter points with counts of "
            "associated meters and readings."
        ),
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get details for a specific meter point",
        description=(
            "Retrieve detailed information about a meter point "
            "including all associated meters."
        ),
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Get all readings for a meter point",
        responses={200: ReadingSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def readings(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get all readings for this meter point."""
        meter_point: MeterPoint = self.get_object()
        readings: QuerySet[Reading] = (
            Reading.objects.filter(meter__meter_point=meter_point)
            .select_related("meter__meter_point", "flow_file")
            .order_by("-reading_date")
        )

        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)


class MeterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing meters.

    Retrieve:
    - List all meters
    - Get details for a specific meter
    - Filter by serial number, MPAN, or meter type

    Custom Actions:
    - `/api/v1/meters/{id}/readings/` - Get all readings for a meter
    """

    queryset = (
        Meter.objects.select_related("meter_point")
        .annotate(reading_count=Count("readings"))
        .order_by("meter_point__mpan", "serial_number")
    )

    serializer_class = MeterSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["meter_type", "meter_point__mpan"]
    search_fields = ["serial_number", "meter_point__mpan"]
    ordering_fields = ["serial_number", "meter_type", "created_at", "reading_count"]
    ordering = ["meter_point__mpan", "serial_number"]

    @extend_schema(
        summary="List all meters",
        description=(
            "Retrieve a list of all meters with their serial numbers, "
            "types, and reading counts."
        ),
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get details for a specific meter",
        description=(
            "Retrieve detailed information about a specific meter "
            "including its MPAN and reading count."
        ),
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Get all readings for a meter",
        responses={200: ReadingSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def readings(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get all readings for this meter."""
        meter: Meter = self.get_object()
        readings: QuerySet[Reading] = (
            Reading.objects.filter(meter=meter)
            .select_related("flow_file")
            .order_by("-reading_date")
        )

        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)


class ReadingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing meter readings.

    Retrieve:
    - List all readings (paginated)
    - Get details for a specific reading
    - Filter by MPAN, date range, reading type, meter type
    - Search by MPAN or meter serial

    Query Parameters:
    - `mpan` - Filter by MPAN (exact match)
    - `meter_serial` - Filter by meter serial number
    - `reading_type` - Filter by reading type
    - `meter_type` - Filter by meter type
    - `date_from` - Readings from this date onwards
    - `date_to` - Readings up to this date
    - `search` - Search in MPAN or serial number
    - `ordering` - Order by field (e.g., `-reading_date`)

    Custom Actions:
    - `/api/v1/readings/summary/` - Get summary statistics
    """

    queryset = Reading.objects.select_related(
        "meter__meter_point", "meter", "flow_file"
    ).order_by("-reading_date")

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["reading_type", "register_id", "meter__meter_type"]
    search_fields = [
        "meter__meter_point__mpan",
        "meter__serial_number",
        "flow_file__filename",
    ]
    ordering_fields = ["reading_date", "reading_value", "created_at"]
    ordering = ["-reading_date"]

    def get_serializer_class(self) -> Type[Serializer]:
        """Use detailed serializer for retrieve action."""
        if self.action == "retrieve":
            return ReadingDetailSerializer
        return ReadingSerializer

    @extend_schema(
        summary="List all meter readings",
        description=(
            "Retrieve a paginated list of all meter readings. Supports "
            "filtering by MPAN, date range, reading type, and meter type."
        ),
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get details for a specific reading",
        description=(
            "Retrieve detailed information about a specific meter reading "
            "including nested meter and flow file data."
        ),
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Reading]:
        """Filter queryset by query parameters."""
        queryset: QuerySet[Reading] = super().get_queryset()

        # Filter by MPAN
        mpan: Optional[str] = self.request.query_params.get("mpan")
        if mpan:
            queryset = queryset.filter(meter__meter_point__mpan=mpan)

        # Filter by meter serial
        meter_serial: Optional[str] = self.request.query_params.get("meter_serial")
        if meter_serial:
            queryset = queryset.filter(meter__serial_number=meter_serial)

        # Filter by date range
        date_from: Optional[str] = self.request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(reading_date__gte=date_from)

        date_to: Optional[str] = self.request.query_params.get("date_to")
        if date_to:
            queryset = queryset.filter(reading_date__lte=date_to)

        return queryset

    @extend_schema(
        summary="Get summary statistics for readings",
        responses={200: ReadingSummarySerializer()},
    )
    @action(detail=False, methods=["get"])
    def summary(self, request: Request) -> Response:
        """
        Get summary statistics for all readings.

        Returns total counts, date range, and breakdown by reading type.
        """
        readings: QuerySet[Reading] = self.get_queryset()

        # Aggregate statistics
        stats: Dict[str, Any] = readings.aggregate(
            total_readings=Count("id"),
            total_meter_points=Count("meter__meter_point", distinct=True),
            total_meters=Count("meter", distinct=True),
            earliest_reading=Min("reading_date"),
            latest_reading=Max("reading_date"),
        )

        # Count by reading type
        reading_types: Dict[str, int] = {}
        type_counts = readings.values("reading_type").annotate(count=Count("id"))
        for item in type_counts:
            reading_types[item["reading_type"]] = item["count"]

        summary: Dict[str, Any] = {
            "total_readings": stats["total_readings"],
            "total_meter_points": stats["total_meter_points"],
            "total_meters": stats["total_meters"],
            "date_range": {
                "earliest": stats["earliest_reading"],
                "latest": stats["latest_reading"],
            },
            "reading_types": reading_types,
        }

        serializer = ReadingSummarySerializer(summary)
        return Response(serializer.data)
