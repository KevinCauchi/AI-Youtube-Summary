from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from pytube import YouTube
import os
import assemblyai as aai

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_summary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link =  data['link']
            return JsonResponse({'content': yt_link})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid Data Sent'}, status= 400)
        
        #get tittle
        title = yt_title(yt_link)
        #get transcript

        #use open ai to generate summary 
        #save article to db
        #retutn summary as response

    else:
        return JsonResponse({'error': 'Invalid Request Method'}, status= 405)
    
    def yt_title(link):
        yt = YouTube(link)
        title = yt.title
        return title
    
    def download_audio(link):
        yt = Youtube(link)
        video = yt.streams.filter(only_audio=True).first()
        out_file=video.download(output_path=settings.MEDIA_ROOT)
        base, ext =os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file

    def get_transcription(link):
         audio_file = download_audio(link)
         aai.settings.api_key = apii
    


def user_login (request):
    if request.method =='POST':
        username = request.POST['username']
        password =request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid Username or Password"
            return render(request, 'login.html', {'error_message':error_message})

    return render(request, 'login.html')

def user_signup (request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password =request.POST['password']
        repeatPassword=request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                login(request, user)
                return redirect ('/')
            except:
                error_message = 'Error Creating Account'
                return render(request, 'signup.html' ,{'error_message':error_message})
        else:
            error_message = 'Password do not match.'
            return render(request, 'signup.html' ,{'error_message':error_message})

    return render(request, 'signup.html')

def user_logout (request):
    logout(request)
    return redirect('/')