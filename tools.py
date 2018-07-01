import os
import numpy as np
from random import shuffle
from PIL import Image
import pickle
import errno

SPECTROGRAM_SLICES_PATH = 'slices'
DATASET_PATH = 'datasets'

def get_dataset_name(nbPerGenre, slice_size):
    name = "{}".format(nbPerGenre)
    name += "_{}".format(slice_size)
    return name

def get_dataset(files_per_genre, genres, slice_size, validation_ratio, test_ratio, mode):
    print("Dataset name: {}".format(get_dataset_name(files_per_genre,slice_size)))
    test_file = "{}\\train_X_{}.p".format(DATASET_PATH, get_dataset_name(files_per_genre, slice_size))
    if not os.path.isfile(test_file):
        print("Creating dataset with {} slices of size {} per genre...".format(files_per_genre,slice_size))
        create_dataset_from_slices(files_per_genre, genres, slice_size, validation_ratio, test_ratio) 
    else:
        print("Using existing dataset")

    return load_dataset(files_per_genre, genres, slice_size, mode)

def create_dataset_from_slices(files_per_genre, genres, slice_size, validation_ratio, test_ratio):
    data = []
    for genre in genres:
        print("-> Adding {}...".format(genre))
        #Get slices in genre subfolder
        filenames = os.listdir("{}\\{}".format(SPECTROGRAM_SLICES_PATH, genre))
        filenames = [filename for filename in filenames if filename.endswith('.png')]
        filenames = filenames[:files_per_genre]
        #Randomize file selection for this genre
        shuffle(filenames)

        #Add data (X,y)
        for filename in filenames:
            imgData = get_image_data("{}\\{}\\{}".format(SPECTROGRAM_SLICES_PATH, genre, filename), slice_size)
            label = [1. if genre == g else 0. for g in genres]
            data.append((imgData,label))

    #Shuffle data
    shuffle(data)

    #Extract X and y
    X,y = zip(*data)

    #Split data
    validationNb = int(len(X)*validation_ratio)
    testNb = int(len(X)*test_ratio)
    trainNb = len(X)-(validationNb + testNb)

    #Prepare for Tflearn at the same time
    train_X = np.array(X[:trainNb]).reshape([-1, slice_size, slice_size, 1])
    train_y = np.array(y[:trainNb])
    validation_X = np.array(X[trainNb:trainNb+validationNb]).reshape([-1, slice_size, slice_size, 1])
    validation_y = np.array(y[trainNb:trainNb+validationNb])
    test_X = np.array(X[-testNb:]).reshape([-1, slice_size, slice_size, 1])
    test_y = np.array(y[-testNb:])
    print("Dataset created.")
        
    #Save
    save_dataset(train_X, train_y, validation_X, validation_y, test_X, test_y, files_per_genre, genres, slice_size)

    return train_X, train_y, validation_X, validation_y, test_X, test_y

def load_dataset(files_per_genre, genres, slice_size, mode):
    #Load existing
    datasetName = get_dataset_name(files_per_genre, slice_size)
    if mode == "train":
        print("Loading training and validation datasets... ")
        train_X = pickle.load(open("{}\\train_X_{}.p".format(DATASET_PATH,datasetName), "rb" ))
        train_y = pickle.load(open("{}\\train_y_{}.p".format(DATASET_PATH,datasetName), "rb" ))
        validation_X = pickle.load(open("{}\\validation_X_{}.p".format(DATASET_PATH,datasetName), "rb" ))
        validation_y = pickle.load(open("{}\\validation_y_{}.p".format(DATASET_PATH,datasetName), "rb" ))
        print("Training and validation datasets loaded.")
        return train_X, train_y, validation_X, validation_y

    else:
        print("Loading testing dataset... ")
        test_X = pickle.load(open("{}\\test_X_{}.p".format(DATASET_PATH,datasetName), "rb" ))
        test_y = pickle.load(open("{}\\test_y_{}.p".format(DATASET_PATH,datasetName), "rb" ))
        print("Testing dataset loaded.")
        return test_X, test_y

#Saves dataset
def save_dataset(train_X, train_y, validation_X, validation_y, test_X, test_y, files_per_genre, genres, slice_size):
     #Create path for dataset if not existing
    if not os.path.exists(DATASET_PATH):
        try:
            os.makedirs(DATASET_PATH)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    #save_dataset
    print("Saving dataset... ")
    datasetName = get_dataset_name(files_per_genre, slice_size)
    pickle.dump(train_X, open("{}\\train_X_{}.p".format(DATASET_PATH,datasetName), "wb" ))
    pickle.dump(train_y, open("{}\\train_y_{}.p".format(DATASET_PATH,datasetName), "wb" ))
    pickle.dump(validation_X, open("{}\\validation_X_{}.p".format(DATASET_PATH,datasetName), "wb" ))
    pickle.dump(validation_y, open("{}\\validation_y_{}.p".format(DATASET_PATH,datasetName), "wb" ))
    pickle.dump(test_X, open("{}\\test_X_{}.p".format(DATASET_PATH,datasetName), "wb" ))
    pickle.dump(test_y, open("{}\\test_y_{}.p".format(DATASET_PATH,datasetName), "wb" ))
    print("Dataset saved.")

#Returns numpy image at size image_size*image_size
def get_processed_data(img, image_size):
    img = img.resize((image_size,image_size), resample=Image.ANTIALIAS)
    imgData = np.asarray(img, dtype=np.uint8).reshape(image_size,image_size,1)
    imgData = imgData/255.
    return imgData

#Returns numpy image at size image_size*image_size
def get_image_data(filename,image_size):
    img = Image.open(filename)
    imgData = get_processed_data(img, image_size)
    return imgData
