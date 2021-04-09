from django.contrib import admin

from .models import Link, Click

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    fields = ['source', 'owner', 'code', 'name', 'updated', 'created']
    list_display = ['__str__', 'code', 'source', 'owner', 'name', 'get_clicks']

    def get_clicks(self, obj):
        return obj.click_set.count()

    get_clicks.short_description = 'Clicks'


admin.site.register(Click)