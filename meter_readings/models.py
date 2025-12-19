from django.db import models


class FlowFile(models.Model):
    """
    Represents an imported D0010 file.
    Tracks which files have been processed to prevent duplicates.
    """
    filename = models.CharField(max_length=255, unique=True, db_index=True)
    file_date = models.DateField(help_text="Processing date from file header")
    imported_at = models.DateTimeField(auto_now_add=True)
    record_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Flow File"
        verbose_name_plural = "Flow Files"
        ordering = ['-imported_at']
    
    def __str__(self):
        return f"{self.filename} ({self.file_date})"


class MeterPoint(models.Model):
    """
    Represents a Meter Point Administration Number (MPAN).
    The unique identifier for an electricity supply point.
    """
    METER_TYPE_CHOICES = [
        ('domestic', 'Domestic'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ]
    
    mpan = models.CharField(
        max_length=13,
        unique=True,
        db_index=True,
        help_text="13-digit Meter Point Administration Number"
    )
    meter_type = models.CharField(
        max_length=20,
        choices=METER_TYPE_CHOICES,
        default='domestic'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Meter Point"
        verbose_name_plural = "Meter Points"
        ordering = ['mpan']
    
    def __str__(self):
        return self.mpan


class Meter(models.Model):
    """
    Physical electricity meter installed at a meter point.
    Multiple meters can exist for one MPAN over time.
    """
    meter_point = models.ForeignKey(
        MeterPoint,
        on_delete=models.CASCADE,
        related_name='meters'
    )
    serial_number = models.CharField(max_length=50, unique=True, db_index=True)
    meter_type = models.CharField(
        max_length=50,
        help_text="Meter type code from D0010"
    )
    installed_date = models.DateField(null=True, blank=True)
    removed_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Meter"
        verbose_name_plural = "Meters"
        ordering = ['serial_number']
    
    def __str__(self):
        return f"{self.serial_number} @ {self.meter_point.mpan}"
