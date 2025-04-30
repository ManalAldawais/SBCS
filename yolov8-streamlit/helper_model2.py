from ultralytics import YOLO
import streamlit as st
import cv2
import yt_dlp
import settings
import numpy as np
from PIL import Image
from ultralytics.utils.plotting import Annotator
import io
from helper_email import send_email_alert
from pathlib import Path
import tempfile
import os

email_sent = False


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None


def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):

    st.session_state.email_sent = False
    st.session_state.alert_shown = False
    st.session_state.sound_played = False

    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        res = model.predict(image, conf=conf)

    annotator = Annotator(image)

    for box in res[0].boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]
        b = box.xyxy[0].cpu().numpy()

        color = (0, 0, 255) if label.lower() == "violence" else (0, 255, 0)
        annotator.box_label(b, label, color=color)

    res_plotted = annotator.result()


    violence_detected = any(model.names[int(box.cls[0])].lower() == 'violence' for box in res[0].boxes)

    if violence_detected:

        if not st.session_state.email_sent:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    temp_image_path = tmp_file.name
                    cv2.imwrite(temp_image_path, res_plotted)

                send_email_alert(
                    receiver_email="Mahaalosaimi2@gmail.com",
                    subject="🚨 Urgent Security Alert: Violence Detected",
                    message_body="""\
                        Dear User,

                        Attention! A potential act of violence has been detected by the security monitoring system.

                        ⚠️ Immediate review of the situation is strongly recommended.

                        Stay safe,
                        Your Security Monitoring System
                        """,
                                            image_path=Path(temp_image_path))

                st.session_state.email_sent = True
                os.remove(temp_image_path)

            except Exception as e:
                st.warning(f"Failed to send email alert: {e}")


        if not st.session_state.sound_played and not st.session_state.alert_shown:
            st.audio(str(settings.ALARM_AUDIO), format="audio/wav", autoplay=True)
            st.session_state.sound_played = True
            st.error("🚨 Violence detected! 🚨", icon="🚨")
            st.session_state.alert_shown = True

        st.markdown(
            """
            <style>
            body {
                background-color: red;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        if st.button("🛑 Stop Alarm and Reset Background",key=f"reset_alarm"):
            st.session_state.email_sent = False
            st.session_state.alert_shown = False
            st.session_state.sound_played = False
            st.experimental_rerun()

    st_frame.image(res_plotted, caption='Detected Video', channels="BGR", use_column_width=True)

def play_rtsp_stream(conf, model):
    """
    Plays an rtsp stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_rtsp = st.sidebar.text_input("rtsp stream url:")
    st.sidebar.caption(
        'Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))

def play_webcam(conf, model):
    """
    Plays a webcam stream. Detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence threshold for the YOLOv8 model.
        model: An instance of the YOLOv8 model.

    Returns:
        None
    """
    camera_image = st.camera_input("Take a picture")

    if camera_image is not None:
        try:
            image = Image.open(camera_image)
            st.image(image, caption="Captured Image", use_column_width=True)

            if st.button("Detect Objects",key="object_detection"):
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


def play_stored_video(conf, model):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_vid = st.sidebar.selectbox(
        "Choose a video...", settings.VIDEOS_DICT.keys())

    is_display_tracker, tracker = display_tracker_options()

    with open(settings.VIDEOS_DICT.get(source_vid), 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.sidebar.button('Detect Video Objects'):
        try:
            vid_cap = cv2.VideoCapture(
                str(settings.VIDEOS_DICT.get(source_vid)))
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                    if st.session_state.sound_played and st.session_state.alert_shown:
                        break
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))
