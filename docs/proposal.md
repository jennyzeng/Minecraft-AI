---
layout: default3
title: Proposal
---

## Summary of the Project

Our Minecraft-AI project will basically focus on **biome recognition** in Minecraft. Input an image that a Minecraft agent observes, it will give a prediction about what kind of biome is in the the image. 

### Biome in Minecraft

A [biome](http://minecraft.gamepedia.com/Biome) is a region in Minecraft world with some specific geographical features such as flora and heights. Image below from [Gamepedia](http://minecraft.gamepedia.com/) shows a picture of a forest biome in Minecraft. 

<img src="https://hydra-media.cursecdn.com/minecraft.gamepedia.com/d/d1/Deciduous_Forest.png?version=a2315c785dbfd1fce8b768923aa98540" width="50%">

Our first step is to do binary classification on a specific kind of biome. If time permits, we will make classification on a few different kinds of distinguishing biomes. 

### Collect data

We will generate biomes with xml in Malmo to capture image data with labels for training and testing. 

## AI/ML Algorithms

We are preparing to use [TensorFlow](https://www.tensorflow.org/) and implementing a Convolutional Neural Network(CNN) for image recognition. Some other possible frameworks are [Caffe](http://caffe.berkeleyvision.org/), [CNTK](https://www.microsoft.com/en-us/research/product/cognitive-toolkit/) and [Scikit-Learn](http://scikit-learn.org). Besides CNN, we may also test the performance of SVM classifier, Random Forest, Gradient Boosting, and so on.

To accelerate the training process, we would use [Amazon Web Service](aws.amazon.com) and [Docker](https://www.docker.com/) with GPU. 

## Evaluation Plan

We expect to evaluate the project result based on the accuracy of the biome recognition. We generate different sets of training and testing data. Then we calcuate the Area Under Curve (AUC), which is a metric for binary classification, for our training data and testing data and plot graphs. We will compare the AUC of output with different parameters and choose the parameters that yields better performance.

## References

[http://minecraft.gamepedia.com/Biome](http://minecraft.gamepedia.com/Biome)

[https://www.tensorflow.org/tutorials/layers](https://www.tensorflow.org/tutorials/layers)

[http://www.deeplearningbook.org/contents/convnets.html](http://www.deeplearningbook.org/contents/convnets.html)

[http://cs231n.github.io/convolutional-networks/](http://cs231n.github.io/convolutional-networks/)

[https://www.youtube.com/watch?v=FmpDIaiMIeA](https://www.youtube.com/watch?v=FmpDIaiMIeA)

[https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html#element_FlatWorldGenerator](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html#element_FlatWorldGenerator)