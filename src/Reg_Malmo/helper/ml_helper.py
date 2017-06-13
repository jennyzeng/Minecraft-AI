import numpy as np
import cv2

class ML_Helper:
    @staticmethod
    def convertImage(img,label,NUM_BINS):
        """
        :param img: a 3 channel image
        :param label: label of this image
        :param NUM_BINS: how many bins we have for each channel in histogram
        :return: 3 channels histogram. a 1-d array with length 3*NUM_BINS+1. the last col
                is the label.
        """
        COLOR = ('b', 'g', 'r')  # channel order in array
        hist = np.zeros((NUM_BINS,3))
        for i,col in enumerate(COLOR):
            histr = cv2.calcHist([img],[i],None,[NUM_BINS],[0,256])
            hist[:,i] = histr[:,0]
        hist = hist.flatten()
        hist = np.append(hist, label)
        return hist

    @staticmethod
    def convertLabel(lab, NUM_LABELS):
        """
        :param lab: 1 d array
        :return: convert to 1 hot labels
        """
        return (np.arange(NUM_LABELS) == lab[:, None]).astype(np.float32)

    @staticmethod
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

    @staticmethod
    def find_maj(predictions):
        """
        :param predictions: a np array of prediction labels
        :return: only return the majority in prediction if
                the occurrence of maj >= len(predictions)//2
                else return None
        """
        maj = np.bincount(predictions).argmax()
        if (predictions == maj).sum() >= len(predictions)//2:
            return maj
        return None


    @staticmethod
    def array_err_rate(err):
        """
        :param err: a list like [0,1,0]
        :return: the portion of 1 in it.
        """
        return 100.0 * float(sum(err)) / (float(len(err)))
