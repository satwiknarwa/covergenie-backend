from django.urls import path
from .views import CoverLetterGenerator

urlpatterns = [
    path('generate-cover-letter/', CoverLetterGenerator.as_view(), name='generate_cover_letter'),
]
