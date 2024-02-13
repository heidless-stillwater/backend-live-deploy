from django.contrib import admin
from .models import Qualifications, Tag


class QualificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'tags')
    list_per_page = 20

admin.site.register(Qualifications, QualificationsAdmin)
admin.site.register(Tag)