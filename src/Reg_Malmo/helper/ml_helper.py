import numpy as np
import cv2



def convertImage(img,label,NUM_BINS,COLOR):
   # img=cv2.imread(img_path)
   # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = np.zeros((NUM_BINS,5))
    bins = np.linspace(0, 256, NUM_BINS)
    for i,col in enumerate(COLOR):
        histr = cv2.calcHist([img],[i],None,[NUM_BINS],[0,256])
        hist[:,i] = histr[:,0]
    hist = hist.flatten()
    hist = np.append(hist, label)
    return hist


def convertLabel(lab):
    """TODO: change 5 to a param, and change related stuff in other functions
    :param lab: 1 d array
    :return: convert to 1 hot labels
    """
    return (np.arange(5) == lab[:, None]).astype(np.float32)

def convertLabelp(labp):
    """
    TODO: please delete this one :)
    """
    return (np.arange(2) == labp[:, None]).astype(np.float32)


def error_rate(predictions, labels):
   # Return the error rate and confusions.
    correct = np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
    total = predictions.shape[0]

    error = 100.0 - (100 * float(correct) / float(total))

    confusions = np.zeros([5, 5], np.float32)
    bundled = zip(np.argmax(predictions, 1), np.argmax(labels, 1))
    for predicted, actual in bundled:
        confusions[predicted, actual] += 1

    return error, confusions
