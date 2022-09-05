#Add folder to sys path to import modules from sub folders
import sys
sys.path.insert(0, r'C:\Users\SaANTIAGO\Google Drive Streaming\My Drive\18_UT_RAPID\cuttings_sensor')

from src.file_dialog import *
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import PIL.Image
from PIL import Image, ImageOps #, ImageFilter, ImageEnhance, 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = Path(r'C:\Program Files\Tesseract-OCR\tesseract.exe') #Set Pytesseract path

import datetime

def get_directory_files(file_extension: str):
    """Look for files in directory with file extension as file_extension.
    Returns directory path as string and list of absolute paths to files with matching extension.
    file_extension: str, file extension
    """
    directory = get_directory('Select Images Directory', as_path=False)
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    files = list([])
    for file in onlyfiles:
         if file.endswith(file_extension):
                file_path = '/'.join([directory, file])
                files.append(file_path)
    return directory, files

def process_img(img_path: str, gray_scale = False):
    """Open image from img_path, invert.
    Returns processed image.
    img_path: absolute path to image file
    gray_scale: Boolean, if True image will be converted to grayscale
    """
    if gray_scale == True:
        img = PIL.Image.open(img_path).convert("L") #Convert to gray-scale
    else:
        img = PIL.Image.open(img_path)
    img = ImageOps.invert(img) #Invert
    return img

def get_number_from_img(img, timeout = 15):
    """Get float number from image.
    Returns float number.
    img: processed image
    timeout: pytesseract timeout value - default = 15
    """
    #Run OCR on image
    img_number = pytesseract.image_to_string(img,
                                             lang='eng',
                                             timeout=timeout,
                                             config='--psm 7 -c tessedit_char_whitelist=0123456789.')
    try:
        img_number = '.' + img_number.split('.')[-1] #Extract right side of number
        img_number = float(img_number) #convert to float
    except:
        img_number = np.nan #if img_number is empty, set as NaN
    return img_number

def get_frame_number(file):
    """Return frame number, based on file absolute path.
    file: file absolute path
    """
    frame_number = file.split('/')[-1].split('_frame_')[-1].split('.')[0]
    frame_number = int(frame_number)
    return frame_number

def get_number_list(files: list):
    """Return number list from image files.
    files: list of image files absolute paths.
    Returns: 
    number_list
    """
    number_list = []
    for file in files:
        img = process_img(file)
        img_number = get_number_from_img(img)
        number_list.append(img_number)
        #print(number_list[-1])
    return number_list

def get_frame_list(files: list):
    """Return frame number list from image files.
    files: list of image files absolute paths.
    Returns: 
    frame_number_list
    """
    frame_number_list = []
    for file in files:
        frame_number = get_frame_number(file)
        frame_number_list.append(frame_number)
    return frame_number_list

def get_time_index(initial_time_str: str, seconds: int, files: list):
    time_array = []
    initial_time_str = initial_time_str
    initial_time = datetime.datetime.strptime(initial_time_str, '%Y-%m-%d %H:%M:%S')
    for i in np.arange(0, len(files), 1):
        time_i = initial_time + i * datetime.timedelta(seconds=seconds)
        time_i = pd.to_datetime(time_i)
        time_array.append(time_i)
    time_array = np.array(time_array)
    return time_array

def get_conveyor_index(initial_conveyor: int, distance: int, files: list):
    conveyor_array = []
    initial_conveyor = initial_conveyor
    for i in np.arange(0, len(files), 1):
        conveyor_i = initial_conveyor + i * distance
        conveyor_array.append(conveyor_i)
    conveyor_array = np.array(conveyor_array)
    return conveyor_array
