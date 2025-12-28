"""
Comprehensive tests for admin custom views.
Tests admin dashboard, file import, and testing utilities.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase

from meter_readings.models import FlowFile, Meter, MeterPoint, Reading


class AdminViewsTest(TestCase):
    """Test custom admin views and testing dashboard."""

    def setUp(self):
        """Set up test environment."""
        self.client = Client()

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass123"
        )

        # Create test data
        self.flow_file = FlowFile.objects.create(
            filename="test.uff", file_reference="TEST001", record_count=1
        )
        self.meter_point = MeterPoint.objects.create(mpan="1234567890123")
        self.meter = Meter.objects.create(
            meter_point=self.meter_point, serial_number="SN123", meter_type="S"
        )

    def test_testing_dashboard_requires_staff(self):
        """Test testing dashboard requires staff privileges."""
        # Anonymous user should be redirected to login
        response = self.client.get("/admin/testing/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_testing_dashboard_get_request(self):
        """Test GET request to testing dashboard."""
        self.client.force_login(self.admin_user)
        response = self.client.get("/admin/testing/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Testing & Debug Dashboard", response.content.decode())
        self.assertIn("stats", response.context)
        self.assertEqual(response.context["stats"]["flow_files"], 1)
        self.assertEqual(response.context["stats"]["meter_points"], 1)

    def test_testing_dashboard_displays_sample_files(self):
        """Test dashboard displays sample files from sample_data directory."""
        self.client.force_login(self.admin_user)

        # Create a temporary sample_data directory
        base_dir = Path(__file__).resolve().parent.parent.parent
        sample_dir = base_dir / "sample_data"
        sample_dir.mkdir(exist_ok=True)

        # Create a test file
        test_file = sample_dir / "test_sample.uff"
        test_file.write_text("ZHV|TEST|")

        try:
            response = self.client.get("/admin/testing/")
            self.assertEqual(response.status_code, 200)
            self.assertIn("sample_files", response.context)
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()

    def test_clear_all_action(self):
        """Test clear_all action deletes all data."""
        self.client.force_login(self.admin_user)

        # Create a reading
        Reading.objects.create(
            meter=self.meter,
            reading_value=100.0,
            reading_date="2025-01-01 00:00:00",
            reading_type="N",
            flow_file=self.flow_file,
        )

        # Verify data exists
        self.assertEqual(Reading.objects.count(), 1)
        self.assertEqual(Meter.objects.count(), 1)
        self.assertEqual(MeterPoint.objects.count(), 1)
        self.assertEqual(FlowFile.objects.count(), 1)

        # Execute clear_all action
        response = self.client.post("/admin/testing/", {"action": "clear_all"})

        # Should redirect after success
        self.assertEqual(response.status_code, 302)

        # Verify all data is deleted
        self.assertEqual(Reading.objects.count(), 0)
        self.assertEqual(Meter.objects.count(), 0)
        self.assertEqual(MeterPoint.objects.count(), 0)
        self.assertEqual(FlowFile.objects.count(), 0)

    def test_import_file_action_success(self):
        """Test import_file action with valid file."""
        self.client.force_login(self.admin_user)

        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write(
                "ZHV|0000123456|D0010002|D|UDMS|X|MRCY|20231201120000||||OPER| | |\n"
            )
            f.write("026|1234567890123|V| | |\n")
            f.write("028|M00123456|S| | |\n")
            f.write("030|01|20231201100000|12345.000|||T|N| | |\n")
            f.write("ZPT|00002|\n")
            temp_path = f.name

        try:
            response = self.client.post(
                "/admin/testing/", {"action": "import_file", "file_path": temp_path}
            )

            self.assertEqual(response.status_code, 302)

            # Verify import occurred (check for increased counts)
            self.assertGreater(FlowFile.objects.count(), 1)
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_import_file_action_invalid_path(self):
        """Test import_file action with non-existent file."""
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/admin/testing/",
            {"action": "import_file", "file_path": "/nonexistent/file.uff"},
        )

        # Should redirect without error
        self.assertEqual(response.status_code, 302)

    @patch("meter_readings.admin_views.call_command")
    def test_import_file_action_command_error(self, mock_call_command):
        """Test import_file action handles command errors."""
        self.client.force_login(self.admin_user)
        mock_call_command.side_effect = Exception("Import failed")

        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".uff", delete=False) as f:
            f.write("invalid content")
            temp_path = f.name

        try:
            response = self.client.post(
                "/admin/testing/", {"action": "import_file", "file_path": temp_path}
            )

            # Should still redirect
            self.assertEqual(response.status_code, 302)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_import_all_action_imports_new_files(self):
        """Test import_all action imports files not yet imported."""
        self.client.force_login(self.admin_user)

        # Create sample_data directory with test files
        base_dir = Path(__file__).resolve().parent.parent.parent
        sample_dir = base_dir / "sample_data"
        sample_dir.mkdir(exist_ok=True)

        test_file = sample_dir / "import_test.uff"
        test_file.write_text(
            "ZHV|0000123456|D0010002|D|UDMS|X|MRCY|20231201120000||||OPER| | |\n"
            "026|1234567890123|V| | |\n"
            "028|M00123456|S| | |\n"
            "030|01|20231201100000|12345.000|||T|N| | |\n"
            "ZPT|00002|\n"
        )

        try:
            response = self.client.post("/admin/testing/", {"action": "import_all"})

            self.assertEqual(response.status_code, 302)
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()

    def test_import_all_action_skips_imported_files(self):
        """Test import_all skips files already imported."""
        self.client.force_login(self.admin_user)

        # Create sample_data directory
        base_dir = Path(__file__).resolve().parent.parent.parent
        sample_dir = base_dir / "sample_data"
        sample_dir.mkdir(exist_ok=True)

        # Create test file
        test_file = sample_dir / "already_imported.uff"
        test_file.write_text("ZHV|TEST|")

        # Mark as already imported
        FlowFile.objects.create(filename="already_imported.uff")

        try:
            response = self.client.post("/admin/testing/", {"action": "import_all"})

            self.assertEqual(response.status_code, 302)
            # File should still only exist once
            self.assertEqual(
                FlowFile.objects.filter(filename="already_imported.uff").count(), 1
            )
        finally:
            if test_file.exists():
                test_file.unlink()

    @patch("meter_readings.admin_views.call_command")
    def test_import_all_action_handles_errors(self, mock_call_command):
        """Test import_all handles import errors gracefully."""
        self.client.force_login(self.admin_user)
        mock_call_command.side_effect = Exception("Import error")

        # Create sample file
        base_dir = Path(__file__).resolve().parent.parent.parent
        sample_dir = base_dir / "sample_data"
        sample_dir.mkdir(exist_ok=True)

        test_file = sample_dir / "error_test.uff"
        test_file.write_text("BAD DATA")

        try:
            response = self.client.post("/admin/testing/", {"action": "import_all"})

            # Should still redirect successfully
            self.assertEqual(response.status_code, 302)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_recent_files_displayed(self):
        """Test recent_files are shown in dashboard context."""
        self.client.force_login(self.admin_user)

        # Create additional flow files
        for i in range(10):
            FlowFile.objects.create(
                filename=f"file_{i}.uff", file_reference=f"REF{i:03d}", record_count=i
            )

        response = self.client.get("/admin/testing/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("recent_files", response.context)
        # Should show 5 most recent
        self.assertEqual(len(response.context["recent_files"]), 5)

    def test_dashboard_stats_accurate(self):
        """Test dashboard displays accurate statistics."""
        self.client.force_login(self.admin_user)

        # Create multiple entities
        for i in range(3):
            mp = MeterPoint.objects.create(mpan=f"123456789012{i}")
            meter = Meter.objects.create(
                meter_point=mp, serial_number=f"SN{i}", meter_type="S"
            )
            Reading.objects.create(
                meter=meter,
                reading_value=100.0 * i,
                reading_date="2025-01-01 00:00:00",
                reading_type="N",
                flow_file=self.flow_file,
            )

        response = self.client.get("/admin/testing/")

        stats = response.context["stats"]
        # Initial setup created 1, we added 3 more = 4 total
        self.assertEqual(stats["meter_points"], 4)
        self.assertEqual(stats["meters"], 4)
        self.assertEqual(stats["readings"], 3)

    def test_unknown_action_ignored(self):
        """Test unknown POST action is handled gracefully."""
        self.client.force_login(self.admin_user)

        response = self.client.post("/admin/testing/", {"action": "unknown_action"})

        # Should still render the page or redirect
        self.assertIn(response.status_code, [200, 302])
