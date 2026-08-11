from django import forms
from .models import CardEntry, Rarity

class CardEntryForm(forms.ModelForm):
    rarity = forms.ChoiceField(
        choices=[(r.value, r.label) for r in Rarity.priced_tiers()]
    )
    
    class Meta:
        model = CardEntry
        fields = ["rarity", "name", "set_name", "quantity", "estimated_value"]