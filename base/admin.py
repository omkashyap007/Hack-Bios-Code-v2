from django.contrib import admin
from base.models import PiGroup

@admin.register(PiGroup)
class PiGroupAdmin(admin.ModelAdmin):
    list_display = ["group_name"]