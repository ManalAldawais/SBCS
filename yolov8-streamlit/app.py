import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd
import altair as alt
import settings
import helper_model1 as m1
import helper_model2 as m2
import streamlit as st
import numpy as np


# Set page config
st.set_page_config(
    page_title="School Buses Controlling System",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title (before tabs)
st.title("🚌 School Bus Controlling System")

# TOP-LEVEL TABS — must come after title/layout setup
tabs = st.tabs(["📘 Project Overview","🧠 Detection"])



with tabs[0]:


    st.title("📘 Project Overview")
    st.markdown("<br><br>", unsafe_allow_html=True)

    image = Image.open("image/3.jpg")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(image, width=250)

    with col2:
        st.markdown("## A Story Sparked Our Solution")
        st.write("""
        Hassan is a young boy whose tragic death inside a school bus sparked national concern in Saudi Arabia.
        He was accidentally left behind and later found deceased, prompting urgent discussions about student safety
        and the need for enhanced monitoring systems in school transport.
        """)



    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    ## 🔍 Project Goals

    This application is built using **YOLOv8** for real-time object detection, focusing on key tasks:

    1. **Ensure Student Safety** — Develop a system to monitor and protect students during school commutes.
    2. **Automated Student Detection & Tracking** — Use AI-based vision to detect and assign IDs to students inside the bus.
    3. **Unsafe Behavior & Violence Detection** — Use  AI models to detect fights or unsafe conduct, and alert staff immediately.
    4. **Emergency Alert System** — Instant alerts for missing students, breakdowns, or route issues.

    The models are loaded using **custom-trained YOLOv8 weights** and run inference on webcam, video files, or RTSP streams.

    ## 🛠️ Technologies Used
    - **Streamlit** for interactive web interface
    - **YOLOv8** (Ultralytics)
    - **Python**
    - **Google Cloud Platform** for project deploying
    - **Github**


    ## 💡 USA Case Studey
    """)





    # Data from your chart
    data = pd.DataFrame({
        "Location": ["Cobb County, GA", "Cobb County, GA",
                    "Bridgeport, CT", "Bridgeport, CT",
                    "Shelton, CT", "Shelton, CT"],
        "Metric": ["Before (per week)", "After (per week)"] * 3,
        "Incidents": [300, 200, 220, 30, 580, 70]
    })

    # Bar chart using Altair
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Location:N', title=None),
        y=alt.Y('Incidents:Q', title='Incidents per Week'),
        color=alt.Color('Metric:N', scale=alt.Scale(range=['#DDDDDD', '#FEC601'])),
        column='Metric:N'
    ).properties(
        width=150,  # Width of each small chart
        height=300,  # Chart height
        title="🚌 Improved School Bus Safety After Implementing a Monitoring System"
    )

    # Show chart
    st.altair_chart(chart, use_container_width=False)









with tabs[1]:
    model_type = st.sidebar.radio("Select Task", ['Violence Detection', 'Student Detection'])

    if model_type == 'Violence Detection':
        model_path = Path(settings.VIOLENCE_DETECTION_MODEL)
        model = m2.load_model(model_path)
        confidence = 0.6
    else:
        model_path = Path(settings.STUDENT_DETECTION_MODEL)
        model = m1.load_model(model_path)
        confidence = 0.2

    st.sidebar.header("Image/Video Config")
    source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)

    if source_radio == settings.VIDEO:
        m2.play_stored_video(confidence, model) if model_type == 'Violence Detection' else m1.play_stored_video(confidence, model)
    elif source_radio == settings.WEBCAM:
        m2.play_webcam(confidence, model) if model_type == 'Violence Detection' else m1.play_webcam(confidence, model)
    elif source_radio == settings.RTSP:
        m2.play_rtsp_stream(confidence, model) if model_type == 'Violence Detection' else m1.play_rtsp_stream(confidence, model)
    else:
        st.error("Please select a valid source type!")

# Footer styled as part of the main content
st.markdown("---")
st.markdown(
    """
    <style>
    .footer {
        margin-top: 50px;
        padding: 15px 0;
        text-align: center;
        font-size: 14px;
        background-color: transparent;
    }
    .footer a {
        color: #0e76a8;
        text-decoration: none;
        margin: 0 15px;
        display: inline-flex;
        align-items: center;
    }
    .footer img {
        height: 18px;
        margin-right: 5px;
    }
    </style>

    <div class="footer">
        <a href="https://www.linkedin.com/in/manal-aldawais-949981208?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">Manal Aldawais
        </a>
        <a href="https://www.linkedin.com/in/amirah-almutairi-596629141?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">Amirah Almutairi
        </a>
        <a href="https://www.linkedin.com/in/shuruq-alotaibi-6014b3302/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">Shuruq Alotaibi
        </a>
        <a href="https://www.linkedin.com/in/alanoud-aldeghaither-3ba32631b/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">Alanoud Aldeghaither
         </a>
        <a href="https://www.linkedin.com/in/mahaalosaimi2?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">Maha Alosaimi
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
