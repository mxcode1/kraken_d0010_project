from django.core.management.base import BaseCommand
from django.db import transaction
from meter_readings.models import FlowFile, MeterPoint, Meter, Reading
from pathlib import Path
from datetime import datetime


class Command(BaseCommand):
    help = 'Import D0010 meter reading files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to D0010 file')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Parse file without saving to database'
        )

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])
        dry_run = options.get('dry_run', False)
        
        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        self.stdout.write(f'Processing: {file_path.name}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No database changes'))
        
        # Parse file
        try:
            header, readings = self.parse_d0010_file(file_path)
            self.stdout.write(f'Parsed header: {header}')
            self.stdout.write(f'Found {len(readings)} reading records')
            
            if not dry_run:
                self.save_to_database(file_path.name, header, readings)
            
            self.stdout.write(self.style.SUCCESS('Import complete!'))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
    
    def parse_d0010_file(self, file_path):
        """Parse D0010 file and extract header + readings."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            raise ValueError('Empty file')
        
        # Parse header (ZHF record)
        header_line = lines[0].strip()
        if not header_line.startswith('ZHF'):
            raise ValueError('Invalid D0010 file - missing ZHF header')
        
        # Extract date from header (positions vary by spec)
        # Example: ZHFNNNNN20231201...
        date_str = header_line[8:16]  # YYYYMMDD format
        file_date = datetime.strptime(date_str, '%Y%m%d').date()
        
        header = {
            'file_date': file_date,
            'flow_id': header_line[3:8]
        }
        
        # Parse reading records (to be implemented)
        readings = []
        
        return header, readings
    
    def save_to_database(self, filename, header, readings):
        """Save parsed data to database."""
        with transaction.atomic():
            # Create FlowFile record
            flow_file, created = FlowFile.objects.get_or_create(
                filename=filename,
                defaults={
                    'file_date': header['file_date'],
                    'record_count': len(readings)
                }
            )
            
            if not created:
                self.stdout.write(self.style.WARNING(f'File already imported: {filename}'))
                return
            
            # TODO: Process readings
            self.stdout.write(self.style.SUCCESS(f'Created FlowFile: {flow_file}'))
