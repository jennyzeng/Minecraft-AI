from PIL import Image
import numpy as np

def imageResize(infile, outfile, size):
    """
    :param infile: input img
    :param outfile: output img
    :param size: max size for the img
    :return: return the resized im
    """
    try:
        im = Image.open(infile)
        im.thumbnail(size,Image.ANTIALIAS)
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
    arr = np.array(img) # w * h *3 array
    return arr
if __name__ == '__main__':
    # imageResize('img/starry-night.jpg', 'out.jpg', (128, 128))
    arr = convertToArray('out.jpg')