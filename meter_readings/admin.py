from django.contrib import admin
from .models import FlowFile, MeterPoint, Meter, Reading


@admin.register(FlowFile)
class FlowFileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'file_date', 'record_count', 'imported_at']
    list_filter = ['file_date', 'imported_at']
    search_fields = ['filename']
    readonly_fields = ['imported_at']


@admin.register(MeterPoint)
class MeterPointAdmin(admin.ModelAdmin):
    list_display = ['mpan', 'meter_type', 'created_at']
    list_filter = ['meter_type']
    search_fields = ['mpan']


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'meter_point', 'meter_type', 'installed_date']
    list_filter = ['meter_type', 'installed_date']
    search_fields = ['serial_number', 'meter_point__mpan']


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ['meter', 'reading_date', 'reading_value', 'register_id', 'md_flag']
    list_filter = ['reading_date', 'md_flag']
    search_fields = ['meter__serial_number', 'meter__meter_point__mpan']
    date_hierarchy = 'reading_date'
