from django.contrib import admin
from .models import Labels


class TagsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Labels, TagsAdmin)
