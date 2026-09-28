from django.contrib import admin
from .models import BulkCount, CardEntry, Set, KnownCard, Purchase

# Register your models here.
@admin.register(BulkCount)
class BulkCountAdmin(admin.ModelAdmin):
    list_display = ('rarity', 'quantity')

@admin.register(CardEntry)
class CardEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'set', 'quantity', 'estimated_value', 'added_on')
    list_filter = ('rarity', 'set')
    search_fields = ('name',)
    
@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'generation')
    
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'set', 'paid', 'returns', 'date')
    list_filter = ('product', 'set')