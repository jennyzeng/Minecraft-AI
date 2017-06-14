import numpy as np

class ML_Helper:

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
        return 100.0 * float(sum(err)) / (float(len(err))+(len(err)==0))
