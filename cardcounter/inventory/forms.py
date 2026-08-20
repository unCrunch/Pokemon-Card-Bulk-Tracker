from django import forms
from .models import CardEntry, Rarity, Set

INPUT_CLASSES = "w-full border border-gray-300 dark:border-gray-600 dark:bg-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500"

class CardEntryForm(forms.ModelForm):
    rarity = forms.ChoiceField(
        choices=[(r.value, r.label) for r in Rarity.priced_tiers()],
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
    )
    set = forms.ModelChoiceField(
        queryset=Set.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": INPUT_CLASSES}),
    )
    
    class Meta:
        model = CardEntry
        fields = ["rarity", "name", "quantity", "estimated_value"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "quantity": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "estimated_value": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }