"""Unit tests for management commands.

Note: These tests import D0010 files which contain timestamps without timezone
information (format: YYYYMMDDHHMMSS). The resulting naive datetime warnings
are expected and indicate the parser is correctly handling the file format.
"""

import os
import tempfile
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from meter_readings.models import MeterPoint, Meter, Reading, FlowFile


class ImportD0010CommandTest(TestCase):
    def setUp(self):
        self.sample_content = (
            "ZHV|0000475656|D0010002|D|UDMS|X|MRCY|20160302153151||||OPER| | |\n"
            "026|1200023305967|V| | |\n"
            "028|F75A 00802|D| | |\n"
            "030|S|20160222000000|56311.0|||T|N| | |\n"
            "ZPT|0000475656|35||11|20160302154650| |"
        )

        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".uff", delete=False
        )
        self.temp_file.write(self.sample_content)
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_successful_import(self):
        """Test successful import of valid D0010 file."""
        call_command("import_d0010", self.temp_file.name)

        self.assertEqual(FlowFile.objects.count(), 1)
        self.assertEqual(MeterPoint.objects.count(), 1)
        self.assertEqual(Meter.objects.count(), 1)
        self.assertEqual(Reading.objects.count(), 1)

    def test_dry_run_mode(self):
        """Test dry run mode doesn't persist data."""
        call_command("import_d0010", self.temp_file.name, dry_run=True)

        self.assertEqual(FlowFile.objects.count(), 0)
        self.assertEqual(MeterPoint.objects.count(), 0)
        self.assertEqual(Meter.objects.count(), 0)
        self.assertEqual(Reading.objects.count(), 0)

    def test_file_not_found(self):
        """Test error for non-existent file."""
        out = StringIO()
        call_command("import_d0010", "/nonexistent/file.uff", stdout=out)
        self.assertIn("File not found", out.getvalue())

    def test_duplicate_file_import(self):
        """Test rejection of duplicate files."""
        call_command("import_d0010", self.temp_file.name, stdout=StringIO())
        out = StringIO()
        call_command("import_d0010", self.temp_file.name, stdout=out)
        self.assertIn("already been imported", out.getvalue())

    def test_invalid_mpan(self):
        """Test invalid MPAN handling."""
        content = """ZHD|TEST|FLOW
026|INVALID
028|SN123|S
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            # Error format: "Failed to parse 026 record"
            self.assertIn("Failed to parse 026", out.getvalue())
        finally:
            os.unlink(path)

    def test_empty_file(self):
        """Test empty file handling."""
        content = "ZHD|TEST|FLOW\nZPT|TEST|0"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            self.assertIn("No readings", out.getvalue())
        finally:
            os.unlink(path)

    def test_reading_without_mpan(self):
        """Test reading without MPAN."""
        content = """ZHD|TEST|FLOW
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            # Error format: "Failed to parse 030 record"
            self.assertIn("Failed to parse 030", out.getvalue())
        finally:
            os.unlink(path)

    def test_invalid_date_format(self):
        """Test invalid date format."""
        content = """ZHD|TEST|FLOW
026|1234567890123
028|SN123|S
030|S|BADDATE|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            # Error format: "Failed to parse 030 record" for date issues
            self.assertIn("Failed to parse 030", out.getvalue())
        finally:
            os.unlink(path)

    def test_invalid_reading_value(self):
        """Test invalid reading value."""
        content = """ZHD|TEST|FLOW
026|1234567890123
028|SN123|S
030|S|20160222000000|INVALID|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            # Error format: "Failed to parse 030 record" for value issues
            self.assertIn("Failed to parse 030", out.getvalue())
        finally:
            os.unlink(path)

    def test_empty_serial_number(self):
        """Test empty serial number."""
        content = """ZHD|TEST|FLOW
026|1234567890123
028||S
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            # Error format: "Failed to parse 028 record" for empty serial
            self.assertIn("Failed to parse 028", out.getvalue())
        finally:
            os.unlink(path)

    def test_file_with_blank_lines(self):
        """Test file with blank lines are skipped."""
        content = """ZHD|TEST|FLOW

026|1234567890123

028|SN123|S
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            call_command("import_d0010", path, stdout=StringIO())
            self.assertEqual(Reading.objects.count(), 1)
        finally:
            os.unlink(path)

    def test_invalid_026_record(self):
        """Test invalid 026 MPAN record."""
        content = """ZHD|TEST|FLOW
026
028|SN123|S
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            self.assertIn("Failed to parse 026", out.getvalue())
        finally:
            os.unlink(path)

    def test_invalid_028_record(self):
        """Test invalid 028 meter record."""
        content = """ZHD|TEST|FLOW
026|1234567890123
028
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            self.assertIn("Failed to parse 028", out.getvalue())
        finally:
            os.unlink(path)

    def test_invalid_030_record(self):
        """Test invalid 030 reading record."""
        content = """ZHD|TEST|FLOW
026|1234567890123
028|SN123|S
030
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            out = StringIO()
            call_command("import_d0010", path, stdout=out)
            self.assertIn("Failed to parse 030", out.getvalue())
        finally:
            os.unlink(path)

    def test_database_error_handling(self):
        """Test database error handling during save."""
        from unittest.mock import patch

        content = """ZHD|TEST|FLOW
026|1234567890123
028|SN123|S
030|S|20160222000000|100.5|||T|N| | |
ZPT|TEST|1"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            with patch(
                "meter_readings.models.Reading.objects.get_or_create",
                side_effect=Exception("DB Error"),
            ):
                out = StringIO()
                call_command("import_d0010", path, stdout=out)
                self.assertIn("Database error", out.getvalue())
        finally:
            os.unlink(path)
