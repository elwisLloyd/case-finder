# Detecting Stop Signs and Traffic Signals: Deep Learning at Lyft Mapping

Источник: https://eng.lyft.com/detecting-stop-signs-and-traffic-signals-deep-learning-at-lyft-mapping-75bac609c231

Detecting Stop Signs and Traffic Signals: Deep Learning at Lyft Mapping
By Deeksha Goyal, Albert Yuen, Han Kim, and James Murphy
Last fall, I was an intern on Lyft’s mapping team, where I worked on map making.
I designed and productionized a deep-learning based algorithm that predicts where Traffic Control Elements (TCE), such as stop signs and traffic lights, are in the road network using purely anonymized driver telemetry data, such as speed and GPS traces. This work paved the way for us to infer traffic control elements and update our map in real-time.
This project culminated in a paper¹ that I recently presented at KDD’s 8th International Workshop on Urban Computing in 2019 held in Anchorage.
Today, I am back full-time on our growing map-making team and working on similar exciting problems to create a hyper-accurate map from real-time data. In the same topic, my coworker Albert Yuen recently wrote a post² on how we detect map errors using anonymized telemetry data.
Why does Lyft care about Traffic Control Elements?
For Lyft, having high accuracy and coverage of traffic control elements in our internal map is valuable for multiple reasons:
a) More accurate route ETAs: We can add a time penalty to go from one road segment to the next if there is a traffic control element.
b) Dispatch: We can improve driver position prediction, which can help improve market decisions.
c) Autonomous vehicles: With more TCEs, our autonomous driving team, L5, can plan the behavior of vehicles on the road more efficiently and reliably.
Intuition
We noticed that as drivers approach stop signs and traffic signals, they have different speed patterns.
Stop Signs
As the typical driver approaches a stop sign, they slow down and stop their car, verify that the traffic is clear and free from pedestrians crossing, and then resume driving. Figure 1 shows an example of the change in speeds as a driver approaches a stop sign: The driver starts with a non-zero initial speed. As the driver approaches the stop sign, their velocity decreases until it reaches around zero velocity in front of the stop sign. Then, the driver increases their velocity.
Figure 2 shows how this fares in reality on anonymized driver speed readings.
Traffic Signals
We found two main main driver patterns for traffic signals:
- When a driver first sees a red light, they slow down and stop in front of the traffic light. When the green light is activated, the driver accelerates again. This behavior is very similar to the stop sign case, as shown by the red stroke in the diagram on the right of Fig. 3. We may nevertheless expect that the stopping time in front of the traffic signal may be longer than the stop sign case.
- When the driver only sees a green light, the driver usually keeps near constant speed, as shown by the green stroke in the diagram on the right of Fig. 3.
Figure 4 shows how this fares in reality on anonymized driver speed readings.
Neither
This case encompasses many different types, including other road signs and intersections. However, most of the time, the drivers are simply not encountering signs. We therefore expect the velocity of the drivers to remain near-constant, as shown in Figure 5.
Figure 6 shows how this fares in reality on anonymized driver speed readings.
On the Search for TCEs
Inferring traffic control elements with telemetry data has been explored in the past by using ruled-based methods in a set of manually selected candidate locations, or by using more traditional statistical learning approaches, both supervised (random forest, Gaussian Mixture Models, SVM, Naive Bayes) and unsupervised (spectral clustering). However, these methods require extensive feature engineering which may not be straightforward because of noisy or sparse sensor data, e.g., the number of the times the vehicle is stopped and the final stop duration. They also do not necessarily generalize well across multiple different roads, cities, and regions due to differences in speeds, traffic light configurations, and dependence on knowledge about the road network.
Instead, we used a computer vision approach that picks up on basic driver patterns that we can reasonably expect from any stop sign or traffic signal.
Get Deeksha Goyal’s stories in your inbox
Join Medium for free to get updates from this writer.
This approach generalizes well for many other types of map features and across regions and is well equipped for updating Lyft’s map regularly based on real-time location traces.
Methodology
We used Lyft’s proprietary telemetry location data to look for different speed behaviors near each intersection type. By using the City of San Francisco’s open dataset for stop signs and traffic signals as ground truth, we were able to label bounding boxes around each intersection in SF. We collect GPS traces within each of these bounding boxes and then train a convolutional neural network (CNN) to pick up on the different patterns we expect from each traffic control element.
Step One: Create Labeled Bounding Boxes around each intersection in SF
We create bounding boxes over the end of each road segment, the intersection, and a little bit after the junction. In order to do this, we use the road network provided by Open Street Map (OSM). We filter out bounding boxes for junctions that have more than four segments as those cases are rare (around 0.01% in San Francisco). We also filter out bounding boxes for junctions that are too close to each other, so that we do not have any bounding boxes cover more than one junction. Even after removing these cases, we retain a coverage of junctions that is over 90%.
We then label the bounding boxes using the City of San Francisco’s open datasets. They are labeled by checking which traffic control element in the dataset is closest to the junction in the bounding box. If there are none, then we label the bounding box as not having any traffic control elements (neither).
Step Two: Gather driver data for each bounding box
For each bounding box, we collected driver telemetry data inside of them from 40 days in the summer of 2018 for San Francisco. These days are deliberately chosen to be different days of the week to ensure that we are not overfitting for traffic patterns on certain days. We then place each of these data points into the correct bounding boxes by aligning the bearing of the telemetry data and the bearing of the bounding box. This prevents collecting driver data in the opposite direction of traffic flow.
It is likely that some data points would display low GPS accuracy because of tall buildings in San Francisco as well as low smartphone quality. Thus, we made sure to only collect data points with high GPS accuracy. The confidence of the signal comes with the phone’s telemetry readings and is calculated based on standard deviation of the noise of the GPS location.
Step Three: Create kernel density estimators for each bounding box
For each bounding box, we create a diagram over speed and distance from junction by applying a 2D Kernel Density Estimator (KDE) on the data with a Gaussian kernel function.
The bandwidth of the KDE is determined by Silverman’s rule of thumb. At lower speeds, we are likely to see more location data points than at higher speeds because of the sampling rate. This leads to a noticeable amount of driver data points at speed zero at all distances from the junction. These points are not indicative of any driver pattern and add noise. In order to mitigate the effect of this noise, we normalize the diagram with a cube root and min/max normalization. These normalization steps moreover help with surfacing the driver patterns we are searching for.
For the stop sign image, you can see a clear decrease and increase in speed as the driver approaches the intersection, which is at around 40 m in the diagram.
At a traffic signal, you see the same behavior as at the stop sign (a ‘V’ shape), but you also see a straight line which indicates drivers going straight through on a green light.
For the neither histogram, there isn’t much change in speed by the driver.
Step Four: Train the Convolutional Neural Network
We trained on VGG19 pretrained on ImageNet to classify the kernel density estimator images. We initialize with the weights from VGG19 pretrained on the ImageNet dataset and do not freeze any layers. We add an additional fully connected layer to the end of the network that has randomly initialized weights and outputs three scores.
After hyperparameter tuning, our best model for the three classes has a validation accuracy of 91.26% in San Francisco. The validation and training accuracies in Figure 9 tend to stay around the same, suggesting that there is little overfitting.
The learning rate (0.0001) that we landed on after hyperparameter tuning gives a steady decrease in loss (Figure 9).
Test on Palo Alto
In order to evaluate how general the classifier is, we test the classifier in Palo Alto. Palo Alto is a good candidate because it is not as urban as San Francisco, so one might expect a drop in performance of the classifier. Moreover, in our dataset, San Francisco’s traffic control elements comprise around 40% stop signs, 20% traffic signals, and 40% neither. Palo Alto, on the other hand, is comprised of around 15% stop signs, 8% traffic signals, and 77% neither.
We created bounding boxes around each intersection in Palo Alto and then used the afore-mentioned SF trained classifier on this data. These predictions are then compared against manual curation by human experts. With a confidence threshold of 90%, we are able to have a total accuracy of 96.654%.
Conclusion
Overall, we have found that driver telemetry patterns are reliable and generalizable indicators of traffic control element types and that CNNs are effective in deciphering these patterns. We plan on extending this work to include other types of traffic control elements, combining this framework with other strategies for detecting road signage, and using this telemetry-based strategy for detecting other types of road network information.
-
Thank you Albert Yuen, Han Kim, Ferhan Elvanoglu, James Murphy, Karina Goot and many others on mapping for guiding me through this project and supporting me! Also, thank you to Alex Kazakova and her team for their help with data curation. Finally, thank you to the wonderful folks at Flyte. Learn more about Flyte, Lyft’s at-scale workflow infrastructure, and how you can use it here.
I enjoyed working on this project and am excited to continue working on map-making.
Deeksha interned at Lyft in Fall of 2018 and recently joined back full time after getting her bachelors and masters degrees in Computer Science from Stanford University.
As always, Lyft is hiring! If you’re passionate about developing state-of-the-art quantitative models or building the infrastructure that powers them, read more about our Science and Engineering roles and reach out to us.
References:
[1] Traffic Control Elements Inference using Telemetry Data and Convolutional Neural Networks, Deeksha Goyal, Albert Yuen, Han Suk Kim, James Murphy, KDD UrbComp Workshop 2019, 2019. link
[2] How Lyft Creates Hyper-Accurate Maps from Open-Source Maps and Real-Time Data, Albert Yuen. link
