import tensorflow as tf
import pandas as pd
import numpy as np
import speech_recognition as sr
import streamlit as st
from PIL import Image
from transformers import pipeline
model = tf.keras.models.load_model('xcep.h5')
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

st.set_page_config(
    page_title="Emotion recognition",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://mail.google.com/mail",
        'About': "# There is nothing here."
    }
)


def import_and_predict(img, model):
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.image.central_crop(img, 0.5)
    img = tf.image.resize(img, [48, 48])
    img = tf.image.rgb_to_grayscale(img)
    img = tf.expand_dims(img, axis=0)
    img /= 127.5
    img -= 1.
    prediction = model.predict(img)
    return prediction


if 'account' not in st.session_state:
    st.session_state.account = dict()
st.write("""
         # Emotion recognition
         """
         )
st.write("This is a ML web app to recognize your emotion")
if 'img' not in st.session_state:
    st.session_state.img = False
if 'spe' not in st.session_state:
    st.session_state.spe = False
press = st.button('Take a photo')
press2 = st.button("Say something")
if press:
    st.session_state.img = True
    # myObj = {"action":"registration","email":email};
if press2:
    st.session_state.spe = True
if st.session_state.img:


    file = st.camera_input("Take a Picture")
    # file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

    if file is None:
        st.text("Please upload an image file")
    else:
        # myObj = {"action":"photo","email":email};

        image = Image.open(file)
        st.image(image, use_column_width=False)
        res = import_and_predict(image, model)

        if res.argmax() ==0:
            st.write("anger")

        elif res.argmax() ==1:
            st.write("disgust")
        elif res.argmax() == 2:
            st.write("fear")
        elif res.argmax() == 3:
            st.write("happiness")
        elif res.argmax() == 4:
            st.write("sadness")
        elif res.argmax() == 5:
            st.write("surprise")
        elif res.argmax() == 6:
            st.write("neutral")

if st.session_state.spe:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        st.write("Beginning...")
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data, language='en-US', show_all=True)
        if len(text)!=0:
            st.write("You are saying:",text['alternative'][0]['transcript'])
            emotion_labels = emotion(text['alternative'][0]['transcript'])
            st.write("Your emotion is:", emotion_labels[0]["label"])
