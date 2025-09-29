from django.shortcuts import render
import platform
import datetime
import psutil


def home(request):
    """Home page view that displays the HelloWorld greeting."""
    return render(request, 'django_app/home.html')


def status(request):
    """System status page view that displays system information."""
    context = {
        'os_name': platform.system(),
        'os_version': platform.release(),
        'current_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
    }
    return render(request, 'django_app/status.html', context)
