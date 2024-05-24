import streamlit as st
import sqlite3
import os
from PIL import Image
import numpy as np
import cv2

st.title("Imagez")
st.caption("Image recognition except it's based on images people submit to this model, nothing else")

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = None

def handle_button_click(button_name):
    st.session_state.button_clicked = button_name

if st.button('Label'):
    handle_button_click('Label')

if st.button('Search'):
    handle_button_click('Search')


uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png"])

def detect_and_annotate_image(image):
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)

    annotated_image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    return annotated_image

if st.session_state.button_clicked == 'Label':
    if uploaded_file is not None:
        st.write("Photo uploaded")
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Photo', use_column_width=True)
        label = st.text_input("Enter a label for the image:")
        if label:
            annotated_image = detect_and_annotate_image(image)
            st.image(annotated_image, caption=f'Labeled: {label}', use_column_width=True)
            if st.button('Confirm'):
                image_path = os.path.join("uploaded_images", uploaded_file.name)
                annotated_image_path = os.path.join("annotated_images", f"annotated_{uploaded_file.name}")
                image.save(image_path)
                annotated_image.save(annotated_image_path)

                conn = sqlite3.connect('image_recognition.db')
                c = conn.cursor()
                c.execute('INSERT INTO images (label, image_path, annotated_image_path) VALUES (?, ?, ?)', 
                          (label, image_path, annotated_image_path))
                conn.commit()
                conn.close()
                st.success("Label saved successfully!")
    else:
        st.warning("Please upload an image first.")

def reset_button_state():
    st.session_state.button_clicked = None

if st.button('Reset'):
    reset_button_state()

if not os.path.exists('uploaded_images'):
    os.makedirs('uploaded_images')
if not os.path.exists('annotated_images'):
    os.makedirs('annotated_images')
