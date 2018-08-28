# 1. Analyze 10 songs of each genre
# 2. Find the second best results - e.g slices that were not correctly recognised
# 3. Combine slices from different songs from the same genre
# 4. Find the music parts corresponding to the slices
# 5. Fetch the parts from the mp3 files and glue 'em in a new audio file

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import spectrogram as sp
from tools import SCRIPTS_DIRECTORY
from tools import convert_slices_to_array

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
    model = create_model(SLICE_SIZE, len(GENRES))    
    model.load(MODEL_FILE_NAME)
    print('Model loaded.')

    predictions = []
    for sample in samples:
        prediction = model.predict(x)
        predictions.append(sample) 

    return predictions

def vote(prediction):
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
        target_index = np.argmax(target)
        targets.append(tar)

    return targets



def isolate_slices(genre):
    samples = get_samples()
    predictions = recognize_samples([s[1] for sample in samples])

    filtered_samples = []
    second_guesses = get_second_best_guess(predictions)
    for i, second in second_guesses:
        if second == genre:
            filtered_samples.append(samples[i])

    return filtered_samples

def main():
    init()

    genre = 'Punk'
    slices = isolate_slices(genre)
    print(slices)

if __name__ == '__main__':
    main()
