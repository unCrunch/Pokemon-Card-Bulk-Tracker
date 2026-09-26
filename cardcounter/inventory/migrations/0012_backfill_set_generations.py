from django.db import migrations

GENERATION_MAP = {
    "Mega Evolution": "Mega Evolution",
    "Pitch Black": "Mega Evolution",
    "Chaos Rising": "Mega Evolution",
    "Perfect Order": "Mega Evolution",
    "Ascended Heroes": "Mega Evolution",
    "Phantasmal Flames": "Mega Evolution",
    "Mega Evolution Energy": "Mega Evolution",
    "Mega Evolution Promos": "Mega Evolution",
    "White Flare": "Scarlet & Violet",
    "Scarlet & Violet Energy": "Scarlet & Violet",
    "Black Bolt": "Scarlet & Violet",
    "Destined Rivals": "Scarlet & Violet",
    "Journey Together": "Scarlet & Violet",
    "Prismatic Evolutions": "Scarlet & Violet",
    "Surging Sparks": "Scarlet & Violet",
    "Stellar Crown": "Scarlet & Violet",
    "Shrouded Fable": "Scarlet & Violet",
    "Twilight Masquerade": "Scarlet & Violet",
    "Temporal Forces": "Scarlet & Violet",
    "Paldean Fates": "Scarlet & Violet",
    "Paradox Rift": "Scarlet & Violet",
    "151": "Scarlet & Violet",
    "Obsidian Flames": "Scarlet & Violet",
    "Paldea Evolved": "Scarlet & Violet",
    "Scarlet & Violet": "Scarlet & Violet",
    "Scarlet & Violet Promos": "Scarlet & Violet",
}


def backfill_generations(apps, schema_editor):
    Set = apps.get_model("inventory", "Set")
    for name, generation in GENERATION_MAP.items():
        Set.objects.filter(name=name).update(generation=generation)


def reverse_backfill(apps, schema_editor):
    Set = apps.get_model("inventory", "Set")
    Set.objects.update(generation="")


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0011_set_generation"),
    ]

    operations = [
        migrations.RunPython(backfill_generations, reverse_backfill),
    ]