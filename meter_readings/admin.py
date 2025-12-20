"""Django admin configuration for meter readings models."""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import FlowFile, Meter, MeterPoint, Reading


class MeterInline(admin.TabularInline):
    model = Meter
    extra = 0
    readonly_fields = ["created_at", "updated_at"]
    fields = ["serial_number", "meter_type", "created_at", "updated_at"]


class ReadingInline(admin.TabularInline):
    model = Reading
    extra = 0
    readonly_fields = ["created_at"]
    fields = [
        "register_id",
        "reading_date",
        "reading_value",
        "reading_type",
        "flow_file",
        "created_at",
    ]
    ordering = ["-reading_date"]


@admin.register(FlowFile)
class FlowFileAdmin(admin.ModelAdmin):
    list_display = ["filename", "file_reference", "record_count", "imported_at"]
    list_filter = ["imported_at"]
    search_fields = ["filename", "file_reference"]
    readonly_fields = ["imported_at"]
    ordering = ["-imported_at"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MeterPoint)
class MeterPointAdmin(admin.ModelAdmin):
    list_display = ["mpan", "meter_count", "reading_count", "created_at"]
    search_fields = ["mpan"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [MeterInline]
    ordering = ["mpan"]

    def meter_count(self, obj):
        return obj.meters.count()

    meter_count.short_description = "Meters"

    def reading_count(self, obj):
        return sum(meter.readings.count() for meter in obj.meters.all())

    reading_count.short_description = "Total Readings"


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = [
        "serial_number",
        "mpan_link",
        "meter_type",
        "reading_count",
        "created_at",
    ]
    list_filter = ["meter_type", "created_at"]
    search_fields = ["serial_number", "meter_point__mpan"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ReadingInline]
    ordering = ["meter_point__mpan", "serial_number"]

    def mpan_link(self, obj):
        url = reverse(
            "admin:meter_readings_meterpoint_change", args=[obj.meter_point.pk]
        )
        return format_html('<a href="{}">{}</a>', url, obj.meter_point.mpan)

    mpan_link.short_description = "MPAN"

    def reading_count(self, obj):
        return obj.readings.count()

    reading_count.short_description = "Readings"


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    """Main admin interface for readings with advanced search capabilities."""

    list_display = [
        "mpan_display",
        "meter_serial_display",
        "register_id",
        "reading_value",
        "reading_date",
        "reading_type",
        "flow_file_display",
        "created_at",
    ]
    list_filter = [
        "reading_type",
        "register_id",
        "reading_date",
        "meter__meter_type",
        "flow_file",
    ]
    search_fields = [
        "meter__meter_point__mpan",  # Search by MPAN
        "meter__serial_number",  # Search by meter serial number
        "flow_file__filename",  # Search by filename
    ]
    readonly_fields = ["created_at"]
    ordering = ["-reading_date"]
    date_hierarchy = "reading_date"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("meter__meter_point", "flow_file")
        )

    def mpan_display(self, obj):
        url = reverse(
            "admin:meter_readings_meterpoint_change", args=[obj.meter.meter_point.pk]
        )
        return format_html('<a href="{}">{}</a>', url, obj.meter.meter_point.mpan)

    mpan_display.short_description = "MPAN"
    mpan_display.admin_order_field = "meter__meter_point__mpan"

    def meter_serial_display(self, obj):
        url = reverse("admin:meter_readings_meter_change", args=[obj.meter.pk])
        return format_html('<a href="{}">{}</a>', url, obj.meter.serial_number)

    meter_serial_display.short_description = "Meter Serial"
    meter_serial_display.admin_order_field = "meter__serial_number"

    def flow_file_display(self, obj):
        url = reverse("admin:meter_readings_flowfile_change", args=[obj.flow_file.pk])
        return format_html('<a href="{}">{}</a>', url, obj.flow_file.filename)

    flow_file_display.short_description = "Source File"
    flow_file_display.admin_order_field = "flow_file__filename"
