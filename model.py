from os import listdir
from os.path import join

import scipy.io.wavfile as wav
import pandas as pd


def read_data(attr):
    source_dir = join("sd_chunks", attr)
    df = pd.read_csv("{}.csv".format(attr))
    x = df["x"]
    y = df["y"]
    x_dict = dict(zip(x, y))

    for audio in listdir(source_dir):
        audio_id = audio.split("_")[0]
        emotion = x_dict[audio_id]

        freq, signal = wav.read(join(source_dir, audio))
        yield signal, emotion

def train():
    for x, y in read_data("train"):
        print(x.shape, y)

def test():
    for x, y in read_data("test"):
        print(x.shape, y)

if __name__ == "__main__":
    train()