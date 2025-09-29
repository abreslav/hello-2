import json
import logging
import time
from django.utils.deprecation import MiddlewareMixin


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all HTTP requests and responses."""

    def process_request(self, request):
        """Log request details and start timing."""
        request._request_start_time = time.time()
        return None

    def process_response(self, request, response):
        """Log complete request/response information."""
        logger = logging.getLogger('django_app')

        # Calculate processing duration
        end_time = time.time()
        start_time = getattr(request, '_request_start_time', end_time)
        duration = end_time - start_time

        # Get request body size
        request_body_size = len(getattr(request, 'body', b''))

        # Get response body size
        response_body_size = len(getattr(response, 'content', b''))

        # Prepare request headers
        request_headers = {}
        for key, value in request.META.items():
            if key.startswith('HTTP_'):
                # Convert HTTP_HEADER_NAME to Header-Name
                header_name = key[5:].replace('_', '-').title()
                request_headers[header_name] = value
            elif key in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
                request_headers[key.replace('_', '-').title()] = value

        # Prepare response headers
        response_headers = dict(response.items())

        # Create log entry
        log_data = {
            "method": request.method,
            "url": request.build_absolute_uri(),
            "request_headers": request_headers,
            "request_body_size": request_body_size,
            "response_status": response.status_code,
            "response_headers": response_headers,
            "response_body_size": response_body_size,
            "processing_duration": round(duration * 1000, 2)  # in milliseconds
        }

        # Add response body if status is not successful
        if response.status_code >= 400:
            try:
                log_data["response_body"] = response.content.decode('utf-8', errors='ignore')
            except:
                log_data["response_body"] = "<binary content>"

        # Log as JSON
        logger.info(json.dumps(log_data))

        return response