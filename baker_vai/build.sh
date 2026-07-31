#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser if it doesn't exist yet
python manage.py shell -c "
from django.contrib.auth.models import User
import os
u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'shawon')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'shawon')
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, '', p)
    print(f'Superuser \"{u}\" created.')
else:
    print(f'Superuser \"{u}\" already exists.')
"
