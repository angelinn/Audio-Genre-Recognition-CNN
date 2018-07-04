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
    else:
        print('Cleaning old data...')
        for file in os.listdir(SLICES_PATH):
            os.remove(SLICES_PATH + file)
        
    if not os.path.exists(SPECTROGRAMS_TEST_PATH):
        os.makedirs(SPECTROGRAMS_TEST_PATH)


def predict_genre(path):
    print("Reading music file {}...".format(path))

    folder_name = os.path.dirname(path) + "\\"
    file_name = os.path.basename(path)

    create_folders()

    if not os.path.exists(folder_name + file_name):
        print("File {} does not exist.".format(path + filename))
        return

    print('Creating spectrogram...')
    sp.create_spectrogram(folder_name, file_name, MONO_PATH, file_name)
    sp.slice_spectrogram(SPECTROGRAMS_PATH, file_name + '.png', SLICE_SIZE, SLICES_PATH, 'slice')
    x = convert_slices_to_array(SLICES_PATH, SLICE_SIZE)

    print('Loading model...')
    model = create_model(128, len(GENRES))    
    model.load(MODEL_FILE_NAME)
    print('Model loaded.')

    print('Predicting genre...')
    prediction = model.predict(x)

    print('Voting...')
    votes = []
    for slice in prediction:
        votes.append(np.argmax(slice))

    bincount = np.bincount(votes)
    print(bincount)
    genre = GENRES[np.argmax(bincount)]
    print('I think the genre is {}.'.format(genre))

if __name__ == '__main__':
    predict_genre(sys.argv[1])
