from django.contrib import admin
from boots.models import Boot, BootVersion


class BootVersionInline(admin.TabularInline):

    model = BootVersion
    ordering = ('created', 'id',)
    fields = ('slug', 'source',)


class BootAdmin(admin.ModelAdmin):

    search_fields = ('name', 'team__name',)
    list_display = ('team', 'slug',)
    list_filter = ('type',)
    inlines = [
        BootVersionInline,
    ]


admin.site.register(Boot, BootAdmin)