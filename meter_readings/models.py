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
