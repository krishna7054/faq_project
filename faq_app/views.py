from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import status
from googletrans import Translator
from django.core.cache import cache

translator = Translator()



def home_view(request):
    return render(request,"home.html")

@api_view(['GET', 'POST'])
def get_faqs(request):
    if request.method == 'GET':
        lang = request.GET.get('lang', 'en')
        faqs = FAQ.objects.all()
        formatted_output = []
        
        for faq in faqs:
            # Cache key based on FAQ ID and language
            cache_key_question = f'faq_{faq.id}_question_{lang}'
            cache_key_answer = f'faq_{faq.id}_answer_{lang}'

            # Try to get translated content from cache
            translated_question = cache.get(cache_key_question)
            translated_answer = cache.get(cache_key_answer)

            if not translated_question or not translated_answer:
                # If not cached, translate and store in cache
                translated_question = translator.translate(faq.question, dest=lang).text
                translated_answer = translator.translate(faq.answer, dest=lang).text
                
                # Cache the translations for future use
                cache.set(cache_key_question, translated_question, timeout=86400)  # Cache for 1 day
                cache.set(cache_key_answer, translated_answer, timeout=86400)  # Cache for 1 day

            formatted_output.append({
                'id': faq.id,
                'question': translated_question,
                'answer': translated_answer
            })

        return Response(formatted_output)

    elif request.method == 'POST':
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_translation(question, lang='en'):
    # Check cache for the translated text
    cache_key = f'question_{lang}_{question}'
    translated_text = cache.get(cache_key)
    if not translated_text:
        # If not in cache, perform translation
        translated_text = translator.translate(question, dest=lang).text
        # Cache the result for future use
        cache.set(cache_key, translated_text, timeout=86400)  # Cache for 1 day
    return translated_text
