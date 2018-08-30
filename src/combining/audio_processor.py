from pydub import AudioSegment
import pickle
import os

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_PATH = os.path.dirname(SCRIPT_PATH) + "\\"

def create_audio(audio_files):
    songs = []
    piece = AudioSegment.empty()
    duration = 1* 1000

    for slice in audio_files:
        slice_index = audio_files[1]
        seconds_from_start = make_seconds(slice_index)

        print('Loading {} ...'.format(slice[0]))
        song = AudioSegment.from_mp3(slice[0])
        songs.append(song)

        piece = piece + song[seconds_from_start:seconds_from_start + duration]

    piece.export(SCRIPT_PATH + 'mashup.mp3', format='mp3')

    print('Done')   

def make_seconds(slice_index):
    return slice_index * 1000

def main():
    with open(SCRIPT_PATH + 'slices.bin', 'rb') as slfile:
        files = pickle.load(slfile)

    print('Loaded')
    create_audio(files)
    
if __name__ == '__main__':
    main()
