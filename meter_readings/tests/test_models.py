"""Unit tests for meter readings models."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from decimal import Decimal
from meter_readings.models import MeterPoint, Meter, Reading, FlowFile


class MeterPointModelTest(TestCase):
    def test_valid_mpan_creation(self):
        """Test creating a valid meter point with 13-digit MPAN."""
        mp = MeterPoint.objects.create(mpan="1234567890123")
        self.assertEqual(mp.mpan, "1234567890123")
        self.assertEqual(str(mp), "MPAN: 1234567890123")

    def test_invalid_mpan_length(self):
        """Test MPAN validation rejects invalid length."""
        with self.assertRaises(ValidationError):
            mp = MeterPoint(mpan="12345")
            mp.full_clean()

    def test_mpan_uniqueness(self):
        """Test MPAN uniqueness constraint."""
        MeterPoint.objects.create(mpan="1234567890123")
        with self.assertRaises(IntegrityError):
            MeterPoint.objects.create(mpan="1234567890123")


class MeterModelTest(TestCase):
    def setUp(self):
        self.meter_point = MeterPoint.objects.create(mpan="1234567890123")

    def test_valid_meter_creation(self):
        """Test creating a meter with valid serial number and type."""
        meter = Meter.objects.create(
            meter_point=self.meter_point, serial_number="ABC123456", meter_type="S"
        )
        self.assertEqual(meter.serial_number, "ABC123456")
        self.assertEqual(str(meter), "ABC123456 (1234567890123)")


class ReadingModelTest(TestCase):
    def setUp(self):
        self.meter_point = MeterPoint.objects.create(mpan="1234567890123")
        self.meter = Meter.objects.create(
            meter_point=self.meter_point, serial_number="ABC123456"
        )
        self.flow_file = FlowFile.objects.create(
            filename="test.uff", file_reference="TEST001"
        )

    def test_valid_reading_creation(self):
        """Test creating a reading with valid data and relationships."""
        reading = Reading.objects.create(
            meter=self.meter,
            flow_file=self.flow_file,
            register_id="S",
            reading_date=timezone.now(),
            reading_value=Decimal("12345.678"),
        )
        self.assertEqual(reading.reading_value, Decimal("12345.678"))
        self.assertEqual(reading.mpan, "1234567890123")
        self.assertEqual(reading.meter_serial, "ABC123456")

    def test_negative_reading_validation(self):
        """Test that negative reading values are rejected."""
        with self.assertRaises(ValidationError):
            reading = Reading(
                meter=self.meter,
                flow_file=self.flow_file,
                register_id="S",
                reading_date=timezone.now(),
                reading_value=Decimal("-100.0"),
            )
            reading.full_clean()

    def test_flow_file_str(self):
        """Test FlowFile string representation."""
        str_repr = str(self.flow_file)
        self.assertIn("test.uff", str_repr)
        self.assertIn("imported", str_repr)

    def test_meter_clean_empty_serial(self):
        """Test meter clean method with empty serial."""
        meter = Meter(meter_point=self.meter_point, serial_number="  ", meter_type="S")
        with self.assertRaises(ValidationError):
            meter.clean()

    def test_meter_str(self):
        """Test Meter string representation."""
        str_repr = str(self.meter)
        self.assertIn(self.meter.serial_number, str_repr)
        self.assertIn(self.meter_point.mpan, str_repr)

    def test_reading_str(self):
        """Test Reading string representation."""
        reading = Reading.objects.create(
            meter=self.meter,
            flow_file=self.flow_file,
            register_id="S",
            reading_date=timezone.now(),
            reading_value=Decimal("100.5"),
        )
        str_repr = str(reading)
        self.assertIn(self.meter_point.mpan, str_repr)
        self.assertIn(self.meter.serial_number, str_repr)
        self.assertIn("100.5", str_repr)
