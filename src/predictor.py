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

def create_folders(cwd):
    print('Creating folders...')
    if not os.path.exists(cwd + 'mono'):
        os.makedirs(cwd + 'mono')
        
    if not os.path.exists(cwd + 'slices'):
        os.makedirs(cwd + 'slices')
        
    if not os.path.exists(cwd + 'spectrograms'):
        os.makedirs(cwd + 'spectrograms')


def predict_genre(path):
    print("Reading music file {}...".format(path))

    folder_name = os.path.dirname(path) + "\\"
    file_name = os.path.basename(path)

    script_path = os.path.realpath(__file__)
    script_path = os.path.dirname(script_path) + "\\"

    create_folders(script_path)

    if not os.path.exists(folder_name + file_name):
        print("File {} does not exist.".format(path + filename))
        return

    sp.create_spectrogram(folder_name, file_name, script_path + 'mono\\', file_name)
    sp.slice_spectrogram(SPECTROGRAMS_PATH, file_name + '.png', SLICE_SIZE, script_path + 'slices\\', 'slice')
    x = convert_slices_to_array(script_path + 'slices', SLICE_SIZE)

    model = create_model(128, 4)    
    model.load(MODEL_FILE_NAME)

    prediction = model.predict(x)

    final = []
    for res in prediction:
        final.append(np.argmax(res))

    print(np.bincount(final))
    print('Determining genre...')

if __name__ == '__main__':
    predict_genre(sys.argv[1])