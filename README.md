# Soft Transcribe - Audio Transcription App

Deploy link: https://soft-transcribe.streamlit.app/

Soft Transcribe is a simple audio transcription app that allows users to transcribe audio files using Hugging Face's Whisper ASR model. The app supports various methods of providing audio data, including file upload, URL, Google Drive link, and YouTube video link.

## Usage

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the app:
```
streamlit run app.py
```

3. Open the provided Streamlit URL in your browser to access the application.

## Features
* File Upload: Upload an audio file directly to the application for transcription.

* URL: Provide a direct link to an audio file for transcription.

* Google Drive: Enter a Google Drive shareable link to transcribe the audio.

* YouTube: Input a YouTube video link to transcribe the audio.

* Audio Playback: Listen to the uploaded or downloaded audio before transcribing.

## Acknowledgments
This application uses Hugging Face's Whisper ASR model for automatic speech recognition. Special thanks to Hugging Face for providing state-of-the-art NLP models and transformers. Oreoluwa inspired creating this app.

## License
This project is licensed under the MIT License.

