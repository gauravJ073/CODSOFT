# pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

import os
import cv2
from facenet_pytorch import MTCNN

## to save frames of a video that has faces in them as images

class LoadFaces():
    def __init__(self, name, vid_path):
        self.mtcnn=MTCNN()
        #opening the video
        self.vid=cv2.VideoCapture(vid_path)
        self.vid_len=int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        print(self.vid_len)
        if self.vid_len==0:
            print("Couldnt load video. Make sure you enter the right path")
        #get total numer of frames in the video
        self.v_len = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        #list to store frames
        frames = []

        #storing frames of the video in the list
        for _ in range(self.v_len):
            success, frame = self.vid.read()
            if not success:
                continue
            frames.append(frame)

        savepath=f'Face-Detection-Recognition/data/{name}'

        if not os.path.exists(savepath):
            os.makedirs(savepath)

        #iterating through each face and using MTCNN to see if it detects a face
        for frame in frames:
            temp = self.mtcnn(frame)
            print(f'{i} images saved')
            #if face is detected, save the frame as jpg file at location - 'savepath'
            if temp is not None:
                cv2.imwrite(f'{savepath}\\frame{i}.jpg', frame)
                print(f'{savepath}\\frame{i}.jpg')
                i+=1



LoadFaces("Gaurav", "C:/Users/GAURAV/Pictures/Camera Roll/testvideo.mp4")
