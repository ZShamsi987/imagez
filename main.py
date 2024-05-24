import streamlit as st

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

if st.session_state.button_clicked == 'Label':
    if uploaded_file is not None:
        st.write("Photo uploaded")
        st.image(uploaded_file, caption='Uploaded Photo', use_column_width=True)
        label = st.text_input("Enter a label for the image:")
        if label:
            st.write(f"Image labeled as: {label}")
            st.success("Label saved successfully!")
    else:
        st.warning("Please upload an image first.")


if st.session_state.button_clicked == 'Search':
    if uploaded_file is not None:
        st.write("Photo uploaded")
        st.image(uploaded_file, caption='Uploaded Photo', use_column_width=True)
        st.write("Searching for image label...")
    else:
        st.warning("Please upload an image first.")

def reset_button_state():
    st.session_state.button_clicked = None

if st.button('Reset'):
    reset_button_state()

#home