from train import create_model
from tools import SPECTROGRAM_SLICES_PATH
from tools import get_dataset
import os

filesPerGenre = 1000
SLICE_SIZE = 128
validation_ratio = 0.3
test_ratio = 0.1  

print("Spectrogram path is: {}".format(SPECTROGRAM_SLICES_PATH))
print("Slice size is: {}".format(SLICE_SIZE))

slices = os.listdir(SPECTROGRAM_SLICES_PATH)
genres = [fileName for fileName in slices if os.path.isdir("{}\\{}".format(SPECTROGRAM_SLICES_PATH, fileName))]
genres_length = len(genres)

print("Found {} genres.".format(genres_length))
print("Creating model...")

model = create_model(SLICE_SIZE, genres_length)
print('Model created')

train_X, train_y, validation_X, validation_y = get_dataset(filesPerGenre, genres, SLICE_SIZE, validation_ratio, test_ratio, mode="train")
