#adapted from http://bretahajek.com/2017/04/importing-multiple-tensorflow-models-graphs/

import tensorflow as tf


class ImportGraph():
    """  Importing and running isolated TF graph """

    def __init__(self, loc):
        # Create local graph and use it in the session
        print "init graph"
        print "init session"
        self.graph = tf.Graph()
        self.sess = tf.InteractiveSession(graph=self.graph)
        print "after init"
        print "make saver"
        with self.graph.as_default():
            saver = tf.train.import_meta_graph(loc + '.meta',
                                               clear_devices=True)
            saver.restore(self.sess, loc)
            # Get activation function from saved collection
            # You may need to change this in case you name it differently
            print "restored"
            self.graph = tf.get_default_graph()
            print "get graph"
        #self.activation = tf.get_collection('activation')[0]
        print "finish save"

    def run(self, prediction, feed_dict):
        """ Running the activation function previously imported """
        # The 'x' corresponds to name of input placeholder
        return self.sess.run(prediction, feed_dict)


if __name__ == "__main__":
    ### Using the class ###
    data = 50  # random data
    model = ImportGraph('models/model_name')
    result = model.run(data)
    print(result)