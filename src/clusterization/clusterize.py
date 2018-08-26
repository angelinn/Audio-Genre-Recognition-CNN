import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools import get_image_data

SLICES_PATH = 'D:\\Repositories\\AudioClassification\\slices\\'

def load_slices():
    data = []
    for genre in os.listdir(SLICES_PATH):
        for file in os.listdir(SLICES_PATH + genre + '\\')[:10]:
            image_data = get_image_data(SLICES_PATH + genre + '\\' + file, 128)
            data.append(image_data)
            print('Read {}'.format(SLICES_PATH + genre + '\\' + file))
    return data

def main():
    data = load_slices()
    print(data)
    print(len(data))

if __name__ == '__main__':
    main()