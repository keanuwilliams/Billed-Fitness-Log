from django.contrib import admin
from .models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'user',)


admin.site.register(Session, SessionAdmin)
