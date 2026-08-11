from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BulkCount, Rarity, CardEntry
from .forms import CardEntryForm

# Create your views here.
def totals(request):
    context = {}
    return render(request, "inventory/totals.html", context)

def cards(request):
    if request.method == "POST":
        form = CardEntryForm
        if form.is_valid():
            form.save()
            return redirect("cards")
    else:
        form = CardEntryForm()
    
    card_entries = CardEntry.objects.all().order_by("-added_on")
    context = {"form": form, "card_entries": card_entries}
    return render(request, "inventory/cards.html", context)

def home(request):
    if request.method == "POST":
        action = request.POST.get("action")
        
        for rarity in Rarity.bulk_tiers():
            field_name = f"quantity_{rarity}"
            value = request.POST.get(field_name, "").strip()
            if value == "":
                continue
            
            amount = int(value)
            bulk_count = BulkCount.objects.get(rarity=rarity)
            
            if action == "add":
                bulk_count.quantity += amount
            elif action == "remove":
                bulk_count.quantity = max(0, bulk_count.quantity - amount)
            elif action == "set":
                bulk_count.quantity = amount
                
            bulk_count.save()
        return redirect("home")
    
    bulk_counts = BulkCount.objects.all()
    context = {"bulk_counts": bulk_counts}
    return render(request, "inventory/home.html", context)