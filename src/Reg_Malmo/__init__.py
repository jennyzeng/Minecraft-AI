import os
import sys
import time

# config tf
if 'TF_CPP_MIN_LOG_LEVEL' not in os.environ:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from src.Img_Preprocess.MC_Img_Preprocess import scaleImg

#add location of ffmpeg. in terminal, put "which ffmpeg" and you will get it
if "/usr/local/bin" not in os.environ["PATH"]:
    os.environ["PATH"] += ":/usr/local/bin"