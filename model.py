from os import listdir
from os.path import join, isdir
import os
import subprocess



def preprocess():
    source_dir = "wav"
    target_dir = "chunks"
    chunk_length = 0.02

    if not isdir(target_dir):
        os.mkdir(target_dir)
    
    for audio_name in listdir(source_dir):
        audio_prefix = audio_name.split(".")[0]
        command = "ffmpeg -i {} -f segment -segment_time {} -c copy {}/{}_%03d.wav".format(
            join(source_dir, audio_name), chunk_length, target_dir, audio_prefix)
        subprocess.run(command, shell=True)
        break

    



    



if __name__ == "__main__":
    preprocess()