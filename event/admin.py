from django.contrib import admin
from event.models import Event


class EventAdminCustom(admin.ModelAdmin):
    filter_horizontal = ('participant', )


admin.site.register(Event, EventAdminCustom)
