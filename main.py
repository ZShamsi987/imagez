import streamlit as st
from image_processor import preprocess_image
from database import create_connection, insert_image
from model import create_model, train_model, save_model


database = "data/images.db"
conn = create_connection(database)


model = create_model()

st.title('Image Recognition App')


st.header('Label Images')
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
label = st.text_input('Label')
if st.button('Submit'):
    if uploaded_file and label:
        image_path = f"data/{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        insert_image(conn, label, image_path)
        st.success('Image and label saved successfully!')


st.header('Scan Images')
scan_file = st.file_uploader("Choose an image to scan...", type="jpg")
if st.button('Scan'):
    if scan_file:
        scan_image_path = f"data/{scan_file.name}"
        with open(scan_image_path, "wb") as f:
            f.write(scan_file.getbuffer())
        scan_image = preprocess_image(scan_image_path)
        prediction = model.predict(np.array([scan_image]))
        predicted_label = np.argmax(prediction)
        st.write(f'Predicted label: {predicted_label}')


if st.button('Train Model'):
    cur = conn.cursor()
    cur.execute("SELECT * FROM images")
    rows = cur.fetchall()
    images = []
    labels = []
    for row in rows:
        images.append(preprocess_image(row[2]))
        labels.append(row[1])
    images = np.array(images)
    labels = np.array(labels)
    model = train_model(model, images, labels)
    save_model(model, "data/model.h5")
    st.success('Model trained successfully!')
