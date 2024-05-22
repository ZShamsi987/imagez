import streamlit as st
import cv2
from PIL import Image
import numpy as np
from scipy import stats, ndimage
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()

class ImageData(Base):
    __tablename__ = 'image_data'
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    data = Column(String)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def main():
    st.title("Image Recognition App")
    
    menu = ["Label", "Scan"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Label":
        st.subheader("Label an Image")
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        if image_file is not None:
            img = Image.open(image_file)
            st.image(img, caption='Uploaded Image.', use_column_width=True)
            label = st.text_input("Label")
            if st.button("Save"):
                save_image_data(img, label)
                st.success("Image saved with label: {}".format(label))
    
    elif choice == "Scan":
        st.subheader("Scan an Image")
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
        if image_file is not None:
            img = Image.open(image_file)
            st.image(img, caption='Uploaded Image.', use_column_width=True)
            result = process_image(img)
            st.write("Processed Image Mean: ", result)

def save_image_data(image, label):
    session = SessionLocal()
    img_data = np.array(image)
    img_data_str = img_data.tostring()
    new_image = ImageData(label=label, data=img_data_str)
    session.add(new_image)
    session.commit()
    session.close()

def process_image(image):
    img_data = np.array(image.convert('L')) 
    mean = stats.tmean(img_data)
    return mean

if __name__ == "__main__":
    main()
