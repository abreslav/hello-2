from django.shortcuts import render


def home(request):
    """Home page view that displays the HelloWorld greeting."""
    return render(request, 'django_app/home.html')
