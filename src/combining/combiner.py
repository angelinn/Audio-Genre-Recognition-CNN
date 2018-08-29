# 1. Analyze 10 songs of each genre
# 2. Find the second best results - e.g slices that were not correctly recognised
# 3. Combine slices from different songs from the same genre
# 4. Find the music parts corresponding to the slices
# 5. Fetch the parts from the mp3 files and glue 'em in a new audio file

import os
import sys
import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import spectrogram as sp
from tools import SCRIPTS_DIRECTORY
from tools import convert_slices_to_array
from train import create_model

from spectrogram import SPECTROGRAMS_PATH

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

    for file in os.listdir(SAMPLES_DIR)[:2]: 
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

def vote(prediction):
    results = []
    for slice in prediction:
        conf = np.max(slice)
        if conf > 0.5:        
            results.append((np.argmax(slice), conf))

    votes, confidence = zip(*results)
    
    bincount = np.bincount(votes)
    print(bincount)
    
    return bincount

def get_second_best_guess(predictions, genre):
    targets = []

    for prediction in predictions:
        votes = vote(prediction)
        target = sorted(votes)[-2]
        target_index = list(votes).index(target)
        targets.append(target_index)

    return targets



def isolate_slices(genre):
    samples = get_samples()
    predictions = recognize_samples([sample[1] for sample in samples])

    filtered_samples = []
    second_guesses = get_second_best_guess(predictions, genre)
    for i, second in enumerate(second_guesses):
        if str(second) == str(genre):
            filtered_samples.append((samples[i][0], predictions[i]))

    return filtered_samples

def filter_slices(slices, genre):
    target_slices = []
    for i, slice in enumerate(slices):
        second_best = sorted(slice)[-2]
        index = list(slice).index(second_best)
        if str(index) == str(genre):
            target_slices.append(i)

    return target_slices

def main():
    init()

    genre = '0'
    slices = isolate_slices(genre) 

    new_genre = []
    i = 0
    for slice in slices:
        target_slices = filter_slices(slice[1], genre)
        new_genre.append(target_slices)
        i += len(target_slices)

    print("Found {} target slices.".format(i))

if __name__ == '__main__':
    main()
