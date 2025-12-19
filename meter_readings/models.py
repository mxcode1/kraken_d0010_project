"""Models for D0010 meter readings application."""

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

import re


class FlowFile(models.Model):
    """Represents a D0010 flow file that has been imported."""

    filename = models.CharField(
        max_length=255, unique=True, help_text="Original filename"
    )
    file_reference = models.CharField(
        max_length=50, help_text="File reference from ZHV header"
    )
    imported_at = models.DateTimeField(auto_now_add=True, help_text="Import timestamp")
    record_count = models.PositiveIntegerField(
        default=0, help_text="Number of records imported"
    )

    class Meta:
        ordering = ["-imported_at"]
        verbose_name = "Flow File"
        verbose_name_plural = "Flow Files"

    def __str__(self):
        return (
            f"{self.filename} (imported {self.imported_at.strftime('%Y-%m-%d %H:%M')})"
        )


class MeterPoint(models.Model):
    """Represents a meter point (MPAN)."""

    mpan_validator = RegexValidator(
        regex=r"^\d{13}$", message="MPAN must be exactly 13 digits", code="invalid_mpan"
    )

    mpan = models.CharField(
        max_length=13,
        unique=True,
        validators=[mpan_validator],
        help_text="Meter Point Administration Number (13 digits)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["mpan"]
        verbose_name = "Meter Point"
        verbose_name_plural = "Meter Points"
        indexes = [models.Index(fields=["mpan"], name="idx_meterpoint_mpan")]

    def clean(self):
        if self.mpan and not re.match(r"^\d{13}$", self.mpan):
            raise ValidationError({"mpan": "MPAN must be exactly 13 digits"})

    def __str__(self):
        return f"MPAN: {self.mpan}"


class Meter(models.Model):
    """Represents a physical electricity meter."""

    METER_TYPE_CHOICES = [
        ("S", "Standard"),
        ("C", "Credit"),
        ("D", "Debit"),
        ("P", "Prepayment"),
        ("U", "Unknown"),
    ]

    meter_point = models.ForeignKey(
        MeterPoint,
        on_delete=models.CASCADE,
        related_name="meters",
        help_text="The meter point this meter is associated with",
    )
    serial_number = models.CharField(
        max_length=20, help_text="Physical meter serial number"
    )
    meter_type = models.CharField(
        max_length=1,
        choices=METER_TYPE_CHOICES,
        default="S",
        help_text="Type of meter (from 028 record)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["meter_point__mpan", "serial_number"]
        verbose_name = "Meter"
        verbose_name_plural = "Meters"
        unique_together = [["meter_point", "serial_number"]]
        indexes = [
            models.Index(fields=["serial_number"], name="idx_meter_serial"),
            models.Index(
                fields=["meter_point", "serial_number"], name="idx_meter_mp_serial"
            ),
        ]

    def clean(self):
        if self.serial_number:
            self.serial_number = self.serial_number.strip()
            if not self.serial_number:
                raise ValidationError(
                    {"serial_number": "Serial number cannot be empty"}
                )

    def __str__(self):
        return f"{self.serial_number} ({self.meter_point.mpan})"


class Reading(models.Model):
    """Represents a meter reading."""

    REGISTER_CHOICES = [
        ("S", "Standard"),
        ("01", "Register 1"),
        ("02", "Register 2"),
        ("03", "Register 3"),
        ("A1", "Advance 1"),
        ("TO", "Total"),
        ("DY", "Day"),
        ("NT", "Night"),
        ("WK", "Weekend"),
        ("OT", "Other"),
    ]

    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name="readings")
    flow_file = models.ForeignKey(
        FlowFile, on_delete=models.CASCADE, related_name="readings"
    )
    register_id = models.CharField(max_length=2, choices=REGISTER_CHOICES)
    reading_date = models.DateTimeField(help_text="Date and time of the meter reading")
    reading_value = models.DecimalField(max_digits=12, decimal_places=3)
    reading_type = models.CharField(max_length=10, default="ACTUAL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reading_date", "meter__meter_point__mpan"]
        verbose_name = "Reading"
        verbose_name_plural = "Readings"
        unique_together = [["meter", "register_id", "reading_date"]]
        indexes = [
            models.Index(fields=["reading_date"], name="idx_reading_date"),
            models.Index(
                fields=["meter", "reading_date"], name="idx_reading_meter_date"
            ),
            models.Index(fields=["flow_file"], name="idx_reading_flowfile"),
        ]

    def clean(self):
        if self.reading_value is not None and self.reading_value < 0:
            raise ValidationError({"reading_value": "Reading value cannot be negative"})

    @property
    def mpan(self):
        return self.meter.meter_point.mpan

    @property
    def meter_serial(self):
        return self.meter.serial_number

    def __str__(self):
        return (
            f"{self.mpan} - {self.meter.serial_number} - "
            f"{self.reading_value} on {self.reading_date.strftime('%Y-%m-%d')}"
        )
