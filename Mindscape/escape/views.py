from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.
def homepage(request):
    return render(request, 'escape/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {'registerform':form}
    return render(request, 'escape/register.html', context=context)

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'loginform':form}
    return render(request, 'escape/login.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect("")

@login_required(login_url="login")
def dashboard(request):
    return render(request, 'escape/dashboard.html')

# views.py
from django.http import JsonResponse

from transformers import pipeline
import numpy as np


transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-medium.en")

def transcribe_audio(stream, new_chunk):
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y
    return stream, transcriber({"sampling_rate": sr, "raw": stream})["text"]


def process_audio(request):
    if request.method == 'POST':
        audio_data = request.POST.get('audio')
        # Process the audio data (e.g., transcribe with Whisper model)
        transcription = transcribe_audio(audio_data)
        return JsonResponse({'transcription': transcription})
    else:
        return JsonResponse({'error': 'Invalid request method'})



def study_set(request):
    return render(request, 'escape/study_set.html')

def import_materials(request):
    return render(request, 'escape/import_materials.html')

def transcription(request):
    return render(request, 'escape/transcription.html')

def test(request):
    return render(request, 'escape/test.html')
