"""
Utility functions for meter_readings app.
"""

from pathlib import Path
from typing import Dict, List

from django.conf import settings


def get_sample_files() -> List[str]:
    """Get list of all .uff files in sample_data directory."""
    sample_dir = Path(settings.BASE_DIR) / "sample_data"
    if not sample_dir.exists():
        return []

    files = list(sample_dir.glob("*.uff"))
    return sorted([f.name for f in files])


def get_sample_file_path(filename: str) -> Path:
    """Get full path to a sample file."""
    return Path(settings.BASE_DIR) / "sample_data" / filename


def clear_all_data() -> Dict[str, int]:
    """
    Clear all meter reading data from database.
    WARNING: This is destructive and cannot be undone.
    """
    from .models import Reading, Meter, MeterPoint, FlowFile

    count = {
        "readings": Reading.objects.count(),
        "meters": Meter.objects.count(),
        "meter_points": MeterPoint.objects.count(),
        "flow_files": FlowFile.objects.count(),
    }

    # Delete in correct order (respect foreign keys)
    Reading.objects.all().delete()
    Meter.objects.all().delete()
    MeterPoint.objects.all().delete()
    FlowFile.objects.all().delete()

    return count
