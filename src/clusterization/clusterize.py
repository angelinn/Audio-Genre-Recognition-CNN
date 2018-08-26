import os
import sys
import numpy as np
from sklearn.cluster import KMeans

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

    X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print(kmeans.labels_)
    print(kmeans.predict([[0, 0], [4, 4]]))
    print(kmeans.cluster_centers_)

if __name__ == '__main__':
    main()