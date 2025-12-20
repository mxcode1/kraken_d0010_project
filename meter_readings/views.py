"""Views for meter readings application."""

from typing import Dict

from django.http import HttpRequest, HttpResponse

from .models import FlowFile, Meter, MeterPoint, Reading


def index(request: HttpRequest) -> HttpResponse:
    """Dashboard view showing application status."""
    context: Dict[str, int] = {
        "meter_points_count": MeterPoint.objects.count(),
        "meters_count": Meter.objects.count(),
        "readings_count": Reading.objects.count(),
        "flow_files_count": FlowFile.objects.count(),
    }

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kraken Energy D0010 System</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px;
                background: #f8f9fa; }}
            .container {{ max-width: 800px; margin: 0 auto;
                background: white; padding: 40px; border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .stats {{ background: #e9ecef; padding: 20px;
                border-radius: 8px; margin-bottom: 30px; }}
            .stat {{ margin: 15px 0; display: flex;
                justify-content: space-between; align-items: center; }}
            .stat-label {{ font-weight: bold; }}
            .stat-value {{ background: #007bff; color: white;
                padding: 5px 15px; border-radius: 20px; }}
            .admin-link {{ text-align: center; margin: 30px 0; }}
            .admin-link a {{
                background: #28a745; color: white;
                padding: 15px 30px; text-decoration: none;
                border-radius: 5px; font-size: 18px;
                display: inline-block; transition: background 0.3s;
            }}
            .admin-link a:hover {{ background: #218838; }}
            .usage {{ margin-top: 30px; }}
            .usage ol {{ line-height: 1.8; }}
            .code {{ background: #f8f9fa; padding: 2px 8px;
                border-radius: 3px; font-family: monospace; }}
            .kraken {{ font-size: 3em; text-align: center;
                margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="kraken">🦑</div>
                <h1>Kraken Energy D0010 Flow Files System</h1>
                <p>Electricity Meter Reading Management Platform</p>
            </div>

            <div class="stats">
                <h2 style="margin-top: 0;">📊 System Statistics</h2>
                <div class="stat">
                    <span class="stat-label">🏠 Meter Points (MPANs)</span>
                    <span class="stat-value">{context['meter_points_count']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">🔌 Physical Meters</span>
                    <span class="stat-value">{context['meters_count']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">📈 Meter Readings</span>
                    <span class="stat-value">{context['readings_count']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">📄 Imported Files</span>
                    <span class="stat-value">{context['flow_files_count']}</span>
                </div>
            </div>

            <div class="admin-link">
                <a href="/admin/">🚀 Access Admin Interface</a>
            </div>

            <div class="admin-link">
                <a href="/admin/testing/">🔍 Access Test Upload - Demo Dashboard </a>
            </div>
            <div class="usage">
                <h3>💡 How to Use This System</h3>
                <ol>
                    <li><strong>Import D0010 files:</strong>
                        <span class="code">
                            python manage.py import_d0010 path/to/file.uff
                        </span>
                    </li>
                    <li><strong>Browse data:</strong>
                        Use the <a href="/admin/">Admin Interface</a> above
                    </li>
                    <li><strong>Search by MPAN:</strong>
                        Enter 13-digit meter point number
                    </li>
                    <li><strong>Search by Serial:</strong>
                        Enter meter serial number
                    </li>
                    <li><strong>View source files:</strong>
                        See which file each reading came from
                    </li>
                </ol>

                <h3>🔍 Demo Search Examples</h3>
                <ul>
                    <li><strong>MPAN Search:</strong>
                        Try searching for <span class="code">1200023305967</span>
                    </li>
                    <li><strong>Serial Search:</strong>
                        Try searching for <span class="code">F75A 00802</span>
                    </li>
                    <li><strong>Filename Search:</strong>
                        Try searching for <span class="code">sample_d0010.uff</span>
                    </li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

    return HttpResponse(html_content)
