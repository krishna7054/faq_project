
from django.urls import path
from .views import get_faqs, homeview
urlpatterns = [
   path('api/faqs/', get_faqs, name='get_faqs'),
   path('',homeview, name='home')
]
