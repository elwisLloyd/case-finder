# Using AI to automate product photo selection

Источник: https://medium.com/prosus-ai-tech-blog/using-ai-to-automate-product-photo-selection-60bddfad99a9

Luis Armando Pérez Rey (Main Contributor), Dmitri Jarnikov
We want to find an easy way to select product photos that show its attributes in the best light.
Imagine that you want to sell an item online. You’ve created a title for your listing, put a few words into the description, and now you must take some photos to upload along with the text. You move around, you look from everywhere, take several pictures, and after some time, you feel like you are done. The only thing left is to select the best photos from the ones you took. But how do you decide which photos show the item in the best light, so people will be inclined to buy it? Let’s say you want to advertise a car online. Which photo would be the best to emphasize its type, its colour, or its condition? Is there an easy way to answer this question?
Yes, there is. Instead of making pictures and spending a lot of time selecting the best ones, you just take a video of your item, upload it to the internet, pick object attributes that are most relevant and, magically see a selection of the images that best highlight your product.
Now, it sounds nice and beautiful but…. how can it be done?
Basic hypothesis
Let’s start with our hypothesis: Image classifiers can be used to assess how well an attribute is portrayed in an image.
The rationale behind the hypothesis goes as follows. When we train an image classifier to predict an object’s attribute from an image, the classifier learns to identify the visual features that are best to predict that attribute. The quality of inference depends on the ability of the model to observe these features in the image. The more pronounced the features are, the more certain the classifier is in its predictions. We can then interpret the certainty as a way to identify the quality of an image with respect to its ability to portray the object’s attribute.
If we treat a video as a collection of images, a simple image classifier can then tell us which of them yields highly certain predictions about a particular object’s attribute. These images are, therefore, good candidates to highlight the attribute.
Implementing the solution
Now, let’s put the hypothesis to test. To move a mountain, we need to start by carrying small rocks, so we start with a proof of concept. Our PoC will focus on cars because a) cars are a very common product to sell, b) there is a well-established list of car attributes to choose from, c) we have plenty of labelled data for training models.
We train a model to predict attributes such as car type, brand, number of doors, and number of seats. The model can also predict the orientation of the front of the car with respect to the camera.
Data attributes
The attributes have the following values:
- Type: 12 types, e.g., Sedan, Hatchback, Estate.
- Brand: 161 brands.
- Number of doors: from 2 to 5.
- Number of seats: 2,4,5, or more than 5.
- Orientation: a continuous value from 0 and 360.
Dataset
We use two datasets: PASCAL3D+[3] and CompCars[4]. The former is used to train a predictor for the car’s orientation. The latter is used for training the rest of the predictors.
Model
We use a probabilistic classifier with multiple predictions, one per attribute, on top of a feature extractor. In particular, we use InceptionResnetV5 [1] pre-trained on ImageNet [2] as feature extractor for our model. The probabilistic nature of our classifier allows us to obtain a certainty measure for each attribute's predictions. This means that the model can be fed with images of cars and produce a prediction for the corresponding attributes and measure the certainty of that prediction.
Predicting certainty
As we have mentioned, we assume that the certainty of a model’s prediction serves as a measure of an image’s quality in depicting the corresponding attribute. Higher certainty in a prediction means higher quality. Probabilistic classifiers provide natural ways of representing the certainty¹ of a prediction with respect to a probability distribution over a neural network's possible predictions. In the case of the car's attributes, we have two possible types of distributions: discrete and continuous.
Get Dmitri Jarnikov’s stories in your inbox
Join Medium for free to get updates from this writer.
Attributes such as type, brand, number of doors, and number of seats are discrete. This means that each of the attribute predictions that we produce for an image should show a probability distribution over all possible interest classes. This distribution can be achieved by using a softmax activation function in the last layer of each of the corresponding predictions. The entropy of the probability distribution determined by the softmax can be considered a measure of the prediction's uncertainty, where higher entropy means less certainty.
Predictions for the car's orientation are a continuous probability density over the possible angles of the relative orientation a car can have with respect to the camera that took the picture. We use the approach presented in [5] to build the orientation model. The output of the prediction is two-fold: a location parameter that determines the most likely angle that an image is predicted into and a scale parameter that represents the certainty of the prediction. The output of the orientation tells us the predicted angle for an image and a measure of the certainty of that prediction.
Together the predictions obtained from a single image provide a way to select the appropriate images that best represent the attributes of the car.
Training
We train each attribute predictor separately via transfer learning by freezing the feature extractor and the layers corresponding to the other attributes' predictions. We select the appropriate dataset during training and update the network parameters to predict the correct attribute with respect to the available labels. Given an input image, the trained model can produce a prediction and certainty level for each attribute.
Frame selection from video
We select one frame from a video that yields prediction with the highest certainty by the corresponding model for each discrete attribute of the car.
In the examples below, the video frames are processed one by one, and the image with the highest certainty at the moment is shown on the right.
Graphs in the middle of each example show the prediction certainty for each attribute's value averaged across the predictions made to the given point in the video.
We use the orientation predictor to extract 8 frames from the video that shows the object from different (approximately equally spaced) angles. The 360 degrees range is divided into eight bins that correspond to angle ranges that the car's orientations should fall into. For each processed frame in a video, if the prediction’s probability for an angle exceeds a threshold of 0.8 and the prediction of the orientation is within one of the empty bins, then the image is selected, and the bin is filled with that image.
Furthermore, the predictions obtained for the orientation can be used to order the selected frames and also to create a map that shows which angles have been observed in the video. The more certain a prediction for a frame is, the more it contributes to this map. In the example video below, the coverage map is depicted as the blue line, whereas the red line corresponds to the prediction for the frame shown at the given moment.
What comes next?
We have built a proof of concept of a method that can automatically highlight a car's attributes from a video. Now there are still some challenges to overcome for taking this simple idea to the next level.
- We need to find ways to efficiently train classifiers to predict any object's attributes, not only for cars, without relying on labelled datasets. One such option is to use unsupervised methods to highlight objects' visual attributes without the need for large amounts of labels [6, 7].
- We shall harness the information about the temporal correlation of frames. Right now, the predictions for the video are obtained by processing frames individually without any attention to the valuable temporal information. Further improvements shall include the addition of different neural network architectures for handling a sequence of images.
- We shall investigate the trade-off between the computational complexity of the model and its accuracy. Using a larger neural network as a feature extractor can achieve better results but require significantly more computational resources.
¹We assume that the output probability distribution over the classes or regression values can be used to estimate the certainty of a prediction in terms of its entropy. However, we know that certainty estimation in machine learning is a more complex concept that deserves a complete description. We refer to the reader to [8] for a complete description of uncertainty estimation.
References
[1] Szegedy C., Ioffe S., Vanhoucke V., Alemi A., Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning. In Proceedings of the AAAI Conference on Artificial Intelligence, 2017.
[2] Xiang Y., Mottaghi R., Savarese S., Beyond PASCAL: A Benchmark for 3D Object Detection in the Wild. In IEEE Winter Conference on Applications of Computer Vision (WACV), 2014.
[3] Yang L., Luo P., Loy C., Tang X., A Large-Scale Car Dataset for Fine-Grained Categorization and Verification, In Computer Vision and Pattern Recognition (CVPR), 2015.
[4] Deng J., Dong W., Socher R., Li L.-J., Li K., Fei-Fei L., ImageNet: A Large-Scale Hierarchical Image Database. In IEEE Computer Vision and Pattern Recognition (CVPR), 2009.
[5] Prokudin S., Gehler P., Nowozin S., Deep Directional Statistics: Pose Estimation with Uncertainty Quantification. In Proceedings of the European Conference on Computer Vision (ECCV), 2018.
[6] Pérez Rey, L. A., Tonnaer, L., Menkovski, V., Holenderski M., Portegies, J.W., “A Metric for Linear Symmetry-Based Disentanglement”. In NeurIPS2020 Workshop of Differential Geometry meets Deep Learning, 2020.
[7] Pérez Rey, L. A. , Menkovski, V., and Portegies, J.W., “Diffusion Variational Autoencoders”. In International Joint Conference on Artificial Intelligence (IJCAI), 2020.
[8] Hüllermeier, E. , Waegeman, W., “Aleatoric and Epistemic Uncertainty in Machine Learning: An Introduction to Concepts and Methods”. In Machine Learning, 2021.
