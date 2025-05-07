import streamlit as st
import settings
from pathlib import Path
from PIL import Image
import cv2
import helper_model1 as m1
import helper_model2 as m2




# Setting page layout
st.set_page_config(
    page_title="School Buses Controlling System",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Main page heading
st.title("Violence & Student Detection")

# Sidebar for selecting model
model_type = st.sidebar.radio(
    "Select Task", ['Violence Detection', 'Student Detection']
)

# Load models + Set confidence without slider
if model_type == 'Violence Detection':
    model_path = Path(settings.VIOLENCE_DETECTION_MODEL)
    model = m2.load_model(model_path)
    confidence = 0.6
elif model_type == 'Student Detection':
    model_path = Path(settings.STUDENT_DETECTION_MODEL)
    model = m1.load_model(model_path)
    confidence = 0.2

st.sidebar.header("Image/Video Config")

source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST
)

# Main content area
source_img = None

if source_radio == settings.VIDEO:
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

else:
    st.error("Please select a valid source type!")
