import os
import sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools import get_image_data

SLICES_PATH = 'D:\\Repositories\\AudioClassification\\slices\\'

genres_count = { }


def load_slices():
    data = [] 
    for genre in os.listdir(SLICES_PATH):
        files = os.listdir(SLICES_PATH + genre + '\\')
        genres_count[genre] = len(files)

        for file in files:
            image_data = get_image_data(SLICES_PATH + genre + '\\' + file, 128)
            data.append((np.array(image_data).reshape(-1), genre))
            print('Read {}'.format(SLICES_PATH + genre + '\\' + file))
    return data

def main():
    data = np.array(load_slices())
    print(data.shape)
    print(data[0])
    print(data[0].shape)
    print(len(data))

    print('Clusterizing...')
    kmeans = KMeans(n_clusters=4, random_state=0).fit([i[0] for i in data])

    i = 0
    print('Metal: ')
    bins = np.bincount(kmeans.labels_[i:genres_count['Metal']])
    print(bins)
    print('Percentage: ')
    print(['%.2f' % (c / bins.sum()) for c in bins])

    i = i + genres_count['Metal']
    print('Pop: ')
    bins = np.bincount(kmeans.labels_[i:i + genres_count['Pop']])
    print(bins)
    print('Percentage: ')
    print(['%.2f' % (c / bins.sum()) for c in bins])
    
    i = i + genres_count['Pop']
    print('Punk: ')
    bins = np.bincount(kmeans.labels_[i:i + genres_count['Punk']])
    print(bins)
    print('Percentage: ')
    print(['%.2f' % (c / bins.sum()) for c in bins])

    i = i + genres_count['Punk']
    print('Rap: ')
    bins = np.bincount(kmeans.labels_[i:i + genres_count['Rap']])
    print(bins)
    print('Percentage: ')
    print(['%.2f' % (c / bins.sum()) for c in bins])

    

if __name__ == '__main__':
    main()