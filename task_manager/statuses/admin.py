from django.contrib import admin
from .models import Statuses


class StatusesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Statuses, StatusesAdmin)
