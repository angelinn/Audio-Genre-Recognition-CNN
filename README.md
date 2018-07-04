# Audio Genre Recognition using Convolutional Neural Network
Software that trains a convolutional neural network in order to recognize music genres using TensorFlow.



## How does it work?
Every audio file is being converted in its visual representation - **spectrogram**.

A spectrogram will be very wide image, so we can slice it in smaller ones to retriieve more samples. I am slicing it in 128x128 images.

Then image recognition on these slices is performed.
The audio processing is done by **sox** software.

## Recognition
The recognition is performed in the file **prediction.py**.
* Receive path to audio file as user input
* Convert the song to mono (single channel)
* Convert the song to a single spectrogram
* Slice the spectrogram into 128x128 pieces
* Load the pieces and pass them to the already trained model
* Whichever genre gets the most votes is the winner

## Tools
* sox

## Libraries
* tensorflow
* tflearn
* eyed3 - for audio tag processing
