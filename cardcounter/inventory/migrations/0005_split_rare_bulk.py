from django.db import migrations


def split_rare(apps, schema_editor):
    BulkCount = apps.get_model('inventory', 'BulkCount')
    BulkCount.objects.filter(rarity='RARE_HOLO_REVERSE').delete()
    BulkCount.objects.get_or_create(rarity='RARE_HOLO', defaults={'quantity': 0})
    BulkCount.objects.get_or_create(rarity='RARE_REVERSE', defaults={'quantity': 0})


def unsplit_rare(apps, schema_editor):
    BulkCount = apps.get_model('inventory', 'BulkCount')
    BulkCount.objects.filter(rarity__in=['RARE_HOLO', 'RARE_REVERSE']).delete()
    BulkCount.objects.get_or_create(rarity='RARE_HOLO_REVERSE', defaults={'quantity': 0})


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_bulkcount_rarity_alter_cardentry_rarity'), 
    ]

    operations = [
        migrations.RunPython(split_rare, unsplit_rare),
    ]
