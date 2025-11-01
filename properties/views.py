"""
Views for the properties app.
"""

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics
import logging

logger = logging.getLogger(__name__)


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to list all properties with caching.
    Cached for 15 minutes using Redis.
    Uses low-level caching for queryset.
    """
    logger.info("property_list view called - using get_all_properties()")
    
    # Use low-level cached queryset
    properties = get_all_properties()
    
    # Convert to list of dictionaries for JSON response
    properties_data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        }
        for prop in properties
    ]
    
    return JsonResponse({
        'count': len(properties_data),
        'properties': properties_data
    })


def cache_metrics(request):
    """
    View to display Redis cache metrics.
    """
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)