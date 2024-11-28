import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize global variables
isTranslateOn = False
translator = Translator()  # Initialize the translator module.
pygame.mixer.init()  # Initialize the mixer module.

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src='{}'.format(from_language), dest='{}'.format(to_language))

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang='{}'.format(to_language), slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")  # Load a sound.
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    
    global isTranslateOn
    
    while isTranslateOn:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.markdown("<h3 style='color:blue;'>🎙️ Listening...</h3>", unsafe_allow_html=True)
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            output_placeholder.markdown("<h3 style='color:orange;'>⏳ Processing...</h3>", unsafe_allow_html=True)
            spoken_text = rec.recognize_google(audio, language='{}'.format(from_language))
            
            output_placeholder.markdown("<h3 style='color:green;'>🌍 Translating...</h3>", unsafe_allow_html=True)
            translated_text = translator_function(spoken_text, from_language, to_language)

            output_placeholder.markdown(f"<h3 style='color:green;'>🔊 Translation: {translated_text.text}</h3>", unsafe_allow_html=True)
            text_to_voice(translated_text.text, to_language)
    
        except Exception as e:
            output_placeholder.error(f"Error: {str(e)}")

# UI layout
st.title("🌐 Language Translator")

# Sidebar for language selection
st.sidebar.markdown("## Select Languages")

from_language_name = st.sidebar.selectbox("🎤 Source Language:", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"))
to_language_name = st.sidebar.selectbox("🔊 Target Language:", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("spanish"))

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Instruction text
st.markdown("""
<style>
    .instructions {
        background-color: black;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 18px;
    }
</style>
<div class="instructions">
    1. Select the Source and Target languages.<br>
    2. Press "Start" to begin translation.<br>
    3. Press "Stop" to end the translation process.
</div>
""", unsafe_allow_html=True)

# Buttons for Start and Stop
col1, col2 = st.columns(2)
with col1:
    start_button = st.button("🟢 Start", use_container_width=True)
with col2:
    stop_button = st.button("🔴 Stop", use_container_width=True)

# Output section
output_placeholder = st.empty()

# Check if "Start" button is clicked
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        main_process(output_placeholder, from_language, to_language)

# Check if "Stop" button is clicked
if stop_button:
    isTranslateOn = False
    output_placeholder.markdown("<h3 style='color:red;'>🚫 Translation Stopped</h3>", unsafe_allow_html=True)
