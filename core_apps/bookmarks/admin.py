"""
Bookmark app admin.
"""
from django.contrib import admin
from .models import Bookmark

admin.site.register(Bookmark)
