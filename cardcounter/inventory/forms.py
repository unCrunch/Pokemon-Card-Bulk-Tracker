from django import forms
from django.db import models
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
        fields = ["rarity", "name", "set", "quantity", "estimated_value"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "quantity": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "estimated_value": forms.TextInput(attrs={"class": INPUT_CLASSES}),
        }

class KnownCardImportForm(forms.Form):
    set = forms.ModelChoiceField(
        queryset=Set.objects.all(),
        widget=forms.Select(attrs={"class": INPUT_CLASSES})
    )
    csv_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": INPUT_CLASSES}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sets = Set.objects.annotate(known_count=models.Count("known_cards")).order_by("generation", "known_count", "name")
        
        grouped_choices = {}
        for s in sets:
            grouped_choices.setdefault(s.generation or "Other", []).append(
                (s.id, f"{s.name} (already imported)" if s.known_count > 0 else s.name)
            )
        
        self.fields["set"].choices = [(gen, choices) for gen, choices in grouped_choices.items()]