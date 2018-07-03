import os

import sys
import spectrogram as sp

from train import create_model
from tools import convert_slices_to_array

SLICE_SIZE = 128

print("Reading music file {}...".format(sys.argv[1]))

folder_name = os.path.dirname(sys.argv[1])
file_name = os.path.basename(sys.argv[1])

script_path = os.path.realpath(__file__)
sp.create_spectrogram(folder_name, file_name, script_path, 'spectrogram.png')
sp.slice_spectrogram(folder_name, file_name, 128, scripts_path, 'slice')

x, y = convert_slices_to_array(script_path, genre, 128)
