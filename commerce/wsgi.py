"""
WSGI config for commerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')

#Initialize the database in /tmp if it does not exist
# db_path = '/tmp/db.sqlite3'
# if not os.path.exists(db_path):
#     try:
#         call_command('migrate')
#     except Exception as e:
#         import sys
#         sys.stderr.write(f"Error running migrations: {e}\n")

# Initialize database in /tmp if it does not exist
# db_path = '/tmp/db.sqlite3'
# if not os.path.exists(db_path):
#     from django.core.management import call_command
#     call_command('migrate')

application = get_wsgi_application()
