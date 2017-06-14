from PIL import Image
import numpy as np
import cv2

def imageResize(infile, outfile, size):
    """
    :param infile: input img
    :param outfile: output img
    :param size: max size for the img
    :return: return the resized im
    """
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(outfile, "JPEG")
    except IOError:
        print "cannot create thumbnail for '%s'" % infile
    return im


def convertToArray(infile):
    """
    Reference: http://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
    :param infile: input img
    :return: an w*h*3 np array storing the img info
    """
    img = Image.open(infile)
    arr = np.array(img)  # w * h *3 array
    return arr


def saveArrayAsImg(array, width, height, outfile, wantDepth=False, outfile_d=None):
    array = np.array(array)
    array = array.reshape(height, width, 3)
    im = Image.fromarray(array, mode='RGB')
    im.save(outfile)
    return True


def resizeImg(pixels, target_height, target_width, record_height, record_width):
    # process for image classification later
    img = np.array(pixels)
    img = img.reshape(record_height, record_width, 3)
    resized_img = cv2.resize(img, (target_width, target_height))

    return resized_img


def rescaleImg(resized_img):
    """
    for CNN only!
    :param resized_img:
    :return:scaled down from 255 to -0.5 to 0.5
    """
    resized_img = resized_img.astype(np.float32)
    return (resized_img - (255 / 2.0)) / 255


def imgHistograms(img, NUM_BINS=8, COLOR=('b', 'g', 'r')):
    """
    for SK learn
    :param resized_img:
    :return: histograms for resized img, no label
    """
    hist = np.zeros((NUM_BINS, 3))
    for i, col in enumerate(COLOR):
        histr = cv2.calcHist([img], [i], None, [NUM_BINS], [0, 256])
        hist[:, i] = histr[:, 0]
    hist = hist.flatten()
    return hist


# 1000*1600
if __name__ == '__main__':
    # imageResize('img/starry-night.jpg', 'out.jpg', (128, 128))
    arr = convertToArray('out.jpg')
