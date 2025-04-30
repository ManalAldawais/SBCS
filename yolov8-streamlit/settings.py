from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())


SENDER_EMAIL = "Mahaalosaimi2@gmail.com"
ALARM_AUDIO = "audio/alarm.wav"

VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'

SOURCES_LIST = [VIDEO, WEBCAM, RTSP]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'office_4.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'office_4_detected.jpg'
HOME_IMAGE = IMAGES_DIR / 'home.jpg'
# Videos config

VIDEO_DIR = ROOT / 'videos'
STUDENT_VIDEO_DIR = ROOT / 'student_videos'


VIDEOS_DICT = {
    'video_1': VIDEO_DIR / 'video_1.mp4',
    'video_2': VIDEO_DIR / 'video_2.mp4',
    'video_3': VIDEO_DIR / 'video_3.mp4',
     'video_5': VIDEO_DIR / 'video_5.mp4',
}
STUDENT_VIDEO_DICT = {
    'video_1': STUDENT_VIDEO_DIR / 'video_one.mp4',
    'video_2': STUDENT_VIDEO_DIR / 'video_two.mp4',
    'video_3': STUDENT_VIDEO_DIR / 'video_three.mp4',
    'video_4': STUDENT_VIDEO_DIR / 'video_four.mp4'
}
# Audio config
AUDIO_DIR = ROOT / 'audio'
ALARM_AUDIO = AUDIO_DIR / 'alarm.wav'


# ML Model config
MODEL_DIR = ROOT / 'weights'
VIOLENCE_DETECTION_MODEL = MODEL_DIR / 'yolov8n.pt'
STUDENT_DETECTION_MODEL = MODEL_DIR / 'student_detection.pt'

WEBCAM_PATH = 0
