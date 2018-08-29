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
    distribute_emotion()
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
