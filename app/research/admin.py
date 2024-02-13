from django.contrib import admin
from .models import Research, Tag


class ResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'tags')
    list_per_page = 20

admin.site.register(Research, ResearchAdmin)
admin.site.register(Tag)