from ultralytics import YOLO
import streamlit as st
import cv2
import settings
import numpy as np
import os
import tempfile
from PIL import Image
from pathlib import Path
from helper_email import send_email_alert
from ultralytics.utils.plotting import Annotator

def load_model(model_path):
    model = YOLO(model_path)
    return model

def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None

def _display_detected_frames(conf, model, st_frame, image, source_key, is_display_tracking=None, tracker=None):
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        res = model.predict(image, conf=conf, imgsz=970)

    annotator = Annotator(image)
    student_count = 0

    for box in res[0].boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]
        b = box.xyxy[0].cpu().numpy()

        if label.lower() == "student":
            student_count += 1
            color = (255, 200, 100)
        else:
            color = (128, 0, 0)

        annotator.box_label(b, label, color=color)

    res_plotted = annotator.result()

    email_key = f"email_sent_{source_key}"
    if email_key not in st.session_state:
        st.session_state[email_key] = False

    if student_count > 0 and not st.session_state[email_key]:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                temp_image_path = tmp_file.name
                cv2.imwrite(temp_image_path, res_plotted)

            send_email_alert(
                receiver_email="Mahaalosaimi2@gmail.com",
                subject="🚸 Student Detected in the Bus",
                message_body="""
Dear User,

Attention! A student has been detected in the bus.

Please review the situation promptly.

Stay safe,
Your Security Monitoring System
""",
                image_path=Path(temp_image_path)
            )
            st.success("📧 Email alert sent!")
            st.session_state[email_key] = True
            os.remove(temp_image_path)

        except Exception as e:
            st.warning(f"Failed to send email alert: {e}")

    st_frame.image(res_plotted, caption='Detected Video', channels="BGR", use_column_width=True)

def play_stored_video(conf, model):
    source_vid = st.sidebar.selectbox("Choose a video...", settings.STUDENT_VIDEO_DICT.keys())
    is_display_tracker, tracker = display_tracker_options()

    with open(settings.STUDENT_VIDEO_DICT.get(source_vid), 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.sidebar.button('Detect Video Objects'):
        try:
            vid_cap = cv2.VideoCapture(str(settings.STUDENT_VIDEO_DICT.get(source_vid)))
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, source_vid, is_display_tracker, tracker)
                else:
                    break
            vid_cap.release()
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))

def play_rtsp_stream(conf, model):
    source_rtsp = st.sidebar.text_input("rtsp stream url:")
    st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, 'rtsp_source', is_display_tracker, tracker)
                else:
                    break
            vid_cap.release()
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))

def play_webcam(conf, model):
    camera_image = st.camera_input("Take a picture")

    if camera_image is not None:
        try:
            image = Image.open(camera_image)
            st.image(image, caption="Captured Image", use_column_width=True)

            if st.button("Detect Objects"):
                res = model.predict(image, conf=conf)
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption="Detected Image", use_column_width=True)

                boxes = res[0].boxes
                with st.expander("Detection Results"):
                    for box in boxes:
                        st.write(box.data)

        except Exception as ex:
            st.error("Error while processing camera image.")
            st.error(ex)
