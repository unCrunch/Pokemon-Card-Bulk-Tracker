from django.db import migrations

BULK_RARITIES = [
    'COMMON_UNCOMMON',
    'COMMON_UNCOMMON_REVERSE',
    'RARE_HOLO_REVERSE',
]


def seed_bulk_counts(apps, schema_editor):
    BulkCount = apps.get_model('inventory', 'BulkCount')
    for rarity in BULK_RARITIES:
        BulkCount.objects.get_or_create(rarity=rarity, defaults={'quantity': 0})


def remove_bulk_counts(apps, schema_editor):
    BulkCount = apps.get_model('inventory', 'BulkCount')
    BulkCount.objects.filter(rarity__in=BULK_RARITIES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_bulk_counts, remove_bulk_counts),
    ]