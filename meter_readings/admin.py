from django.contrib import admin
from .models import FlowFile, MeterPoint, Meter, Reading


admin.site.register(FlowFile)
admin.site.register(MeterPoint)
admin.site.register(Meter)
admin.site.register(Reading)
