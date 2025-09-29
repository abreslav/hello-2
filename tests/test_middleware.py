import json
import logging
import time
from unittest.mock import Mock, patch, MagicMock
import pytest
from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from django_app.middleware import RequestLoggingMiddleware


class TestRequestLoggingMiddleware(TestCase):
    """Test cases for RequestLoggingMiddleware class."""

    def setUp(self):
        """Set up test fixtures."""
        self.middleware = RequestLoggingMiddleware(get_response=lambda request: HttpResponse())

    @pytest.mark.timeout(30)
    def test_process_request(self):
        """
        Test kind: unit_tests
        Original method FQN: RequestLoggingMiddleware.process_request
        """
        # Create a mock request
        request = Mock(spec=HttpRequest)

        # Call the method
        with patch('time.time', return_value=1234567890.123):
            result = self.middleware.process_request(request)

        # Verify the result is None (middleware continues processing)
        self.assertIsNone(result)

        # Verify that the request start time was set
        self.assertEqual(request._request_start_time, 1234567890.123)

    @pytest.mark.timeout(30)
    @patch('django_app.middleware.logging.getLogger')
    @patch('time.time')
    def test_process_response_basic(self, mock_time, mock_get_logger):
        """
        Test kind: unit_tests
        Original method FQN: RequestLoggingMiddleware.process_response
        """
        # Set up mocks
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_time.return_value = 1234567891.123  # End time

        # Create mock request and response
        request = Mock(spec=HttpRequest)
        request._request_start_time = 1234567890.123  # Start time
        request.method = 'GET'
        request.build_absolute_uri.return_value = 'http://testserver/'
        request.META = {
            'HTTP_USER_AGENT': 'TestAgent',
            'HTTP_ACCEPT': 'text/html',
            'CONTENT_TYPE': 'application/json',
            'CONTENT_LENGTH': '100'
        }
        request.body = b'test body'

        response = Mock(spec=HttpResponse)
        response.status_code = 200
        response.content = b'test response'
        response.items.return_value = [('Content-Type', 'text/html')]

        # Call the method
        result = self.middleware.process_response(request, response)

        # Verify the response is returned unchanged
        self.assertEqual(result, response)

        # Verify logger was called
        mock_get_logger.assert_called_once_with('django_app')
        mock_logger.info.assert_called_once()

        # Parse the logged JSON data
        logged_json = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_json)

        # Verify log data structure
        self.assertEqual(log_data['method'], 'GET')
        self.assertEqual(log_data['url'], 'http://testserver/')
        self.assertEqual(log_data['response_status'], 200)
        self.assertEqual(log_data['processing_duration'], 1000.0)  # 1 second in ms
        self.assertEqual(log_data['request_body_size'], 9)  # len(b'test body')
        self.assertEqual(log_data['response_body_size'], 13)  # len(b'test response')

        # Verify headers processing
        expected_request_headers = {
            'User-Agent': 'TestAgent',
            'Accept': 'text/html',
            'Content-Type': 'application/json',
            'Content-Length': '100'
        }
        self.assertEqual(log_data['request_headers'], expected_request_headers)
        self.assertEqual(log_data['response_headers'], {'Content-Type': 'text/html'})

    @pytest.mark.timeout(30)
    @patch('django_app.middleware.logging.getLogger')
    @patch('time.time')
    def test_process_response_error_status(self, mock_time, mock_get_logger):
        """
        Test kind: unit_tests
        Original method FQN: RequestLoggingMiddleware.process_response
        """
        # Set up mocks for error response
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_time.return_value = 1234567891.123

        request = Mock(spec=HttpRequest)
        request._request_start_time = 1234567890.123
        request.method = 'POST'
        request.build_absolute_uri.return_value = 'http://testserver/error'
        request.META = {}
        request.body = b''

        response = Mock(spec=HttpResponse)
        response.status_code = 404
        response.content = b'Not Found'
        response.items.return_value = []

        # Call the method
        result = self.middleware.process_response(request, response)

        # Verify the response is returned
        self.assertEqual(result, response)

        # Parse the logged JSON data
        logged_json = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_json)

        # Verify error status includes response body
        self.assertEqual(log_data['response_status'], 404)
        self.assertEqual(log_data['response_body'], 'Not Found')

    @pytest.mark.timeout(30)
    @patch('django_app.middleware.logging.getLogger')
    @patch('time.time')
    def test_process_response_missing_start_time(self, mock_time, mock_get_logger):
        """
        Test kind: unit_tests
        Original method FQN: RequestLoggingMiddleware.process_response
        """
        # Set up mocks
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_time.return_value = 1234567891.123

        # Create request without _request_start_time
        request = Mock(spec=HttpRequest)
        # Don't set request._request_start_time
        request.method = 'GET'
        request.build_absolute_uri.return_value = 'http://testserver/'
        request.META = {}
        request.body = b''

        response = Mock(spec=HttpResponse)
        response.status_code = 200
        response.content = b''
        response.items.return_value = []

        # Call the method
        result = self.middleware.process_response(request, response)

        # Verify the response is returned
        self.assertEqual(result, response)

        # Parse the logged JSON data
        logged_json = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_json)

        # Verify duration is 0 when start time is missing
        self.assertEqual(log_data['processing_duration'], 0.0)

    @pytest.mark.timeout(30)
    @patch('django_app.middleware.logging.getLogger')
    @patch('time.time')
    def test_process_response_binary_content(self, mock_time, mock_get_logger):
        """
        Test kind: unit_tests
        Original method FQN: RequestLoggingMiddleware.process_response
        """
        # Set up mocks
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_time.return_value = 1234567891.123

        request = Mock(spec=HttpRequest)
        request._request_start_time = 1234567890.123
        request.method = 'GET'
        request.build_absolute_uri.return_value = 'http://testserver/'
        request.META = {}
        request.body = b''

        # Create response with content that will trigger the except block
        response = Mock(spec=HttpResponse)
        response.status_code = 500
        response.items.return_value = []

        # Create a mock content object that raises UnicodeDecodeError when decode is called
        mock_content = Mock()
        mock_content.decode.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid')
        response.content = mock_content

        # Call the method
        result = self.middleware.process_response(request, response)

        # Verify the response is returned
        self.assertEqual(result, response)

        # Parse the logged JSON data
        logged_json = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_json)

        # Verify binary content handling
        self.assertEqual(log_data['response_body'], '<binary content>')