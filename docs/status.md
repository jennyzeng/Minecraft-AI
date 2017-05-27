---
layout: default
title: Proposal
---

## Project summary

## Approach

### Data Collection

​	Since we have three different classifications, we need to collect three types of the data. For biome classification, we have collected 50,000 images, namely, 10,000 images per biome. Specifically, we generate a single biome world for each biome type with different weathers and run multiple Malmo sessions in this world to collect data. In this way, we can know the ground truth of each image directly. For weathers classification, we have gathered 1,000 images under five different biomes for each of the four kinds of weather ("rain", "thunder", "clear" and "normal"), that is, 5000 images in total. We think that weather is more structured to recognize biomes, so we decided to collect fewer data. For pig classifications, we only collect 100 images of a pig in a fence since the data of pig is much more structured with many pink blocks.

​	In each Malmo session, the agent starts with a random position in the world, and then walk a random distance and rotate an arbitrary angle. We record the whole mission using the recordMP4 function, then get frames from the video every 0.5 seconds and save the array of pixels into images using PIL module. Therefore, for each biome, we collect 10000 screenshots that have different time(morning, noon and night).The image size is 320\*200 pixels, which is smaller than the default Minecraft size (640*400 pixels) to save some storage space. 

![image16](imgs/status/image16.png)

​	There may be some errors in our data because our agent sometimes walks into the ground, or inside mountains. Sometimes, the agent collects images that are mostly sky. We tried to delete as much bad data as possible manually.

### How to deal with the data

​	After we collect the data, we deal with the images in two different ways, one for the Convolutional Neural Network (CNN), and the other for the traditional Machine Learning (ML) methods. Given the large size of our image data, we found it impractical to load all images to the memory at one time for training and testing. 

