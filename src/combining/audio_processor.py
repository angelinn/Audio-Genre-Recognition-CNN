from pydub import AudioSegment
import pickle
import os

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_PATH = os.path.dirname(SCRIPT_PATH) + "\\"

def create_audio(audio_files):
    songs = []
    piece = AudioSegment.empty()
    duration = 1 * 1000
    start = 30 * 1000

    for slice in audio_files:
        print('Loading {} ...'.format(slice[0]))
        song = AudioSegment.from_mp3(slice[0])
        songs.append(song)

        piece = piece + song[start:start + duration]

    piece.export(SCRIPT_PATH + 'mashup.mp3', format='mp3')

    print('Done')   

def main():
    with open(SCRIPT_PATH + 'slices.bin', 'rb') as slfile:
        files = pickle.load(slfile)

    print('Loaded')
    create_audio(files)
    
if __name__ == '__main__':
    main()
