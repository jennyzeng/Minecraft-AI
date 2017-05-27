---
layout: default
title: Proposal
---

## Summary of the Project

Our Minecraft-AI project will basically focus on **biome recognition** in Minecraft. Input an image that a Minecraft agent observes, our model will give a prediction about what kind of biome is in the the image. More specifically, we will train the model with many images that the Minecraft agent observes, let the model learn the pattern with these training images, use the model to predict test(new) images and see the expected types of output.

### Biome in Minecraft

A [biome](http://minecraft.gamepedia.com/Biome) is a region in Minecraft world with some specific geographical features such as flora and heights. Image below from [Gamepedia](http://minecraft.gamepedia.com/) shows a picture of a forest biome in Minecraft. 

<img src="https://hydra-media.cursecdn.com/minecraft.gamepedia.com/d/d1/Deciduous_Forest.png?version=a2315c785dbfd1fce8b768923aa98540" width="50%">

Our first step is to do binary classification on a specific kind of biome (such as ocean or forest). If time permits, we will make classification on a few different kinds of distinguishing biomes. Each biome have a main color, and information about the temperature.

### Collect data

The data we need to collect is the images about the Biome. We will generate biomes with xml in Malmo to capture image data with labels for training and testing. We plan to have at least 500 samples as the training data and first make the samples balanced. If time permits, we will also test the imbalanced data if neeeded.


## AI/ML Algorithms

Recognizing biome is an classification problem. Image recognition/classification is widely applied with Convolutional Neural Network(CNN). Besides CNN, we may also test the performance of SVM classifier, Random Forest, Gradient Boosting, because these are some good methods for solving classification problems. We are also open to other algorithms during research.

We plan to use [TensorFlow](https://www.tensorflow.org/) framework and implement a Convolutional Neural Network(CNN) for image recognition. Some other possible frameworks are [Caffe](http://caffe.berkeleyvision.org/), [CNTK](https://www.microsoft.com/en-us/research/product/cognitive-toolkit/) and [Scikit-Learn](http://scikit-learn.org). 

To accelerate the training process, we will use [Amazon Web Service](aws.amazon.com) and [Docker](https://www.docker.com/) with GPU. 

## Evaluation Plan

Our evaluation plan will have two parts. One is the quantity evaluation and the other is the quality evaluation. For the quantity evaluation, we plan to use at least 200 image to test and see the correctness.For the quality evaluation, We expect to evaluate the project result based on the accuracy of the biome recognition. We generate different sets of training and testing data. Then we calcuate the error rate (provided by tensor flow) , which is a metric for binary classification, for our training data and testing data and plot graphs. We will compare the AUC of output with different parameters and choose the parameters that yields better performance.

## References

[http://minecraft.gamepedia.com/Biome](http://minecraft.gamepedia.com/Biome)

[https://www.tensorflow.org/tutorials/layers](https://www.tensorflow.org/tutorials/layers)

[http://www.deeplearningbook.org/contents/convnets.html](http://www.deeplearningbook.org/contents/convnets.html)

[http://cs231n.github.io/convolutional-networks/](http://cs231n.github.io/convolutional-networks/)

[https://www.youtube.com/watch?v=FmpDIaiMIeA](https://www.youtube.com/watch?v=FmpDIaiMIeA)

[https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html#element_FlatWorldGenerator](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html#element_FlatWorldGenerator)
