from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    list_display = ('title', 'order')
    
    # Inyectamos nuestro fichero css
    class Media:
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }
        
admin.site.register(Page, PageAdmin)