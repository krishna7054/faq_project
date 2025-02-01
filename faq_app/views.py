from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import status

@api_view(['GET', 'POST'])
def get_faqs(request):
    if request.method == 'GET':
        lang = request.GET.get('lang', 'en')
        faqs = FAQ.objects.all()
        formatted_output = []
        
        for faq in faqs:
          
            
            question = f'faq_{faq.id}_question_{lang}'
            answer = f'faq_{faq.id}answer{lang}'

            formatted_output.append({
                'id': faq.id,
                'question': question,
                'answer': answer
            })

        return Response(formatted_output)

    elif request.method == 'POST':
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

