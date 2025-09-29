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