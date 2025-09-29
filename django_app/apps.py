import atexit
import logging
from django.apps import AppConfig


class DjangoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app'

    def ready(self):
        """Configure logging when the app is ready."""
        # Get logger for this app
        logger = logging.getLogger('django_app')

        # Log server start
        logger.info("Server started successfully")

        # Register shutdown handler
        atexit.register(self._log_shutdown)

    def _log_shutdown(self):
        """Log server shutdown."""
        logger = logging.getLogger('django_app')
        logger.info("Stopping server")
