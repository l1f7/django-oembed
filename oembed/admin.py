from django import forms
from django.contrib import admin

from oembed.models import ProviderRule, StoredOEmbed

class ProviderRuleAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'regex': forms.Textarea(),
            'endpoint': forms.Textarea()
        }

class ProviderRuleAdmin(admin.ModelAdmin):
    form = ProviderRuleAdminForm
    fieldsets = (
        (None, {
            'fields': ('name', 'regex', 'endpoint')
        }),
        (None, {
            'fields': ('format', 'simple')
        }),
    )
    list_display = ['name', 'simple', 'endpoint']
    list_editable = ['simple']
    list_filter = ['simple']
    search_fields = ['name', 'regex', 'endpoint']

admin.site.register(ProviderRule, ProviderRuleAdmin)

class StoredOEmbedAdmin(admin.ModelAdmin):
    pass

admin.site.register(StoredOEmbed, StoredOEmbedAdmin)
