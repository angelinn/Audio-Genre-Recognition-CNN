from subprocess import Popen, PIPE, STDOUT
import eyed3
import os
from PIL import Image

SOX_PATH = 'D:\\Program Files (x86)\\sox-14-4-2\\sox'
AUDIO_DIR = 'D:\\Repositories\\AudioClassification\\fma_small\\'
NEW_AUDIO_DIR = 'D:\\Repositories\\AudioClassification\\mono\\'
SPECTROGRAMS_PATH = 'spectrograms\\'
SLICES_PATH = 'slices\\'
#GENRES = ['Electronic', 'Folk', 'Hip Hop', 'Jazz', 'Pop', 'Punk', 'Rock']
GENRES = ['Hip-Hop']

def create_spectrogram(path, filename, new_path, new_file_name):
    if isMono(path + filename):    
        command = "xcopy /y \"{}{}\" \"{}{}\"".format(path, filename, new_path, filename)
    else:
        command = "\"{}\" \"{}{}\" \"{}{}\" remix 1,2".format(SOX_PATH, path, filename, new_path, filename)
    
    pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False, cwd='D:\\Repositories\\AudioClassification\\')
    output, errors = pipe.communicate()
    if errors:
        print(errors)
    

    command = "\"{}\" \"{}{}\" -n spectrogram -Y 200 -X {} -m -r -o \"{}.png\"".format(SOX_PATH, new_path, filename, 50, SPECTROGRAMS_PATH + '\\' + new_file_name)
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


genresID = dict()
def create_all_spectrograms(path):
    files = os.listdir(path)
    files = [file for file in files if file.endswith(".mp3")]
    nbFiles = len(files)

    #Create path if not existing
    if not os.path.exists(os.path.dirname(SPECTROGRAMS_PATH)):
        print("Creating {}...".format(SPECTROGRAMS_PATH))
        os.makedirs(os.path.dirname(SPECTROGRAMS_PATH))
    
    #Create path if not existing
    if not os.path.exists(os.path.dirname(NEW_AUDIO_DIR)):
        print("Creating {}...".format(NEW_AUDIO_DIR))
        os.makedirs(os.path.dirname(NEW_AUDIO_DIR))

    #Rename files according to genre
    for index,filename in enumerate(files):
        print("Creating spectrogram for file {}/{}...".format(index+1,nbFiles))
        fileGenre = getGenre(path + filename)
        if fileGenre not in GENRES:
            print("Genre is {}. Skipping...".format(fileGenre))
            continue

        genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
        fileID = genresID[fileGenre]

        newFilename = fileGenre +"_"+str(fileID)
        create_spectrogram(path, filename, NEW_AUDIO_DIR, newFilename)

def create_slices():
	for filename in os.listdir(SPECTROGRAMS_PATH):
		if filename.endswith(".png"):
			slice_spectrogram(SPECTROGRAMS_PATH, filename, 128, SLICES_PATH)

def slice_spectrogram(path, filename, desiredSize, slices_path):
	genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

	# Load the full spectrogram
	img = Image.open(path+filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize

	#Create path if not existing
	slicePath = slices_path+"{}/".format(genre);
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
		imgTmp.save(slices_path + "{}/{}_{}.png".format(genre,filename[:-4],i))

def isMono(filename):
	audiofile = eyed3.load(filename)
	return audiofile.info.mode == 'Mono'

if __name__ == '__main__':
    directories = next(os.walk(AUDIO_DIR))[1]
    print(directories)
    for dir_name in directories:
        print(AUDIO_DIR + '\\' + dir_name)
        create_all_spectrograms(AUDIO_DIR + '\\' + dir_name + '\\')

    create_slices()