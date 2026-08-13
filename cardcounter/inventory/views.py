from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from .models import BulkCount, Rarity, CardEntry
from .forms import CardEntryForm

# Create your views here.
def totals(request):
    card_entries = CardEntry.objects.all()
    
    #total value = sum of (qty*est_value)
    total_value = card_entries.aggregate(
        total=Coalesce(
            Sum(F("quantity") *F("estimated_value"), output_field=DecimalField()), 0, output_field=DecimalField(),
        )
    ) ["total"]
    
    #breakdown per priced rarity tier
    rarity_breakdown = []
    for rarity in Rarity.priced_tiers():
        tier_entries = card_entries.filter(rarity=rarity)
        tier_count = tier_entries.aggregate(total=Coalesce(Sum("quantity"), 0))["total"]
        tier_value = tier_entries.aggregate(
            total=Coalesce(
                Sum(F("quantity") *F("estimated_value"), output_field=DecimalField()), 0, output_field=DecimalField(),
            )
        )["total"]
        rarity_breakdown.append({
            "label": Rarity(rarity).label,
            "count": tier_count,
            "value": tier_value,
        })
    
    bulk_counts = BulkCount.objects.all()
    
    
    context = {
        "total_value": total_value,
        "rarity_breakdown": rarity_breakdown,
        "bulk_counts": bulk_counts,
    }
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