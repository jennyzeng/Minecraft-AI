from PIL import Image
import numpy as np
import tensorflow as tf
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

def saveArrayAsImg(array, width, height, outfile, wantDepth=False, outfile_d=None):
    array = np.array(array)
    # if wantDepth:
    #     array = array.reshape(height,width,4)
    #     im = Image.fromarray(array[:,:,:3], mode='RGB')
    #     im.save(outfile)
    #     d_array = array[:,:,3:]
    #     d_array = d_array.reshape(height,width)
    #     im_depth = Image.fromarray(d_array, mode='L')
    #     #im_depth.save(outfile_d)
    # else:

    array = array.reshape(height,width,3)
    im = Image.fromarray(array, mode='RGB')
    im.save(outfile)
    return True

# process for tf classification later
def scaleImg(pixels, target_height, target_width, record_height, record_width):
    # I reset the want_depth in xml, so now I only have 3 channels
    img = np.array(pixels)
    img = img.reshape(record_height, record_width, 3)
    # img = Image.fromarray(array[:, :, :3], mode='RGB')

    resized_img = tf.image.resize_image_with_crop_or_pad(image=img,
                                           target_height=target_height,
                                           target_width=target_width)

    resized_img = resized_img.eval()
    resized_img = resized_img.astype(np.float32)
    return (resized_img-(255/2.0)) / 255






#1000*1600
if __name__ == '__main__':
    # imageResize('img/starry-night.jpg', 'out.jpg', (128, 128))
    arr = convertToArray('out.jpg')