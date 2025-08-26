from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .forms import AudioUploadForm
from .models import AudioFile
from .audio_processing import AudioStressScorer
import os

# Create a global instance to ensure the scaler is fitted once
scorer = AudioStressScorer()

def home(request):
    form = AudioUploadForm()
    return render(request, 'analyzer/home.html', {'form': form})

def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            
            # Get the full path to the uploaded file
            file_path = os.path.join(settings.MEDIA_ROOT, audio_file.file.name)
            
            # Calculate stress score
            stress_score = scorer.predict_stress(file_path)
            audio_file.stress_score = stress_score
            
            # Get feature breakdown
            feature_breakdown = scorer.explain_stress_score(file_path)
            audio_file.feature_breakdown = {
                feature: float(contribution) for feature, contribution in feature_breakdown
            }
            
            audio_file.save()
            
            return JsonResponse({
                'success': True,
                'score': stress_score,
                'features': audio_file.feature_breakdown
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})