# 1. Analyze 10 songs of each genre
# 2. Find the second best results - e.g slices that were not correctly recognised
# 3. Combine slices from different songs from the same genre
# 4. Find the music parts corresponding to the slices
# 5. Fetch the parts from the mp3 files and glue 'em in a new audio file

import os
import sys
import pickle
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import spectrogram as sp
from itertools import product
from tools import SCRIPTS_DIRECTORY
from tools import convert_slices_to_array
from train import create_model

from spectrogram import SPECTROGRAMS_PATH

from audio_processor import create_audio

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_PATH = os.path.dirname(SCRIPT_PATH) + "\\"
MODEL_FILE_NAME = os.path.join(SCRIPTS_DIRECTORY, '../model/musicDNN.tflearn')

SLICE_SIZE = 128
MONO_PATH = SCRIPT_PATH + 'mono\\'
SAMPLES_DIR = SCRIPT_PATH + 'samples\\'
SLICES_PATH = SCRIPT_PATH + 'slices\\'

def init():
    if not os.path.exists(MONO_PATH):
        print('Creating directories...')

        os.makedirs(MONO_PATH)
        os.makedirs(SLICES_PATH)

def get_samples():
    samples = []

    for file in os.listdir(SAMPLES_DIR): 
        for slice in os.listdir(SLICES_PATH):
            os.remove(SLICES_PATH + slice)

        print('Creating spectrogram...')

        sp.create_spectrogram(SAMPLES_DIR, file, MONO_PATH, file)
        sp.slice_spectrogram(SPECTROGRAMS_PATH, file + '.png', SLICE_SIZE, SLICES_PATH, 'slice')

        array = convert_slices_to_array(SLICES_PATH, SLICE_SIZE)
        samples.append((SAMPLES_DIR + file, array))

    return samples
        
def recognize_samples(samples):
    print('Loading model...')
    model = create_model(SLICE_SIZE, 4)    
    model.load(MODEL_FILE_NAME)
    print('Model loaded.')

    predictions = []
    for sample in samples:
        prediction = model.predict(sample)
        predictions.append(prediction) 

    return predictions

def get_slices_with_genre(predictions, genre):
    targets = []

    for predicted_slices in predictions:
        current = []
        for i, slice in enumerate(predicted_slices):    
            max_index = np.argmax(slice)

            if str(max_index) == str(genre):
                current.append(i)
        targets.append(current)

    return targets



def isolate_slices(genre):
    samples = get_samples()
    predictions = recognize_samples([sample[1] for sample in samples])

    filtered_samples = []
    slices_with_genre = get_slices_with_genre(predictions, genre)

    files_names = [s[0] for s in samples]
    return zip(files_names, slices_with_genre)

def main():
    init()

    genre = '2'
    slices = isolate_slices(genre)
    slices = list(slices)
        
    for slice in slices:
        print("Found {} target slices for {}.".format(len(slice[1]), slice[0]))

    with open(SCRIPT_PATH + 'slices.bin', 'wb') as slfile:
        pickle.dump(slices, slfile)

    create_audio(slices)

if __name__ == '__main__':
    main()
