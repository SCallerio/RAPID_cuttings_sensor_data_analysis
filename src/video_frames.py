import cv2
import numpy as np

def get_file_path(name, num, save_directory):
    filename = '_'.join([name, str(num)]) + '.tiff'
    file_path = '/'.join([save_directory, filename])
    return file_path

def set_frames_array(seconds_distance, video_cap):
    #Save video FPS
    fps = video_cap.get(cv2.CAP_PROP_FPS)
    #Total Video Frames
    video_duration = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    sec = seconds_distance
    frames_array = np.arange(0, video_duration, fps*sec, dtype=int)
    return frames_array, fps

def save_video_frames(file_name: str, video_cap, frames_array, fps, save_directory, save_laser_img = False, save_full_img = False):
    #Set file names
    full_frame_name = '_'.join([file_name, 'full_frame'])
    log_frame_name = '_'.join([file_name, 'log_frame'])
    laser_frame_name = '_'.join([file_name, 'laser_frame'])
    #Loop through saving frames array to save each selected frame
    for frame_num in frames_array:
        frame_num = int(frame_num)
        #set video frame
        video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        #store current frame
        is_read, frame = video_cap.read()
        #Upscale Image using Laplacian Pyramid Super-Resolution Network
        frame = cv2.pyrUp(cv2.pyrUp(frame))
        #Crop frame to get lower left log data
        crop_log = frame[2685:2725, 680:1000] #[y1:y2, x1:x2]
        crop_laser = frame[170:250, 650:1000]
        #Set file number
        file_num = int(frame_num / fps + 1)
        #Set file path
        file_path = get_file_path(full_frame_name, file_num, save_directory)
        crop_file_path = get_file_path(log_frame_name, file_num, save_directory)
        crop_laser_file_path = get_file_path(laser_frame_name, file_num, save_directory)
        #Save cropped frame to image (log data frame)
        cv2.imwrite(crop_file_path, crop_log) #, [cv2.IMWRITE_JPEG_QUALITY, 100])
        if save_laser_img == True:
            #Save frame to image
            cv2.imwrite(crop_laser_file_path, crop_laser) #, [cv2.IMWRITE_JPEG_QUALITY, 100])
        if save_full_img == True:
            #Save frame to image
            cv2.imwrite(file_path, frame) #, [cv2.IMWRITE_JPEG_QUALITY, 100])

    return
