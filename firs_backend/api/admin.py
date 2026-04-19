from django.contrib import admin


from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'dt', 'loc', 'inv', 'alarm', 'dmg_raw', 'by_user', 'created_at')
    list_filter   = ('inv', 'alarm')
    search_fields = ('loc', 'occ', 'by_user', 'rem')
    ordering      = ('created_at',)