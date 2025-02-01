from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import status
from googletrans import Translator


translator = Translator()




@api_view(['GET', 'POST'])
def get_faqs(request):
    if request.method == 'GET':
        lang = request.GET.get('lang', 'en')
        faqs = FAQ.objects.all()
        formatted_output = []
        
        for faq in faqs:
            
            # Try to get translated content from cache
            translated_question = f'faq_{faq.id}_question_{lang}'
            translated_answer = f'faq_{faq.id}answer{lang}'

            if not translated_question or not translated_answer:
                # If not cached, translate and store in cache
                translated_question = translator.translate(faq.question, dest=lang).text
                translated_answer = translator.translate(faq.answer, dest=lang).text
                
        
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
    
    translated_text = f'question_{lang}_{question}'
    if not translated_text:
        # perform translation
        translated_text = translator.translate(question, dest=lang).text
        
    return translated_text
