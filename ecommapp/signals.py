from .models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Product)
def index_product(sender, instance, **kwargs):
    instance.indexing()
