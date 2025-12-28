"""Tests for custom exception classes."""

from django.test import TestCase
from meter_readings.exceptions import (
    MeterPointNotFoundError,
    MeterNotFoundError,
)


class ExceptionTests(TestCase):
    """Test custom exception classes."""

    def test_meter_point_not_found_error(self):
        """Test MeterPointNotFoundError initialization."""
        error = MeterPointNotFoundError(
            mpan="1234567890123",
            filename="test.uff",
            line_number=10,
        )
        self.assertEqual(error.mpan, "1234567890123")
        self.assertEqual(error.filename, "test.uff")
        self.assertEqual(error.line_number, 10)
        self.assertIn("1234567890123", str(error))

    def test_meter_point_not_found_error_minimal(self):
        """Test MeterPointNotFoundError with minimal args."""
        error = MeterPointNotFoundError(mpan="9876543210987")
        self.assertEqual(error.mpan, "9876543210987")
        self.assertIsNone(error.filename)
        self.assertIsNone(error.line_number)

    def test_meter_not_found_error(self):
        """Test MeterNotFoundError initialization."""
        error = MeterNotFoundError(
            serial_number="XYZ123456",
            filename="test.uff",
            line_number=20,
        )
        self.assertEqual(error.serial_number, "XYZ123456")
        self.assertEqual(error.filename, "test.uff")
        self.assertEqual(error.line_number, 20)
        self.assertIn("XYZ123456", str(error))

    def test_meter_not_found_error_minimal(self):
        """Test MeterNotFoundError with minimal args."""
        error = MeterNotFoundError(serial_number="ABC987654")
        self.assertEqual(error.serial_number, "ABC987654")
        self.assertIsNone(error.filename)
        self.assertIsNone(error.line_number)
