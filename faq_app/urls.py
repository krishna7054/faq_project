
from django.urls import path
from .views import get_faqs
urlpatterns = [
   path('api/faqs/', get_faqs, name='get_faqs'),
]
