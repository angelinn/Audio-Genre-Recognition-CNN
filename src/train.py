import numpy as np

print('Importing libraries...')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import tflearn

from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

print('Done')

def create_model(image_size, classes_length):
    convnet = input_data(shape=[None, image_size, image_size, 1])

    convnet = conv_2d(convnet, 64, 2, activation='elu', weights_init='Xavier')
    convnet = max_pool_2d(convnet, 2)

    convnet = conv_2d(convnet, 128, 2, activation='elu', weights_init='Xavier')
    convnet = max_pool_2d(convnet, 2)

    convnet = conv_2d(convnet, 256, 2, activation='elu', weights_init='Xavier')
    convnet = max_pool_2d(convnet, 2)

    convnet = conv_2d(convnet, 512, 2, activation='elu', weights_init='Xavier')
    convnet = max_pool_2d(convnet, 2)
    
    convnet = fully_connected(convnet, 1024, activation='elu')
    convnet = dropout(convnet, 0.5)

    convnet = fully_connected(convnet, classes_length, activation='softmax')
    convnet = regression(convnet, optimizer='rmsprop', loss='categorical_crossentropy')

    model = tflearn.DNN(convnet, tensorboard_verbose=3, checkpoint_path='checkpoints', best_checkpoint_path='best')
    return model
