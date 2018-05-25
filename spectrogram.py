from subprocess import Popen, PIPE, STDOUT
import eyed3
import os
from PIL import Image

SOX_PATH = 'D:\\Program Files (x86)\\sox-14-4-2\\sox'
AUDIO_DIR = 'D:\\Repositories\\AudioClassification\\fma_small\\000\\'
SPECTROGRAMS_PATH = 'spectrograms\\'
SLICES_PATH = 'slices\\'

def create_spectrogram(filename, new_file_name):
    command = "\"{}\" \"{}\" -n spectrogram -Y 200 -X {} -m -r -o \"{}.png\"".format(SOX_PATH, filename, 50, SPECTROGRAMS_PATH + '\\' + new_file_name)
    print(command)

    pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False, cwd='D:\\Repositories\\AudioClassification\\')
    output, errors = pipe.communicate()
    if errors:
        print(errors)
    
def getGenre(filename):
    audiofile = eyed3.load(filename)
    #No genre
    if not audiofile.tag.genre:
        return 'None'
    else:
        return audiofile.tag.genre.name

def create_all_spectrograms(path):
    genresID = dict()
    files = os.listdir(path)
    files = [file for file in files if file.endswith(".mp3")]
    nbFiles = len(files)

    #Create path if not existing
    if not os.path.exists(os.path.dirname(SPECTROGRAMS_PATH)):
        print("Creating {}...".format(SPECTROGRAMS_PATH))
        os.makedirs(os.path.dirname(SPECTROGRAMS_PATH))

    #Rename files according to genre
    for index,filename in enumerate(files):
        print("Creating spectrogram for file {}/{}...".format(index+1,nbFiles))
        fileGenre = getGenre(AUDIO_DIR + filename)

        genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
        fileID = genresID[fileGenre]

        newFilename = fileGenre +"_"+str(fileID)
        create_spectrogram(AUDIO_DIR + filename,newFilename)

def create_slices():
	for filename in os.listdir(SPECTROGRAMS_PATH):
		if filename.endswith(".png"):
			slice_spectrogram(filename,128)

def slice_spectrogram(filename, desiredSize):
	genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

	# Load the full spectrogram
	img = Image.open(SPECTROGRAMS_PATH+filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize

	#Create path if not existing
	slicePath = SLICES_PATH+"{}/".format(genre);
	if not os.path.exists(os.path.dirname(slicePath)):
		try:
			os.makedirs(os.path.dirname(slicePath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#For each sample
	for i in range(nbSamples):
		print("Creating slice: ", (i + 1), "/", nbSamples, "for", filename)
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save(SLICES_PATH + "{}/{}_{}.png".format(genre,filename[:-4],i))

# create_all_spectrograms(AUDIO_DIR)
create_slices()