"""
API endpoint tests for meter readings.
"""

import io
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timezone

from meter_readings.models import FlowFile, MeterPoint, Meter, Reading

User = get_user_model()


class APITestCase(TestCase):
    """Test REST API endpoints."""

    def setUp(self):
        """Create test data."""
        self.client = APIClient()

        # Create test data
        self.flow_file = FlowFile.objects.create(
            filename="test.uff", file_reference="TEST001", record_count=2
        )

        self.meter_point = MeterPoint.objects.create(mpan="1234567890123")

        self.meter = Meter.objects.create(
            meter_point=self.meter_point, serial_number="TEST001", meter_type="S"
        )

        self.reading = Reading.objects.create(
            meter=self.meter,
            register_id="S",
            reading_date=datetime(2025, 1, 15, 12, 0, tzinfo=timezone.utc),
            reading_value=12345.67,
            reading_type="ACTUAL",
            flow_file=self.flow_file,
        )

    def test_list_meter_points(self):
        """Test listing meter points."""
        response = self.client.get("/api/meter-points/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["mpan"], "1234567890123")

    def test_retrieve_meter_point(self):
        """Test retrieving single meter point."""
        response = self.client.get(
            f"/api/meter-points/{self.meter_point.pk}/", follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mpan"], "1234567890123")
        self.assertIn("meters", response.data)

    def test_list_readings(self):
        """Test listing readings."""
        response = self.client.get("/api/readings/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_readings_by_mpan(self):
        """Test filtering readings by MPAN."""
        response = self.client.get(
            "/api/readings/", {"mpan": "1234567890123"}, follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_readings_by_date(self):
        """Test filtering readings by date range."""
        response = self.client.get(
            "/api/readings/",
            {"date_from": "2025-01-01", "date_to": "2025-01-31"},
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_readings_summary(self):
        """Test readings summary endpoint."""
        response = self.client.get("/api/readings/summary/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_readings"], 1)
        self.assertEqual(response.data["total_meter_points"], 1)
        self.assertEqual(response.data["total_meters"], 1)

    def test_meter_point_readings_action(self):
        """Test custom action to get readings for a meter point."""
        response = self.client.get(
            f"/api/meter-points/{self.meter_point.pk}/readings/", follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_api_pagination(self):
        """Test API pagination."""
        # Create more readings with unique dates/times to avoid constraint violations
        for i in range(150):
            Reading.objects.create(
                meter=self.meter,
                register_id="S",
                reading_date=datetime(
                    2025, 1, (i % 28) + 1, i % 24, i % 60, tzinfo=timezone.utc
                ),  # Unique timestamps
                reading_value=i * 100,
                reading_type="ACTUAL",
                flow_file=self.flow_file,
            )

        response = self.client.get("/api/readings/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 100)  # PAGE_SIZE
        self.assertIsNotNone(response.data["next"])

    def test_list_flow_files(self):
        """Test listing flow files."""
        response = self.client.get("/api/flow-files/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["filename"], "test.uff")

    def test_retrieve_flow_file(self):
        """Test retrieving single flow file."""
        response = self.client.get(f"/api/flow-files/{self.flow_file.pk}/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["filename"], "test.uff")
        self.assertEqual(response.data["file_reference"], "TEST001")

    def test_list_meters(self):
        """Test listing meters."""
        response = self.client.get("/api/meters/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["serial_number"], "TEST001")

    def test_retrieve_meter(self):
        """Test retrieving single meter."""
        response = self.client.get(f"/api/meters/{self.meter.pk}/", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial_number"], "TEST001")
        self.assertEqual(response.data["meter_type"], "S")

    def test_meter_readings_action(self):
        """Test custom action to get readings for a meter."""
        response = self.client.get(
            f"/api/meters/{self.meter.pk}/readings/", follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_functionality(self):
        """Test search across MPAN and serial number."""
        response = self.client.get(
            "/api/readings/", {"search": "1234567890123"}, follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)

    def test_reading_detail_serializer(self):
        """Test reading detail endpoint uses detailed serializer."""
        response = self.client.get(f"/api/readings/{self.reading.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("meter", response.data)
        self.assertIn("flow_file", response.data)

    def test_meter_serial_filter(self):
        """Test filtering readings by meter serial number."""
        response = self.client.get(
            "/api/readings/", {"meter_serial": "TEST001"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)

    def test_upload_file_unauthenticated(self):
        """Test upload requires authentication."""
        # Create a simple UFF file content
        uff_content = (
            b"ZHV|0000475701|D0010002|D|UDMS|X|MRCY|20250115120000||||OPER| | |\n"
            b"026|1234567890123|V| | |\n"
            b"028|TEST001|S| | |\n"
            b"030|S|20250115120000|12345.000|||A|N| | |\n"
        )

        file = io.BytesIO(uff_content)
        file.name = "test_upload.uff"

        response = self.client.post(
            "/api/flow-files/upload/", {"file": file}, format="multipart"
        )

        # Should require authentication (403 or 401)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_upload_file_authenticated(self):
        """Test successful file upload with authentication."""
        # Create test user
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)

        # Create a valid UFF file content (based on actual D0010 format)
        uff_content = (
            b"ZHV|0000475702|D0010002|D|UDMS|X|MRCY|20250115120000||||OPER| | |\n"
            b"026|9876543210987|V| | |\n"
            b"028|UPLOAD001|S| | |\n"
            b"030|S|20250115120000|54321.000|||A|N| | |\n"
        )

        file = io.BytesIO(uff_content)
        file.name = "test_upload_auth.uff"

        response = self.client.post(
            "/api/flow-files/upload/", {"file": file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["filename"], "test_upload_auth.uff")
        self.assertEqual(response.data["file_reference"], "0000475702")
        self.assertEqual(response.data["record_count"], 1)

        # Verify file was imported
        flow_file = FlowFile.objects.get(filename="test_upload_auth.uff")
        self.assertEqual(flow_file.record_count, 1)

    def test_upload_invalid_file_type(self):
        """Test upload rejects non-UFF files."""
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)

        # Create a non-UFF file
        file = io.BytesIO(b"This is not a UFF file")
        file.name = "test.txt"

        response = self.client.post(
            "/api/flow-files/upload/", {"file": file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("file", response.data)

    def test_upload_invalid_uff_content(self):
        """Test upload handles invalid UFF content."""
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)

        # Create invalid UFF content
        uff_content = b"INVALID UFF CONTENT"

        file = io.BytesIO(uff_content)
        file.name = "invalid.uff"

        response = self.client.post(
            "/api/flow-files/upload/", {"file": file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch("meter_readings.api_views.call_command")
    def test_upload_import_exception(self, mock_call_command):
        """Test upload handles exceptions during import."""
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=user)

        # Mock call_command to raise an exception
        mock_call_command.side_effect = Exception("Database connection failed")

        # Create a valid UFF file content
        uff_content = (
            b"ZHV|0000475703|D0010002|D|UDMS|X|MRCY|20250115120000||||OPER| | |\n"
            b"026|1111222233334|V| | |\n"
            b"028|EXCEPTION001|S| | |\n"
            b"030|S|20250115120000|99999.000|||A|N| | |\n"
        )

        file = io.BytesIO(uff_content)
        file.name = "exception_test.uff"

        response = self.client.post(
            "/api/flow-files/upload/", {"file": file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Database connection failed", response.data["error"])
