from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import random

from PIL import Image

import sys

def shuffle_img(img, indices):
    """
    img: a numpy array of uint8 from an image.
    indices: a n-dimensional array that gives the position of each of the
    n subdivisions of the image.
    """
    y = img.shape[1] # number of columns
    z = img.shape[2] # number of channels (3 for RGB)
    n = len(indices)

    result = np.zeros(img.shape)
    stride = y//n
    rest = y - stride*n

    lop = [(i*stride+rest, i*stride+stride+rest) for i in range(n)]
    for i in range(rest):
        lop[i] = (lop[i][0]-(rest-i),lop[i][1]-(rest-i-1))

    for i in range(z):
        idx = 0
        for nidx in indices:
            start,end = lop[nidx]
            result[:,idx:idx+(end-start),i] = np.copy(img[:,start:end,i])
            idx += (end-start)
            
    return result

def save_perm_phrase(words, indices):
    """
    words: array of words in a phrase.
    indices: array of indices corresponding to each word.
        The i-th value in indices is the index of the 
        indices[i]-th word in words
    Returns the words permuted as stipulated by indices.
    """
    perm = []
    to_save = ''
    for i in indices:
        perm += [words[i]]
    for i in range(len(perm)):
        to_save += perm[i] + ' '
    to_save += '\n'
    return to_save

if __name__ == "__main__":
    img_path = sys.argv[1]

    phrase = input('Your phrase: ')

    words = phrase.split(' ')

    image = np.asarray(Image.open(img_path))
    indices = np.array(range(len(words)))
    random.shuffle(indices)

    to_save = save_perm_phrase(words, indices)
    perm_image = shuffle_img(image,indices)

    img = Image.fromarray(np.uint8(perm_image))
    img.save('perm'+img_path)
    fl = open(words[0] + '.txt', mode='w')
    fl.write(to_save)
    fl.close()