​	For the CNN, since we want to keep the original images and use a small batch of data to train the model. We convert our dataset to two [tfrecord](http://warmspringwinds.github.io/tensorflow/tf-slim/2016/12/21/tfrecords-guide/)  files (training/testing). We also use a FIFO queue with 3 threads to read the tfrecord and get a random batch every time we call it. In contrast to what we do for CNN, we convert an 320x200x3 image to data with 24 features for the traditional ML methods. Because of the difference in colors, human can recognize if an image is showing a mesa biome or a forest biome at a glance. That gives us an inspiration: is it possible to classify a biome simply based on the colors? For each image in the dataset, we extract colors using OpenCV module. An image is represented as an np array with shape (320,200,3) in python.There are three channels, R,G,B, for an image, and in each channel there are 320x200 cells. Value in each cell vary between 0 and 255, inclusive. We get a histogram with 8 bins for each channel, that is, we divide range 0-255 into 8 small ranges. For each bin (e.g. range 0-32), we count the number of cells with value in that range. The histogram shown below represent the result for the mesa image at the left. 

​	For traditional Machine Learning (ML) methods, we want to use txt file and scikit-learn to train the model. After we get 8 bin values for each channel, and 24 bin values in total as an 8x3 array above, we flatten it to be an 1-d array and write it as a row to a txt file with a corresponding label. Since the size of data is significantly reduced, we can now load all the training data and test data for training using scikit-learn. 

### Traditional ML

​	We know that some biomes(datasets) are pretty structured, so we decide to try Traditional Machine learning methods to see if they have better performance in these biomes. Specifically, since the colors(RGB) of desert and mesa are very distinguishable, the dataset for this biome is pretty structured and we want to try SVM and random forest to deal with it.	

​	Since we have three classes, R, G and B, We have tried MultiOutputClassifier with SVM and random forest with njobs=3. SVM is defined by a convex optimisation problem (no local minima) for which there are efficient methods and helps avoid over-fitting. However, SVM was very inefficient to train especially with large dataset. So we prefer using random forest.Random forest, because it is nothing more than a bunch of Decision Trees combined, can handle categorical (binary) features very well. The other main advantage is that, because of how it is constructed (used bagging) these algorithms handle very well high dimensional spaces as well as large number of training examples.	

​	We train our model with our large dataset which transformed 50,000 images for 5 different biomes to txt file. At the end, we test the performance of our training result using the test data in the separated test txt. The test error rate is 5.29%.The figure 1 and 3 in the Evaluation session illustrates more detail about the performance of the result on different biome classes.

### CNN

Some traditional machine learning methods, such as Support Vector Machine (SVM), have bad performance when the dataset has a lot of features. For an image, we can view each pixel as a feature, so an image with size 320x200x3 will have 192,000 features, which is unmanageable by the SVM. By the way, we make those methods workable for our large size data is to extract RGB histograms from each images as features. However, it does not maintain the basic structure of an image and loses too much information (e.g. shape) of it. On the contrary, [Convolutional Neural Networks](http://cs231n.github.io/convolutional-networks/#conv) take advantage of the fact that the the input consists of images and they constrain the architecture in a more sensible way. For example, the CONV layer in CNN extract image features with convolution operation.

We implement a CNN model based on the instructions from [https://www.tensorflow.org/get_started/mnist/mechanics](https://www.tensorflow.org/get_started/mnist/mechanics) and [https://www.tensorflow.org/get_started/mnist/beginners]( https://www.tensorflow.org/get_started/mnist/beginners). First, we pick about 200 images randomly from the training tfrecord as the validation data. Then we reload train tfrecord again for the training data input later. Note that for all the data we feed into the CNN, values in each image are rescaled from [0, 255] down to [-0.5, 0.5] and data type is casted to float32. This is necessary because we feed the data into the training/prediction nodes(represented as tf variables) only accept data in some some specific types. We construct our CNN model which consists of 2 conv2d, 2 relu, 2 max pooling, 1 hidden, and 1 dropout layers.  

![image6](imgs/status/image6.png)

We train our model with our large dataset which contains 50,000 images for 5 different biomes. At the end, we test the performance of our training result using the test data in the separated test tfrecord file. 

​	

## Evaluation

​	Our evaluation plan will have two parts. One is the quantity evaluation and the other is the quality evaluation. For the quantity evaluation, we use 1,000 images each different biomes to train and 9000 images to test and see the correctness.we have calculated the error rate and the incidence proportion for both CNN and random forest model with following two formula. 

 $$i = \frac{\textrm{number of (Predicted label } i \textrm{ AND Actual label i)}}{\textrm{number of Actual label i}} $$ 

And Incidence proportion for label 

$$i = \frac{\textrm{number of (Predicted label } i \textrm{AND Actual label } i)}{\textrm{number of Predicted label } i} $$

 For quality part, we have  



### Quantitative part

​	For quantitation evalution, we want to 



 we get a histogram with 8 bins for each channel, that is, we divide range 0-255 into 8 small ranges. For each bin (e.g. range 0-32), we count the number of cells with value in that range. The histogram shown below represent the result for the mesa image at the left. 





​	Figure 1 and 3 has shown the performance of Random Forest. We train our model with our large dataset which transformed 50,000 images for 5 different biomes to txt file. At the end, we test the performance of our training result using the test data in the separated test txt. The overall test error rate is 5.29%. In figure 3 we calculated the error rate and the incidence proportion.We get the best prediction result for the mesa biome with class label 0, because it predicts 1950 test images correctly and the error rate is 0.9%.But we get pretty bad error rate 9.3% for the eh (extreme hill) biome with label 4 and error rate 9.5% the forest biome with label 1. 

​	Figure 2 and 4 has shown the performance of CNN. We train our model with our large dataset which contains 50,000 images for 5 different biomes. At the end, we test the performance of our training result using the test data in the separated test tfrecord file. The overall test error rate is 4.7%. The figure below illustrates the performance of the result on different biome classes. We get the best prediction result for the desert biome with class label 0, because it predicts 989 test images correctly and the error rate is 0.8%. But we get the worst error rate 17% for the forest biome with label 1.  

![image17](imgs/status/image17.png)



![image18](imgs/status/image18.png)

![image19](imgs/status/image19.png)

![image20](imgs/status/image20.png)

### Quality part

<img src="imgs/status/image21.png" width="70%">



<img src="imgs/status/image22.png" width="70%">

<img src="imgs/status/image23.png" width="100%">