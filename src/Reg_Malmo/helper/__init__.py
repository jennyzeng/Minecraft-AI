import os

# config tf
if 'TF_CPP_MIN_LOG_LEVEL' not in os.environ:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#add location of ffmpeg. in terminal, put "which ffmpeg" and you will get it
if "/usr/local/bin" not in os.environ["PATH"]:
    os.environ["PATH"] += ":/usr/local/bin"

from ml_helper import ML_Helper
from init_helper import Init_Helper
from mission_helper import MissionHelper