from os import listdir
from os.path import join, isdir
import os
import subprocess



def preprocess():
    # source2Chunks()
    # normalizedAudio()
    pass


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
