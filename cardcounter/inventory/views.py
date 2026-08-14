from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce

from .models import BulkCount, Rarity, CardEntry
from .forms import CardEntryForm

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
    total_card_count = 0
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
        total_card_count += tier_count
    
    bulk_counts = BulkCount.objects.all()
    total_bulk_count = bulk_counts.aggregate(total=Coalesce(Sum("quantity"), 0))["total"]
    
    
    context = {
        "total_value": total_value,
        "rarity_breakdown": rarity_breakdown,
        "total_card_count": total_card_count,
        "bulk_counts": bulk_counts,
        "total_bulk_count": total_bulk_count,
    }
    return render(request, "inventory/totals.html", context)

def cards(request):
    if request.method == "POST":
        form = CardEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cards")
    else:
        form = CardEntryForm()
    
    card_entries = CardEntry.objects.all().order_by("-added_on")
    context = {"form": form, "card_entries": card_entries}
    return render(request, "inventory/cards.html", context)

def edit_card(request, card_id):
    card = get_object_or_404(CardEntry, id=card_id)
    if request.method == "POST":
        form = CardEntryForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect("cards")
    else:
        form = CardEntryForm(instance=card)
    
    context = {"form": form, "card": card}
    return render(request, "inventory/edit_card.html", context)

def del_card(request, card_id):
    card = get_object_or_404(CardEntry, id=card_id)
    if request.method == "POST":
        card.delete()
    return redirect("cards")

def home(request):
    if request.method == "POST":
        action = request.POST.get("action")
        
        for rarity in Rarity.bulk_tiers():
            field_name = f"quantity_{rarity}"
            value = request.POST.get(field_name, "").strip()
            if value == "":
                continue
            if not value.isdigit():
                messages.error(request, f"'{value}' is not a valid number for {Rarity(rarity).label}.")
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