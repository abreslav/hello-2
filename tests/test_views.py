import pytest
from django.test import TestCase, Client
from django.urls import reverse


class TestHomeView(TestCase):
    """Test cases for the home view endpoint."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()

    @pytest.mark.timeout(30)
    def test_home_endpoint(self):
        """
        Test kind: endpoint_tests
        Original method FQN: home
        """
        # Make GET request to home endpoint
        response = self.client.get('/')

        # Verify successful response
        self.assertEqual(response.status_code, 200)

        # Verify content type
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

        # Verify template was rendered correctly
        self.assertContains(response, 'Hello from CodeSpeak!')
        self.assertContains(response, 'Welcome to your Django web application')
        self.assertContains(response, 'Built with Django & Tailwind CSS')

        # Verify HTML structure
        self.assertContains(response, '<!DOCTYPE html>')
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, '<title>HelloWorld - CodeSpeak</title>')

        # Verify CSS classes are present (indicating proper template rendering)
        self.assertContains(response, 'bg-gradient-to-br')
        self.assertContains(response, 'codespeak-blue')
        self.assertContains(response, 'codespeak-purple')

    @pytest.mark.timeout(30)
    def test_home_endpoint_using_reverse(self):
        """
        Test kind: endpoint_tests
        Original method FQN: home
        """
        # Test using URL name resolution
        url = reverse('home')
        response = self.client.get(url)

        # Verify successful response
        self.assertEqual(response.status_code, 200)

        # Verify template used
        self.assertTemplateUsed(response, 'django_app/home.html')

    @pytest.mark.timeout(30)
    def test_home_endpoint_post_method(self):
        """
        Test kind: endpoint_tests
        Original method FQN: home
        """
        # Test POST request to home endpoint (should still work as Django views handle all HTTP methods by default)
        response = self.client.post('/')

        # Verify successful response (Django view should handle POST the same as GET)
        self.assertEqual(response.status_code, 200)

        # Verify same template content is returned
        self.assertContains(response, 'Hello from CodeSpeak!')

    @pytest.mark.timeout(30)
    def test_home_endpoint_head_method(self):
        """
        Test kind: endpoint_tests
        Original method FQN: home
        """
        # Test HEAD request to home endpoint
        response = self.client.head('/')

        # Verify successful response with no content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 0)

    @pytest.mark.timeout(30)
    def test_home_endpoint_with_query_params(self):
        """
        Test kind: endpoint_tests
        Original method FQN: home
        """
        # Test GET request with query parameters
        response = self.client.get('/?param=value&test=123')

        # Verify successful response (query params should be ignored by the view)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello from CodeSpeak!')


class TestStatusView(TestCase):
    """Test cases for the status view endpoint."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()

    @pytest.mark.timeout(30)
    def test_status_endpoint(self):
        """
        Test kind: endpoint_tests
        Original method FQN: status
        """
        # Make GET request to status endpoint
        response = self.client.get('/status')

        # Verify successful response
        self.assertEqual(response.status_code, 200)

        # Verify content type
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

        # Verify template was used correctly
        self.assertTemplateUsed(response, 'django_app/status.html')

        # Verify required content is present
        self.assertContains(response, 'System Status')
        self.assertContains(response, 'Operating System')
        self.assertContains(response, 'Current Time')
        self.assertContains(response, 'CPU Usage')
        self.assertContains(response, 'Memory Usage')

        # Verify HTML structure
        self.assertContains(response, '<!DOCTYPE html>')
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, '<title>System Status - CodeSpeak</title>')

        # Verify CSS classes are present (indicating proper template rendering)
        self.assertContains(response, 'bg-gradient-to-br')
        self.assertContains(response, 'codespeak-blue')
        self.assertContains(response, 'codespeak-purple')

        # Verify context data is rendered (check that variables are not empty)
        content = response.content.decode()
        # OS name should be present and not be the template variable
        self.assertNotIn('{{ os_name }}', content)
        self.assertNotIn('{{ os_version }}', content)
        self.assertNotIn('{{ current_datetime }}', content)
        self.assertNotIn('{{ cpu_usage }}', content)
        self.assertNotIn('{{ memory_usage }}', content)

    @pytest.mark.timeout(30)
    def test_status_endpoint_using_reverse(self):
        """
        Test kind: endpoint_tests
        Original method FQN: status
        """
        # Test using URL name resolution
        url = reverse('status')
        response = self.client.get(url)

        # Verify successful response
        self.assertEqual(response.status_code, 200)

        # Verify template used
        self.assertTemplateUsed(response, 'django_app/status.html')

    @pytest.mark.timeout(30)
    def test_status_endpoint_context_data(self):
        """
        Test kind: endpoint_tests
        Original method FQN: status
        """
        # Make GET request to status endpoint
        response = self.client.get('/status')

        # Verify successful response
        self.assertEqual(response.status_code, 200)

        # Verify context contains expected keys
        context = response.context
        self.assertIn('os_name', context)
        self.assertIn('os_version', context)
        self.assertIn('current_datetime', context)
        self.assertIn('cpu_usage', context)
        self.assertIn('memory_usage', context)

        # Verify context data types and basic validation
        self.assertIsInstance(context['os_name'], str)
        self.assertIsInstance(context['os_version'], str)
        self.assertIsInstance(context['current_datetime'], str)
        self.assertIsInstance(context['cpu_usage'], float)
        self.assertIsInstance(context['memory_usage'], float)

        # Verify values are reasonable
        self.assertGreater(len(context['os_name']), 0)
        self.assertGreater(len(context['os_version']), 0)
        self.assertGreater(len(context['current_datetime']), 0)
        self.assertGreaterEqual(context['cpu_usage'], 0.0)
        self.assertLessEqual(context['cpu_usage'], 100.0)
        self.assertGreaterEqual(context['memory_usage'], 0.0)
        self.assertLessEqual(context['memory_usage'], 100.0)

    @pytest.mark.timeout(30)
    def test_status_endpoint_post_method(self):
        """
        Test kind: endpoint_tests
        Original method FQN: status
        """
        # Test POST request to status endpoint (should still work as Django views handle all HTTP methods by default)
        response = self.client.post('/status')

        # Verify successful response (Django view should handle POST the same as GET)
        self.assertEqual(response.status_code, 200)

        # Verify same template content is returned
        self.assertContains(response, 'System Status')

    @pytest.mark.timeout(30)
    def test_status_endpoint_head_method(self):
        """
        Test kind: endpoint_tests
        Original method FQN: status
        """
        # Test HEAD request to status endpoint
        response = self.client.head('/status')

        # Verify successful response with no content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 0)

    @pytest.mark.timeout(30)
    def test_status_endpoint_with_query_params(self):
        """
        Test kind: endpoint_tests
        Original method FQN: status
        """
        # Test GET request with query parameters
        response = self.client.get('/status?param=value&test=123')

        # Verify successful response (query params should be ignored by the view)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'System Status')