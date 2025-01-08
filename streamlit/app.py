import streamlit as st
from PIL import Image
from gtts import gTTS
import os
import io
import cv2
import numpy as np

st.set_page_config(page_title="Streamlit Sidebar Example", layout="wide")
st.title("My Website")

# Tabs
face, sketch, tts = st.tabs(["Face Recognition", "Convert to Sketch", "Text-to-speech"])

def detect_faces(img_data):
    gray_img = cv2.cvtColor(np.frombuffer(img_data, np.uint8), cv2.COLOR_RGB2BGR)
    # gray_img = cv2.normalize(gray_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

    print(faces)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img_data, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return img_data

# Face recognition tab
with face:
    st.write("Upload an image to detect faces in it and draw rectangles around them.")
    myimg = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    if myimg:
        img_data = myimg.read()
        processed_img = detect_faces(img_data)
        if processed_img is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(Image.open(io.BytesIO(img_data)), caption="Original Photo", use_container_width=True)
            with col2:
                st.image(processed_img, caption="Detected Faces", use_container_width=True)

def convert_to_sketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred_image = cv2.GaussianBlur(inverted_image, (111, 111), 0)
    # Blend the grayscale and blurred images
    sketch = cv2.divide(gray_image, 255 - blurred_image, scale=256)

    return sketch

# Convert image to sketch tab
with sketch:
    st.write("Upload an image to convert it into a pencil sketch.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Original Image", use_container_width=True)
        with col2:
            sketch = convert_to_sketch(image)
            st.image(sketch, caption="Pencil Sketch", use_container_width=True)

# Text-to-speech tab
with tts:
    st.write("Text-to-Speech Converter")
    text = st.text_area("Enter the text you want to convert to speech:")
    language = st.selectbox("Select language", ["en", "es", "fr", "de", "it"])
    
    if st.button("Convert to Speech"):
        if text:
            tts = gTTS(text=text, lang=language, slow=False)
            audio_file = "output.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")
            os.remove(audio_file)
        else:
            st.warning("Please enter some text to convert.")
