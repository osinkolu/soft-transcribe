import streamlit as st
from transformers import pipeline
import requests
import gdown
from pytube import YouTube
import os, time

def download_file_from_url(url, output_folder="."):
    response = requests.get(url)
    file_path = os.path.join(output_folder, "downloaded_file")
    
    with open(file_path, "wb") as file:
        file.write(response.content)
    
    return file_path

def download_file_from_google_drive(gdrive_link, file_type, output_folder="."):
    drive_id = gdrive_link.split("/")[-2]
    file_path = os.path.join(output_folder, "downloaded_file."+file_type)
    file_url = "https://drive.google.com/uc?id=" + drive_id
    gdown.download(file_url, file_path, quiet=False)
    return file_path

def download_audio_from_youtube(youtube_link, output_folder="."):
    yt = YouTube(youtube_link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    file_path = os.path.join(output_folder, "downloaded_file.mp3")
    audio_stream.download(output_path = output_folder, filename=file_path)
    return file_path

def transcribe_audio(input_data, method):
    whisper = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")
    
    if method == "URL":
        try:
            file_path = download_file_from_url(input_data)
            st.audio(file_path, format="audio/" + file_path.split(".")[-1], start_time=0)
        except Exception:
            st.warning("Something is wrong with your download URL")
    elif method == "Google Drive":
        try:
            file_extension = st.selectbox("Select File Extension", ["mp3", "wav", "ogg", "flac", "aac", "m4a"])
            file_path = download_file_from_google_drive(input_data, file_extension)
        except Exception:
            st.warning("There was an issue, kindly confirm your link allows access for all, and copy it as it is from drive")
        st.audio(file_path, format="audio/" + file_extension, start_time=0)

    elif method == "YouTube":
        try:
            file_path = download_audio_from_youtube(input_data)
        except Exception:
            st.warning("I couldn't pull out your audio from the Youtube video. There's probably some restrictions from Youtube")
            st.audio(file_path, format="audio/" + file_path.split(".")[-1], start_time=0)
    elif method == "File Upload":
        file_path = input_data
        st.audio(file_path, start_time=0)
        file_path = input_data.read() #pass in the numpy array instead.
    else:
        raise ValueError("Invalid transcription method")
    
    st.text("Listen to the uploaded audio before transcribing:")
    if st.button("Transcribe"):
        # Record the start time
        start_time = time.time()
        st.text("Transcribing... This may take a moment.")
        try:
            transcription = whisper(file_path,  max_new_tokens=100, chunk_length_s=30)['text']
            # Record the end time
            end_time = time.time()
            # Calculate and print the elapsed time in seconds
            elapsed_time = end_time - start_time
            st.success(f"Transcription complete 🎊, the computation took: {elapsed_time:.4f} seconds")
            st.write(transcription)
        except:
            st.error("So sorry 😔, I couldn't transcribe the audio, something is wrong. Ensure you select the correct Transcription Method")

def home_page():
    st.title("Soft Transcribe - Audio Transcription App")
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg", "flac", "aac", "m4a"])
    transcription_mode = st.selectbox("Select Transcription Method", ["File Upload", "URL", "Google Drive", "YouTube"])
    
    if transcription_mode == "File Upload" and uploaded_file:
        transcribe_audio(uploaded_file, method="File Upload")
    elif transcription_mode in ["URL", "Google Drive", "YouTube"]:
        link_label = "Enter the link"
        if transcription_mode == "Google Drive":
            link_label = "Enter the Google Drive link (shareable link)"
        elif transcription_mode == "YouTube":
            link_label = "Enter the YouTube video link"
        
        audio_link = st.text_input(link_label)
        
        if audio_link:
            transcribe_audio(audio_link, method=transcription_mode)

def about_page():
    st.title("About Soft Transcribe")
    st.write("Soft Transcribe is a simple audio transcription app using Hugging Face's Whisper ASR model. Built with ❤️ for Oreoluwa")

def main():
    st.sidebar.title("Navigation")
    pages = ["Home", "About"]
    choice = st.sidebar.radio("Go to", pages)

    if choice == "Home":
        home_page()
    elif choice == "About":
        about_page()

if __name__ == "__main__":
    main()
