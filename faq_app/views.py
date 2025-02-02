from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import status
from googletrans import Translator
from django.core.cache import cache
from .forms import faqFrom

translator = Translator()

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def faq_handler(request, faq_id=None):
    if request.method == 'GET':
        lang = request.GET.get('lang', 'en')
        faqs = FAQ.objects.all()
        formatted_output = []
        
        for faq in faqs:
            cache_key_question = f'faq_{faq.id}_question_{lang}'
            cache_key_answer = f'faq_{faq.id}_answer_{lang}'

            translated_question = cache.get(cache_key_question)
            translated_answer = cache.get(cache_key_answer)

            if not translated_question or not translated_answer:
                translated_question = translator.translate(faq.question, dest=lang).text
                translated_answer = translator.translate(faq.answer, dest=lang).text
                cache.set(cache_key_question, translated_question, timeout=86400)
                cache.set(cache_key_answer, translated_answer, timeout=86400)

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

    elif request.method == 'PUT' and faq_id:
        faq = get_object_or_404(FAQ, id=faq_id)
        serializer = FAQSerializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and faq_id:
        faq = get_object_or_404(FAQ, id=faq_id)
        faq.delete()
        return Response({'message': 'FAQ deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

def get_translation(question, lang='en'):
    cache_key = f'question_{lang}_{question}'
    translated_text = cache.get(cache_key)
    if not translated_text:
        translated_text = translator.translate(question, dest=lang).text
        cache.set(cache_key, translated_text, timeout=86400)
    return translated_text

def homeview(request):
    form = faqFrom()
    if request.method == 'POST':
        form = faqFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'home.html', {'form': form})
