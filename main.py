from train import create_model
from tools import SPECTROGRAM_SLICES_PATH
from tools import get_dataset
import os
import random
import string

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN", nargs='+', choices=["train","test","slice"])
args = parser.parse_args()

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

if "train" in args.mode:
    train_X, train_y, validation_X, validation_y = get_dataset(filesPerGenre, genres, SLICE_SIZE, validation_ratio, test_ratio, mode="train")
    run_id = "MusicGenres - "+str(128)+" "+''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))

    print('[+] Training model...')
    model.fit(train_X, train_y, n_epoch=20, batch_size=128, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
    print("    Model trained! ✅")

    print("[+] Saving the weights...")
    model.save('musicDNN.tflearn')
    print("[+] Weights saved! ✅💾")

if "test" in args.mode:
    print('train')