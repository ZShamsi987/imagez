import streamlit as st
import sqlite3
import os
from PIL import Image
import numpy as np
import cv2

# Set the title and caption
st.title("Imagez")
st.caption("Image recognition except it's based on images people submit to this model, nothing else")

# Create a session state variable to keep track of which button was clicked
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = None

# Function to handle button clicks
def handle_button_click(button_name):
    st.session_state.button_clicked = button_name

# Add buttons for Label and Search
if st.button('Label'):
    handle_button_click('Label')

if st.button('Search'):
    handle_button_click('Search')

# File uploader for uploading photos
uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png"])

# Function to detect and draw bounding box around the main object
def detect_and_annotate_image(image):
    # Convert to OpenCV format
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Detect object (simple approach using contours)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        # Draw bounding box
        cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Convert back to PIL format
    annotated_image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    return annotated_image

# Handle the Label button click
if st.session_state.button_clicked == 'Label':
    if uploaded_file is not None:
        st.write("Photo uploaded")
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Photo', use_column_width=True)
        # Text box for labeling the image
        label = st.text_input("Enter a label for the image:")
        if label:
            # Annotate the image
            annotated_image = detect_and_annotate_image(image)
            st.image(annotated_image, caption=f'Labeled: {label}', use_column_width=True)
            if st.button('Confirm'):
                # Ensure directories exist
                if not os.path.exists('uploaded_images'):
                    os.makedirs('uploaded_images')
                if not os.path.exists('annotated_images'):
                    os.makedirs('annotated_images')

                # Save the original and annotated images
                image_path = os.path.join("uploaded_images", uploaded_file.name)
                annotated_image_path = os.path.join("annotated_images", f"annotated_{uploaded_file.name}")
                image.save(image_path)
                annotated_image.save(annotated_image_path)

                # Save to database
                conn = sqlite3.connect('image_recognition.db')
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS images 
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              label TEXT, 
                              image_path TEXT, 
                              annotated_image_path TEXT)''')
                c.execute('INSERT INTO images (label, image_path, annotated_image_path) VALUES (?, ?, ?)', 
                          (label, image_path, annotated_image_path))
                conn.commit()
                conn.close()
                st.success("Label saved successfully!")
    else:
        st.warning("Please upload an image first.")

# To reset the button click state
def reset_button_state():
    st.session_state.button_clicked = None

# Provide a reset button to go back to the initial state
if st.button('Reset'):
    reset_button_state()
