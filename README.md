# Property Listings - Django Caching with Redis

A Django application demonstrating multi-level caching strategies using Redis for a property listing platform.

## Features

- **Multi-level Caching**: View-level and low-level queryset caching
- **Cache Invalidation**: Automatic cache invalidation using Django signals
- **Dockerized Services**: PostgreSQL and Redis running in Docker containers
- **Cache Metrics**: Monitor and analyze Redis cache performance
- **RESTful API**: JSON endpoints for property listings

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip and virtualenv

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd alx-backend-caching_property_listings
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Docker Containers
```bash
docker-compose up -d
```

Verify containers are running:
```bash
docker-compose ps
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## Project Structure
```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── __init__.py
│   ├── settings.py          # Django settings with cache config
│   ├── urls.py
│   └── wsgi.py
├── properties/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py              # App config with signal import
│   ├── models.py            # Property model
│   ├── signals.py           # Cache invalidation signals
│   ├── urls.py              # URL routing
│   ├── utils.py             # Caching utilities
│   └── views.py             # Cached views
├── docker-compose.yml       # Docker services config
├── manage.py
├── requirements.txt
└── README.md
```

## API Endpoints

### List All Properties
```
GET /properties/
```

Returns a JSON list of all properties (cached for 15 minutes).

**Response:**
```json
{
  "count": 2,
  "properties": [
    {
      "id": 1,
      "title": "Luxury Villa",
      "description": "Beautiful villa with ocean view",
      "price": "500000.00",
      "location": "Miami",
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

### Cache Metrics
```
GET /properties/metrics/
```

Returns Redis cache statistics.

**Response:**
```json
{
  "keyspace_hits": 150,
  "keyspace_misses": 25,
  "total_requests": 175,
  "hit_ratio": 85.71
}
```

## Caching Strategy

### View-Level Caching
- Property list view cached for **15 minutes**
- Uses `@cache_page(60 * 15)` decorator
- Entire HTTP response is cached

### Low-Level Queryset Caching
- Property queryset cached for **1 hour** (3600 seconds)
- Uses `cache.get()` and `cache.set()`
- Cache key: `all_properties`

### Cache Invalidation
- Automatic invalidation on Property create/update/delete
- Implemented using Django signals (`post_save`, `post_delete`)
- Ensures data consistency

## Testing

### Add Sample Properties
```bash
python manage.py shell
```
```python
from properties.models import Property
from decimal import Decimal

Property.objects.create(
    title="Luxury Villa",
    description="Beautiful villa with ocean view",
    price=Decimal("500000.00"),
    location="Miami"
)

Property.objects.create(
    title="Downtown Apartment",
    description="Modern apartment in city center",
    price=Decimal("250000.00"),
    location="New York"
)
```

### Test Caching

1. **First Request** (Cache Miss):
```bash
curl http://localhost:8000/properties/
```

Check logs - you should see "Cache MISS"

2. **Second Request** (Cache Hit):
```bash
curl http://localhost:8000/properties/
```

Check logs - you should see "Cache HIT"

3. **Check Cache Metrics**:
```bash
curl http://localhost:8000/properties/metrics/
```

### Test Cache Invalidation
```bash
python manage.py shell
```
```python
from properties.models import Property

# Update a property - this should invalidate cache
prop = Property.objects.first()
prop.price = 600000
prop.save()

# Check logs - you should see cache invalidation message
```

## Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Access Redis CLI
```bash
docker exec -it redis_cache redis-cli
```

Inside Redis CLI:
```redis
# Check all keys
KEYS *

# Get cache value
GET property_listings:all_properties

# Get stats
INFO stats
```

### Access PostgreSQL
```bash
docker exec -it postgres_db psql -U postgres -d property_listings_db
```

## Performance Monitoring

### Check Cache Hit Ratio

Visit: `http://localhost:8000/properties/metrics/`

A good hit ratio is > 80%

### View Application Logs
```bash
python manage.py runserver
```

Watch for log messages:
- `Cache HIT for all_properties`
- `Cache MISS for all_properties`
- `Property X created - cache 'all_properties' invalidated`

## Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
docker-compose ps

# Restart Redis
docker-compose restart redis

# Test Redis connection
docker exec -it redis_cache redis-cli ping
```

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Cache Not Working

1. Clear cache:
```bash
python manage.py shell
```
```python
from django.core.cache import cache
cache.clear()
```

2. Restart Redis:
```bash
docker-compose restart redis
```

3. Check `CACHES` configuration in `settings.py`

## Production Considerations

- Use environment variables for sensitive data
- Set `DEBUG = False`
- Configure proper `ALLOWED_HOSTS`
- Use a production-grade Redis instance
- Implement cache monitoring and alerts
- Set appropriate cache timeouts based on data volatility
- Consider using Redis Sentinel for high availability

## Technologies Used

- **Django 4.2**: Web framework
- **PostgreSQL**: Relational database
- **Redis**: Caching layer
- **Docker**: Containerization
- **django-redis**: Redis cache backend
- **psycopg2**: PostgreSQL adapter

## License

[Your License Here]

---

**Project:** ALX Backend Specialization
**Module:** Caching in Django
**Version:** 1.0