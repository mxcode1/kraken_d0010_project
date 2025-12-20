"""Tests for dashboard views."""

from django.test import TestCase, Client
from meter_readings.models import FlowFile, MeterPoint, Meter, Reading
from django.utils import timezone


class ViewsTest(TestCase):
    """Test dashboard views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

        # Create test data
        self.flow_file = FlowFile.objects.create(filename="test.uff")
        self.meter_point = MeterPoint.objects.create(mpan="1234567890123")
        self.meter = Meter.objects.create(
            meter_point=self.meter_point, serial_number="SN123", meter_type="S"
        )
        self.reading = Reading.objects.create(
            meter=self.meter,
            reading_value=100.5,
            reading_date=timezone.now(),
            reading_type="N",
            flow_file=self.flow_file,
        )

    def test_index_view(self):
        """Test index view renders with correct counts."""
        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kraken Energy D0010 System")
        self.assertContains(response, "1")  # Check counts appear
