from django.shortcuts import render
from .firebase import database
import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.conf import settings
import requests
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
@api_view(['POST'])

def home(request):
    # Exemple : Ajouter des données à Firebase
    if request.method == 'POST':
        name = request.POST.get('name')
        stack = request.POST.get('stack')
        data = {"name": name, "stack": stack}
        database.child("users").push(data) # Ajoute les données dans la collection "users"
    
    # Exemple : Lire des données depuis Firebase
    users = database.child("users").get().val() # Récupère tous les utilisateurs
    return render(request, 'myapp/index.html', {'users': users})
# Create your views here.

def myapp(request):
    prompt = request.data.get('prompt')
    if not prompt:
        return Response({'error': 'Prompt is required'}, status=400)

    try:
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = ai_response['choices'][0]['message']['content']

        message = Message.objects.create(prompt=prompt, response=response_text)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def chat_view(request):
    prompt = request.data.get('prompt', '')
    if not prompt:
        return Response({'error': 'Prompt is required'}, status=400)

    api_key = settings.GEMINI_API_KEY
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}'

    payload = {
        "prompt": {
            "text": prompt
        },
        "temperature": 0.7,
        "candidateCount": 1,
        "maxOutputTokens": 1024,
        "topP": 0.8,
        "topK": 40,
    }

    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        # Extract generated text (adjust this if Gemini API response format changes)
        generated_text = data['candidates'][0]['output']
        return Response({'response': generated_text})
    except Exception as e:
        return Response({'error': str(e)}, status=500)