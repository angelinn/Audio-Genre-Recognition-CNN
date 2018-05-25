from subprocess import Popen, PIPE, STDOUT
import eyed3
import os

SOX_PATH = 'D:\\Program Files (x86)\\sox-14-4-2\\sox'
AUDIO_DIR = 'D:\\Repositories\\AudioClassification\\fma_small\\000\\'
SPECTROGRAMS_PATH = 'spectrograms\\'

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

create_all_spectrograms(AUDIO_DIR)
