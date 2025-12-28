"""Tests for admin functionality."""

from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.utils import timezone
from ..admin import ReadingAdmin, MeterAdmin, MeterPointAdmin, FlowFileAdmin
from ..models import Reading, Meter, MeterPoint, FlowFile


class AdminTests(TestCase):
    """Test admin customizations."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.user = User.objects.create_superuser("admin", "admin@test.com", "password")

        # Create test data
        self.flow_file = FlowFile.objects.create(
            filename="test.uff", file_reference="TEST001"
        )
        self.meter_point = MeterPoint.objects.create(mpan="1234567890123")
        self.meter = Meter.objects.create(
            meter_point=self.meter_point, serial_number="SN12345", meter_type="E"
        )
        self.reading = Reading.objects.create(
            meter=self.meter,
            reading_value=100.5,
            reading_date=timezone.now(),
            reading_type="N",
            flow_file=self.flow_file,
        )

    def test_reading_admin_mpan_display(self):
        """Test MPAN display in reading admin."""
        admin = ReadingAdmin(Reading, self.site)
        result = admin.mpan_display(self.reading)
        self.assertIn("1234567890123", result)

    def test_reading_admin_meter_serial_display(self):
        """Test meter serial display in reading admin."""
        admin = ReadingAdmin(Reading, self.site)
        result = admin.meter_serial_display(self.reading)
        self.assertIn("SN12345", result)

    def test_meter_admin_mpan_display(self):
        """Test MPAN display in meter admin."""
        admin = MeterAdmin(Meter, self.site)
        result = admin.mpan_link(self.meter)
        self.assertIn("1234567890123", result)

    def test_meter_admin_reading_count(self):
        """Test reading count in meter admin."""
        admin = MeterAdmin(Meter, self.site)
        self.assertEqual(admin.reading_count(self.meter), 1)

    def test_meter_point_admin_meter_count(self):
        """Test meter count in meter point admin."""
        admin = MeterPointAdmin(MeterPoint, self.site)
        self.assertEqual(admin.meter_count(self.meter_point), 1)

    def test_meter_point_admin_reading_count(self):
        """Test reading count in meter point admin."""
        admin = MeterPointAdmin(MeterPoint, self.site)
        self.assertEqual(admin.reading_count(self.meter_point), 1)

    def test_flow_file_admin_display(self):
        """Test flow file admin list display."""
        admin = FlowFileAdmin(FlowFile, self.site)
        self.assertIn("filename", admin.list_display)
        self.assertIn("imported_at", admin.list_display)

    def test_flow_file_delete_permission(self):
        """Test FlowFile delete permission is disabled."""
        admin = FlowFileAdmin(FlowFile, self.site)
        request = self.factory.get("/")
        request.user = self.user
        self.assertFalse(admin.has_delete_permission(request, self.flow_file))

    def test_reading_admin_queryset_optimization(self):
        """Test reading admin uses optimized queryset."""
        admin = ReadingAdmin(Reading, self.site)
        request = self.factory.get("/")
        request.user = self.user
        qs = admin.get_queryset(request)
        # Check that select_related is used (queryset has query with select_related)
        self.assertIn("meter_point", str(qs.query))

    def test_reading_admin_flow_file_display(self):
        """Test flow file display in reading admin."""
        admin = ReadingAdmin(Reading, self.site)
        result = admin.flow_file_display(self.reading)
        self.assertIn("test.uff", result)
