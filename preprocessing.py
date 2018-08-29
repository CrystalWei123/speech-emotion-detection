from os import listdir
from os.path import join, isdir
import os
from shutil import copyfile
import subprocess

from sklearn.model_selection import train_test_split
import scipy.io.wavfile as wav
import pandas as pd
import numpy as np



def preprocess():
    # distribute_emotion()
    distributeTrainTest()
    # source2Chunks()
    # normalizedAudio()

def distribute_emotion():
    emotions = ["anger", "boredom", "disgust", "fear", "happiness", "sadness", "neural"]
    letters = ["W", "L", "E", "A", "F", "T", "N"]
    emotion_dict = dict(zip(letters, emotions))
    print(emotion_dict)
    for emotion in emotions:
        if not isdir(emotion):
            os.mkdir(emotion)
    
    source_dir = "wav"
    for audio in listdir(source_dir):
        tag = audio[5]
        try:
            target_dir = emotion_dict[tag]
            copyfile(join(source_dir, audio), join(target_dir, audio))
        except KeyError:
            pass

def readAudio():
    source_dir = "standized_chunks"
    for audio in listdir(source_dir):
        freq, signal = wav.read(join(source_dir, audio))
        print(signal.shape) # 24576

def distributeTrainTest():
    dir_names = ["train", "test"]
    for dir_name in dir_names:
        if not isdir(dir_name):
            os.mkdir(dir_name)
    
    emotions = ["anger", "boredom", "disgust", "fear", "happiness", "sadness", "neural"]
    train_x_list = []
    train_y_list = []

    test_x_list = []
    test_y_list = []


    for emotion in emotions:
        audios = listdir(emotion)
        # print(len(audios))
        x_train, x_test, y_train, y_test = train_test_split(audios, 
                [emotion for _ in range(len(audios))], test_size=0.2)
        # print(len(x_train), x_train)
        # print(len(x_test), x_test)
        for attr, dir_n, x_list, y_list in zip([x_train, x_test], dir_names,
                    [train_x_list, test_x_list], [train_y_list, test_y_list]):
            for audio in attr:
                copyfile(join(emotion, audio), join(dir_n, audio))
                x_list.append(audio.split(".")[0]) 
                y_list.append(emotion)
            # print(dict_name)
        
    train_df = pd.DataFrame({"x": train_x_list, "y": train_y_list})
    test_df = pd.DataFrame({"x": test_x_list, "y": test_y_list})
    train_df.to_csv("train.csv", index=False)
    test_df.to_csv("test.csv", index=False)

def removeSilence():
    """ Remove the silent part of audio
    Ref:
        - https://stackoverflow.com/questions/25697596/using-ffmpeg-with-silencedetect-to-remove-audio-silence

    """
    pass

def normalizedAudio():
    """ Normalized audio with ffmpeg
    Ref:
        - https://superuser.com/questions/323119/how-can-i-normalize-audio-using-ffmpeg
        - https://trac.ffmpeg.org/wiki/AudioVolume
    """
    source_dir = "chunks"
    target_dir = "standized_chunks"

    if not isdir(target_dir):
        os.mkdir(target_dir)
    
    for audio_name in listdir(source_dir):
        audio_prefix = audio_name.split(".")[0]
        command = "ffmpeg -i {} -filter:a loudnorm {}".format(
            join(source_dir, audio_name), join(target_dir, "{}.wav".format(audio_prefix)))
        subprocess.run(command, shell=True)
    
def source2Chunks():
    """ Split audio to 20ms-length chunks
    Ref:
        - https://unix.stackexchange.com/questions/280767/how-do-i-split-an-audio-file-into-multiple
    """
    source_dir = "wav"
    target_dir = "chunks"
    chunk_length = 0.02 # 20 ms

    if not isdir(target_dir):
        os.mkdir(target_dir)
    
    for audio_name in listdir(source_dir):
        audio_prefix = audio_name.split(".")[0]
        command = "ffmpeg -i {} -f segment -segment_time {} -c copy {}".format(
            join(source_dir, audio_name), chunk_length, join(target_dir, "{}_%03d.wav".format(audio_prefix)))
        subprocess.run(command, shell=True)
    



    



if __name__ == "__main__":
    preprocess()
