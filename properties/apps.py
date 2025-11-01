"""
App configuration for properties app.
"""

from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    """
    Configuration for the properties app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import properties.signals  # noqa