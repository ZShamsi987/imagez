import streamlit as st


st.title("Imagez")
st.caption("Image recognition except it's based on images people submit to this model, nothing else")

if st.button('Label'):
    st.write("Label button clicked")

if st.button('Search'):
    st.write("Search button clicked")

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png"])

if uploaded_file is not None:
    st.write("Photo uploaded")
    st.image(uploaded_file, caption='Uploaded Photo', use_column_width=True)
