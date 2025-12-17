"""
WSGI config for autoparts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from waitress import serve
from autoparts.wsgi import application  # Replace 'myproject' with your project name


from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=80)  # Bind to all interfaces and port 8000
