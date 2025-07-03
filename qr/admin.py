from django.contrib import admin
from django.utils.html import format_html
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_preview', 'content_length', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'content_length_display']
    ordering = ['-created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Contenido del QR', {
            'fields': ('content',)
        }),
        ('Información', {
            'fields': ('created_at', 'content_length_display'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        """Vista previa del contenido"""
        preview = obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, preview)
    content_preview.short_description = "Vista previa"
    
    def content_length(self, obj):
        """Longitud del contenido"""
        return len(obj.content)
    content_length.short_description = "Caracteres"
    
    def content_length_display(self, obj):
        """Longitud para el formulario"""
        return f"{len(obj.content)} caracteres"
    content_length_display.short_description = "Longitud del contenido"