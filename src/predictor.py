import os

import sys
import spectrogram as sp

print("Reading music file {}...".format(sys.argv[1]))

folder_name = os.path.dirname(sys.argv[1])
file_name = os.path.basename(sys.argv[1])

sp.create_spectrogram(folder_name, file_name, 'user.mp3')
sp.slice_spectrogram(sys.argv[1], 128)

