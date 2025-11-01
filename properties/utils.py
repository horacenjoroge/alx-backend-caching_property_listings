"""
Utility functions for the properties app.
"""

from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Get all properties with low-level caching.
    
    Checks Redis cache first. If not found, fetches from database
    and caches for 1 hour (3600 seconds).
    
    Returns:
        QuerySet: All Property objects
    """
    cache_key = 'all_properties'
    
    # Try to get from cache
    properties = cache.get(cache_key)
    
    if properties is not None:
        logger.info(f"Cache HIT for {cache_key}")
        return properties
    
    # Cache miss - fetch from database
    logger.info(f"Cache MISS for {cache_key} - fetching from database")
    properties = list(Property.objects.all())
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties, 3600)
    logger.info(f"Cached {len(properties)} properties for 1 hour")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including:
            - keyspace_hits: Number of cache hits
            - keyspace_misses: Number of cache misses
            - hit_ratio: Cache hit ratio (hits / total requests)
    """
    from django_redis import get_redis_connection
    
    try:
        # Get Redis connection
        redis_conn = get_redis_connection('default')
        
        # Get Redis INFO stats
        info = redis_conn.info('stats')
        
        # Extract metrics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2),
        }
        
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
        }