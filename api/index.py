import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_portal.settings')

from student_portal.wsgi import application

app = application