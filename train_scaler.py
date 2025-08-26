import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('C:/Users/acer/Desktop/audio_stress_analyzer/audio_stress_analyzer')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stress_analyzer.settings')
django.setup()

from analyzer.audio_processing import AudioStressScorer

def main():
    # Initialize scorer
    scorer = AudioStressScorer()
    
    # Get audio files from a directory
    audio_files = []
    audio_dir = os.path.join(os.path.dirname(__file__), 'sample_audio')
    
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        print(f"Created directory {audio_dir}. Please add some audio files and run again.")
        return
    
    for file in os.listdir(audio_dir):
        if file.endswith(('.wav', '.mp3', '.flac')):
            audio_files.append(os.path.join(audio_dir, file))
    
    if not audio_files:
        print("No audio files found in sample_audio directory!")
        print("Please add some .wav, .mp3, or .flac files and try again.")
        return
    
    print(f"Found {len(audio_files)} audio files")
    
    # Fit the scaler with real data
    scorer.fit(audio_files)
    print("Scaler fitted successfully!")

if __name__ == "__main__":
    main()