"""Custom admin views for testing and debugging."""

import os
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import FlowFile, Meter, MeterPoint, Reading


@staff_member_required
def testing_dashboard(request: HttpRequest) -> HttpResponse:
    """Testing and debugging dashboard."""

    # Get sample data directory
    base_dir: Path = Path(__file__).resolve().parent.parent
    sample_data_dir: Path = base_dir / "sample_data"

    # Get list of .uff files
    sample_files: List[Dict[str, Any]] = []
    if sample_data_dir.exists():
        for file in sorted(sample_data_dir.glob("*.uff")):
            sample_files.append(
                {
                    "name": file.name,
                    "path": str(file),
                    "size": file.stat().st_size,
                    "imported": FlowFile.objects.filter(filename=file.name).exists(),
                }
            )

    # Handle POST actions
    if request.method == "POST":
        action: Optional[str] = request.POST.get("action")

        if action == "clear_all":
            with transaction.atomic():
                reading_count = Reading.objects.count()
                meter_count = Meter.objects.count()
                mp_count = MeterPoint.objects.count()
                file_count = FlowFile.objects.count()

                Reading.objects.all().delete()
                Meter.objects.all().delete()
                MeterPoint.objects.all().delete()
                FlowFile.objects.all().delete()

                messages.success(
                    request,
                    f"✓ Cleared {reading_count} readings, {meter_count} meters, "
                    f"{mp_count} meter points, {file_count} flow files",
                )
            return redirect("testing_dashboard")

        elif action == "import_file":
            file_path = request.POST.get("file_path")
            if file_path and os.path.exists(file_path):
                try:
                    output = StringIO()
                    call_command("import_d0010", file_path, stdout=output)
                    messages.success(
                        request, f"✓ Imported {os.path.basename(file_path)}"
                    )
                except Exception as e:
                    messages.error(
                        request,
                        f"✗ Error importing {os.path.basename(file_path)}: {str(e)}",
                    )
            return redirect("testing_dashboard")

        elif action == "import_all":
            imported = 0
            skipped = 0
            errors = 0

            for file_info in sample_files:
                if not file_info["imported"]:
                    try:
                        output = StringIO()
                        call_command("import_d0010", file_info["path"], stdout=output)
                        imported += 1
                    except Exception as e:
                        errors += 1
                        messages.warning(
                            request, f'✗ Error importing {file_info["name"]}: {str(e)}'
                        )
                else:
                    skipped += 1

            if imported > 0:
                messages.success(request, f"✓ Imported {imported} files")
            if skipped > 0:
                messages.info(request, f"⊘ Skipped {skipped} already imported files")
            if errors > 0:
                messages.error(request, f"✗ {errors} files failed to import")

            return redirect("testing_dashboard")

    # Get current data statistics
    context: Dict[str, Any] = {
        "title": "Testing & Debug Dashboard",
        "sample_files": sample_files,
        "stats": {
            "flow_files": FlowFile.objects.count(),
            "meter_points": MeterPoint.objects.count(),
            "meters": Meter.objects.count(),
            "readings": Reading.objects.count(),
        },
        "recent_files": FlowFile.objects.order_by("-imported_at")[:5],
    }

    return render(request, "admin/testing_dashboard.html", context)
