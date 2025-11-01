"""
Signal handlers for cache invalidation.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.
    
    Args:
        sender: The model class (Property)
        instance: The actual instance being saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    action = "created" if created else "updated"
    logger.info(f"Property {instance.id} {action} - cache '{cache_key}' invalidated")


@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.
    
    Args:
        sender: The model class (Property)
        instance: The actual instance being deleted
        **kwargs: Additional keyword arguments
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    logger.info(f"Property {instance.id} deleted - cache '{cache_key}' invalidated")