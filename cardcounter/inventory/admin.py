from django.contrib import admin
from .models import BulkCount, CardEntry

# Register your models here.
@admin.register(BulkCount)
class BulkCountAdmin(admin.ModelAdmin):
    list_display = ('rarity', 'quantity')

@admin.register(CardEntry)
class CardEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'set_name', 'estimated_value', 'added_on')
    list_filter = ('rarity',)
    search_fields = ('name', 'set_name')