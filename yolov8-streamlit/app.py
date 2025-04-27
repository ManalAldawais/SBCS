import streamlit as st
import settings
from pathlib import Path
from PIL import Image
import cv2
import helper_model1 as m1
import helper_model2 as m2

# Setting page layout
st.set_page_config(
    page_title="Object Detection using YOLOv8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Violence & Student Detection using YOLOv8")

# Sidebar for selecting model
model_type = st.sidebar.radio(
    "Select Task", ['Violence Detection', 'Student Detection'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 10, 100, 20)) / 100

# Load models
if model_type == 'Violence Detection':
    model_path = Path(settings.VIOLENCE_DETECTION_MODEL)
    model = m2.load_model(model_path)
elif model_type == 'Student Detection':
    model_path = Path(settings.STUDENT_DETECTION_MODEL)
    model = m1.load_model(model_path)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

# Main content area
source_img = None
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is not None:
                uploaded_image = Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
            else:
                st.info("Please upload an image for detection")
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is not None:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    if model_type == 'Violence Detection':
        m2.play_stored_video(confidence, model)
    else:
        m1.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    if model_type == 'Violence Detection':
        m2.play_webcam(confidence, model)
    else:
        m1.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    if model_type == 'Violence Detection':
        m2.play_rtsp_stream(confidence, model)
    else:
        m1.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    if model_type == 'Violence Detection':
        m2.play_youtube_video(confidence, model)
    else:
        m1.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
