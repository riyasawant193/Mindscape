from django.shortcuts import render
from .models import YouTubeVideo
from .summarizer import summarize_transcript  # This is where you'll integrate spaCy or NLTK

def home(request):
    if request.method == 'POST':
        url = request.POST.get('youtube_url')
        summarized_text = summarize_transcript(url)  # Implement this function to summarize the video transcript
        video = YouTubeVideo.objects.create(url=url, summarized_text=summarized_text)
    else:
        video = None
    return render(request, 'summarizer/home.html', {'video': video})
