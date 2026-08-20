from django.db import models

# Create your models here.
class Rarity(models.TextChoices):
    COMMON_UNCOMMON = "COMMON_UNCOMMON", "Common / Uncommon"
    COMMON_UNCOMMON_REVERSE = "COMMON_UNCOMMON_REVERSE", "Common / Uncommon (Reverse Holo)"
    RARE_HOLO = "RARE_HOLO", "Rare (Holo)"
    RARE_REVERSE = "RARE_REVERSE", "Rare (Reverse Holo)"
    DOUBLE_RARE = "DOUBLE_RARE", "Double Rare"
    ULTRA_RARE = "ULTRA_RARE", "Ultra Rare"
    HYPER_RARE = "HYPER_RARE", "Hyper Rare"
    MEGA_HYPER_RARE = "MEGA_HYPER_RARE", "Mega Hyper Rare"
    ILL_RARE = "ILL_RARE", "Illustration Rare"
    SPEC_ILL_RARE = "SPEC_ILL_RARE", "Special Illustration Rare"
    ACE_SPEC_RARE = "ACE_SPEC_RARE", "ACE SPEC Rare"
    SHINY_RARE = "SHINY_RARE", "Shiny Rare"
    SHINY_ULTRA_RARE = "SHINY_ULTRA_RARE", "Shiny Ultra Rare"
    SECRET_RARE = "SECRET_RARE", "Secret Rare"
    PROMO = "PROMO", "Promo"
    
    @classmethod
    def bulk_tiers(cls):
        return [cls.COMMON_UNCOMMON, cls.COMMON_UNCOMMON_REVERSE, cls.RARE_HOLO, cls.RARE_REVERSE]
    
    @classmethod
    def priced_tiers(cls):
        return [cls.DOUBLE_RARE, cls.ULTRA_RARE, cls.HYPER_RARE, cls.MEGA_HYPER_RARE, cls.ILL_RARE, cls.SPEC_ILL_RARE, cls.ACE_SPEC_RARE, cls.SHINY_RARE, cls.SHINY_ULTRA_RARE, cls.SECRET_RARE, cls.PROMO,]

class BulkCount(models.Model):
    rarity = models.CharField(
        max_length= 32,
        choices= Rarity.choices,
        unique= True,
    )
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.get_rarity_display()}: {self.quantity}"
  
class Set(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, blank=True)
    available_rarities = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CardEntry(models.Model):
    rarity = models.CharField(
        max_length= 32,
        choices= Rarity.choices,
    ) 
    name = models.CharField(max_length= 200, blank= True)
    set_name = models.CharField(max_length=200, blank=True)  # kept temporarily for migration
    set = models.ForeignKey(Set, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField(default= 1)
    estimated_value = models.DecimalField(
        max_digits= 8,
        decimal_places= 2,
        null= True,
        blank= True,
    ) #price is optional esp. for bulk
    added_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Card entries"
    
    def __str__(self):
        label = self.name or self.get_rarity_display()
        return f"{label} x{self.quantity}"
