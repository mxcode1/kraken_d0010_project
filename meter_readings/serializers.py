"""
API serializers for meter readings app.
Converts model instances to/from JSON.
"""

from rest_framework import serializers

from .models import FlowFile, Meter, MeterPoint, Reading


class FlowFileUploadSerializer(serializers.Serializer):
    """Serializer for D0010 file uploads."""

    file = serializers.FileField()

    def validate_file(self, value):
        """Validate uploaded file."""
        if not value.name.endswith(".uff"):
            raise serializers.ValidationError(
                "Invalid file type. Only .uff files are supported."
            )
        return value


class FlowFileSerializer(serializers.ModelSerializer):
    """Serializer for imported D0010 files."""

    class Meta:
        model = FlowFile
        fields = [
            "id",
            "filename",
            "file_reference",
            "record_count",
            "imported_at",
        ]
        read_only_fields = ["id", "imported_at"]


class MeterPointSerializer(serializers.ModelSerializer):
    """Serializer for meter points (MPANs)."""

    meter_count = serializers.IntegerField(read_only=True)
    reading_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = MeterPoint
        fields = [
            "id",
            "mpan",
            "created_at",
            "updated_at",
            "meter_count",
            "reading_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MeterSerializer(serializers.ModelSerializer):
    """Serializer for meters."""

    mpan = serializers.CharField(source="meter_point.mpan", read_only=True)
    reading_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Meter
        fields = [
            "id",
            "mpan",
            "serial_number",
            "meter_type",
            "created_at",
            "updated_at",
            "reading_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ReadingSerializer(serializers.ModelSerializer):
    """Serializer for meter readings."""

    mpan = serializers.CharField(source="meter.meter_point.mpan", read_only=True)
    meter_serial = serializers.CharField(source="meter.serial_number", read_only=True)
    meter_type = serializers.CharField(source="meter.meter_type", read_only=True)
    flow_filename = serializers.CharField(source="flow_file.filename", read_only=True)

    class Meta:
        model = Reading
        fields = [
            "id",
            "mpan",
            "meter_serial",
            "meter_type",
            "register_id",
            "reading_date",
            "reading_value",
            "reading_type",
            "flow_filename",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ReadingDetailSerializer(ReadingSerializer):
    """Detailed reading serializer with nested meter/meter point."""

    meter = MeterSerializer(read_only=True)
    flow_file = FlowFileSerializer(read_only=True)

    class Meta(ReadingSerializer.Meta):
        fields = ReadingSerializer.Meta.fields + ["meter", "flow_file"]


class MeterPointDetailSerializer(MeterPointSerializer):
    """Detailed meter point with nested meters."""

    meters = MeterSerializer(many=True, read_only=True)

    class Meta(MeterPointSerializer.Meta):
        fields = MeterPointSerializer.Meta.fields + ["meters"]


class ReadingSummarySerializer(serializers.Serializer):
    """Summary statistics for readings."""

    total_readings = serializers.IntegerField()
    total_meter_points = serializers.IntegerField()
    total_meters = serializers.IntegerField()
    date_range = serializers.DictField()
    reading_types = serializers.DictField()
