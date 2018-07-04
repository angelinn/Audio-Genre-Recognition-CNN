import os

import sys
import spectrogram as sp
import numpy as np

from train import create_model
from tools import convert_slices_to_array
from spectrogram import SPECTROGRAMS_PATH
from tools import SCRIPTS_DIRECTORY

SLICE_SIZE = 128
MODEL_FILE_NAME = os.path.join(SCRIPTS_DIRECTORY, '../model/musicDNN.tflearn')
GENRES = ['Metal', 'Pop', 'Punk', 'Rap']    
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_PATH = os.path.dirname(SCRIPT_PATH) + "\\"
MONO_PATH = SCRIPT_PATH + 'mono\\'
SLICES_PATH = SCRIPT_PATH + 'slices\\'
SPECTROGRAMS_TEST_PATH = SCRIPT_PATH + 'spectrograms\\'

def create_folders():
    print('Creating folders...')
    if not os.path.exists(MONO_PATH):
        os.makedirs(MONO_PATH)
        
    if not os.path.exists(SLICES_PATH):
        os.makedirs(SLICES_PATH)
        
    if not os.path.exists(SPECTROGRAMS_TEST_PATH):
        os.makedirs(SPECTROGRAMS_TEST_PATH)

def init():
    create_folders()
    print('Loading model...')
    model = create_model(SLICE_SIZE, len(GENRES))    
    model.load(MODEL_FILE_NAME)
    print('Model loaded.')

    return model

def predict_genre(path, model):
    print("Reading music file {}...".format(path))
    
    folder_name = os.path.dirname(path) + "\\"
    file_name = os.path.basename(path)

    if not folder_name or not file_name or not os.path.exists(folder_name + file_name):
        print("File {} does not exist.".format(path))
        return

    for file in os.listdir(SLICES_PATH):
        os.remove(SLICES_PATH + file)

    print('Creating spectrogram...')
    sp.create_spectrogram(folder_name, file_name, MONO_PATH, file_name)
    sp.slice_spectrogram(SPECTROGRAMS_PATH, file_name + '.png', SLICE_SIZE, SLICES_PATH, 'slice')
    x = convert_slices_to_array(SLICES_PATH, SLICE_SIZE)

    print('Predicting genre...')
    prediction = model.predict(x)

    print('Voting...')
    results = []
    # for slice in prediction:

    for slice in prediction:
        conf = np.max(slice)
        if conf > 0.5:        
            results.append((np.argmax(slice), conf))

    votes, confidence = zip(*results)
    
    bincount = np.bincount(votes)
    print(bincount)

    confidences = []
    for i in range(len(bincount)):
        confidences.append(sum([confidence[i] for vote in votes if vote == i]) / bincount[i])
        
    chosen = np.argmax(bincount)
    frequency = np.max(bincount) / sum(bincount)
    genre = GENRES[chosen]
    print('I think the genre is {} and I\'m {:.2f} percent confident.'.format(genre, frequency))

def prompt_for_path(model):
    while True:
        path = input('Enter a song path to predict its genre:\n')
        predict_genre(path, model)

        go = input('Continue? (y/n)')
        if go == 'n':
            break

def main():
    model = init()

    if len(sys.argv) > 1:
        predict_genre(sys.argv[1], model)
    else:
        prompt_for_path(model)

if __name__ == '__main__':
    main()

