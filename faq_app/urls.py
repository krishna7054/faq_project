
from django.urls import path
from .views import faq_handler, homeview
urlpatterns = [
   path('api/faqs/', faq_handler, name='get_faqs'),
   path('',homeview, name='home'),
    path('api/faqs/<int:faq_id>/', faq_handler, name='faq-detail'),
]
