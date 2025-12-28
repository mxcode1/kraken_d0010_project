"""
Tests for utility functions.
"""

from django.test import TestCase
from unittest.mock import patch, MagicMock

from meter_readings.utils import get_sample_files, get_sample_file_path, clear_all_data


class GetSampleFilesTest(TestCase):
    """Tests for get_sample_files function."""

    @patch("meter_readings.utils.Path")
    def test_returns_empty_when_directory_missing(self, mock_path: MagicMock) -> None:
        """Test returns empty list when sample_data directory doesn't exist."""
        mock_sample_dir = MagicMock()
        mock_sample_dir.exists.return_value = False
        mock_path.return_value.__truediv__.return_value = mock_sample_dir

        result = get_sample_files()

        self.assertEqual(result, [])

    def test_returns_sorted_uff_files(self) -> None:
        """Test returns sorted list of .uff files from sample_data."""
        # This will use the actual sample_data directory
        result = get_sample_files()

        # Verify we get a list
        self.assertIsInstance(result, list)

        # All entries should be .uff files
        for filename in result:
            self.assertTrue(filename.endswith(".uff"))

        # List should be sorted
        self.assertEqual(result, sorted(result))


class GetSampleFilePathTest(TestCase):
    """Tests for get_sample_file_path function."""

    def test_returns_path_to_sample_file(self) -> None:
        """Test returns correct path for a sample file."""
        result = get_sample_file_path("test.uff")

        self.assertTrue(str(result).endswith("sample_data/test.uff"))


class ClearAllDataTest(TestCase):
    """Tests for clear_all_data function."""

    def test_clears_all_data_and_returns_counts(self) -> None:
        """Test clears all database records and returns deletion counts."""
        from meter_readings.models import FlowFile, MeterPoint, Meter, Reading
        from django.utils import timezone

        # Create test data
        flow_file = FlowFile.objects.create(
            filename="test_utils.uff",
            file_reference="TEST001",
            record_count=1,
        )
        meter_point = MeterPoint.objects.create(mpan="1234567890123")
        meter = Meter.objects.create(
            meter_point=meter_point,
            serial_number="E12345678",
            meter_type="S",
        )
        Reading.objects.create(
            meter=meter,
            flow_file=flow_file,
            reading_date=timezone.now(),
            reading_value=12345,
            register_id="01",
            reading_type="ACTUAL",
        )

        # Verify data exists
        self.assertEqual(FlowFile.objects.count(), 1)
        self.assertEqual(MeterPoint.objects.count(), 1)
        self.assertEqual(Meter.objects.count(), 1)
        self.assertEqual(Reading.objects.count(), 1)

        # Clear all data
        counts = clear_all_data()

        # Verify counts returned
        self.assertEqual(counts["flow_files"], 1)
        self.assertEqual(counts["meter_points"], 1)
        self.assertEqual(counts["meters"], 1)
        self.assertEqual(counts["readings"], 1)

        # Verify data is cleared
        self.assertEqual(FlowFile.objects.count(), 0)
        self.assertEqual(MeterPoint.objects.count(), 0)
        self.assertEqual(Meter.objects.count(), 0)
        self.assertEqual(Reading.objects.count(), 0)
