# FastDTW in Action: Optimising Manufacturing Operations

Источник: https://medium.com/trusted-data-science-haleon/fastdtw-in-action-optimizing-manufacturing-operations-c07f3cc5023c

FastDTW in Action: Optimising Manufacturing Operations
As a leading consumer healthcare company, Haleon is on a mission to deliver better everyday health with humanity. Haleon’s Data Science Team supports this goal by optimising supply chain operations, as it leads to enhanced efficiency, visibility of processes, as well as quality control. In particular, one of the projects focuses on optimising operations in a toothpaste manufacturing site: products such as Sensodyne or Aquafresh share similar manufacturing processes.
By acknowledging this similarity, the potential for optimisation and greater efficiency has been unlocked: Haleon’s Data Science Team has built a predictive model with FastDTW as its core foundation. The aim of the system is to proactively detect ongoing manufacturing processes, give recommendations to the site operators in real-time to ensure optimal outcome, and provide a tool for site operators to get meaningful insights about the historical processes.
This article will serve as your technical guide, taking you on a comprehensive journey through the algorithm, the intricacies of distance measurements, and explore DTW’s practical real-world application in toothpaste production.
What is (Fast) Dynamic Time Warping?
Dynamic Time Warping is an algorithm originally developed in the 1970s, primarily for speech recognition tasks. Its purpose is to measure the similarity between two temporal sequences, even when they exhibit variations in time or speed. This technique finds widespread use in various domains, including signal processing, time series analysis, and speech recognition, as it can effectively handle situations where one time series may be faster or slower than the other.
In contrast to the DTW algorithm, FastDTW stands out for its enhanced computational efficiency, having a near-linear time complexity as an approximation algorithm. This efficiency is achieved through down-sampling, which reduces the number of points involved in distance calculation, and a constraint on the warping path, limiting the number of cells on each side of the path. However, one drawback emerges when applying FastDTW to manufacturing step detection — it may lead to less precise identification of individual steps. Manufacturing processes have large datasets, with new data being streamed every 30 seconds, therefore FastDTW’s speed is a suitable for the task. If achieving high accuracy is crucial and computational resources pose no constraints, opting for regular DTW emerges as the preferable choice. Furthermore, in scenarios involving short time series, DTW can surpass FastDTW in terms of speed.
In our project, FastDTW enabled us to efficiently align patterns of procedures to manufacture toothpaste in real-time processes and perform manufacturing step detection with precision.
Distance Measures — What are They?
Fast DTW is not a typical algorithm used by data science teams, even more in manufacturing use cases. It is not designed to output a prediction or classification but is instead a signal processing method used to measure similarity, called the DTW distance. It quantifies how similar or dissimilar two time series are based on their temporal patterns. It is a traditional output format for similarity measurement and alignment tasks in time series analysis.
It’s important to distinguish between the concepts of similarity and distance, as these terms are frequently used in the context of FastDTW. Similarity measures how similar or close two time series are to each other, while distance quantifies the dissimilarity between two time series. The smaller the distance, the more similar the two patterns are considered, as they require fewer adjustments for optimal alignment.
There are various methods for measuring distance, including some widely recognised distance metrics like Euclidean distance and Manhattan distance. Euclidean Distance, for instance, represents the length of a straight-line segment that would connect two points in a two- or three-dimensional Euclidean space.
Euclidean distance matches timestamps regardless of how similar/different patterns are, whereas DTW matches patterns based on the similarity, even if the timestamps are not in sync.
The overall methodology to calculate FastDTW distance can be broken down in 3 parts.
It’s important to mention that FastDTW has 3 essential constraints:
- Boundary Condition: This condition ensures that the warping path must start at the beginning and end at the conclusion of the time series, maintaining continuity from start to finish.
- Monotonicity Condition: This constraint upholds the chronological order of data points, preventing the path from moving backward in time, thus preserving the natural time sequence.
- Step Size Condition: This condition restricts path transitions to adjacent points in time, preventing abrupt jumps between non-consecutive points in the series.
Implementation example using synthetically generated series.
Get Evelina Haite’s stories in your inbox
Join Medium for free to get updates from this writer.
First, we need to create 2 data arrays to calculate the distance metric.
import numpy as np
import random
# Set seed for reproducability purposes.
np.random.seed(42)
# Create 2 arrays that generate random numbers between 1 and 3. 
x = np.array([random.randint(1, 3) for _ in range(5)])
y = np.array([random.randint(1, 3) for _ in range(5)])
Then, using the FastDTW function from the FastDTW package, we can generate the DTW distance measure and an optimal warp path (tuples that indicate how to warping path moves as the series progress). The lower the DTW distance is, the more similar series are.
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from matplotlib import gridspec
dtw_distance, warp_path = fastdtw(x.reshape(-1, 1), y.reshape(-1,1), dist=euclidean)
print(f'X Sequence: {x}, Y Sequence: {y}')
print('Similarity Distance between series x and y: ', dtw_distance)
print('Warping path between series x and y: ', warp_path)
# Get the warp path in x and y directions
path_x = [p[0] for p in warp_path]
path_y = [p[1] for p in warp_path]
# Visualise the path of aligning 2 sample series 
# Create a grid of subplots with different widths and heights
fig = plt.figure(figsize=(8, 5))
gs = gridspec.GridSpec(2, 2, width_ratios=[1, 4], height_ratios=[2, 1])
# Plot the Y Series vs Time
ax0 = plt.subplot(gs[0])
ax0.plot(y, np.arange(len(y)), color='black')
ax0.set_title('Sequence Y vs Time')
ax0.set_label('Y Series')
ax0.set_ylabel('Time')
plt.grid()
# Plotting the FastDTW Warping Path
ax1 = plt.subplot(gs[1])
ax1.plot(path_x, path_y, color='#30EA03', linewidth=3)
ax1.set_title('FastDTW Warping Path')
plt.grid()
# Plot X Series VS Time
ax2 = plt.subplot(gs[3])
ax2.plot(np.arange(len(x)), x, color='magenta')
ax2.set_title('Sequence X vs Time')
ax2.set_xlabel('Time')
plt.grid()
# Remove unused subplot
plt.delaxes(plt.subplot(gs[2]))
# Adjust layout to prevent clipping of titles
plt.tight_layout()
# Show the plot
plt.show()
The next section delves into an exploration of how the characteristics of FastDTW can be used for the purpose of step detection.
Application Example in the Manufacturing Context
To identify manufacturing steps in a real-time setting, there are several crucial considerations that must be addressed before any distance calculations can occur. When we talk about manufacturing steps, we’re referring to the distinct actions and procedures involved in creating toothpaste. While these factors may sometimes be overlooked, they are essential for enabling step detection. These key elements include:
- Data Source: Sensor data is continuously streamed from the manufacturing site’s data collector to the Cloud. These sensors gather and transmit data on various features, including pressure and temperature inside the mixer, and the data is collected every 5 seconds. The predictive model is seamlessly integrated into the data streaming system, allowing end users to monitor real-time progress in the manufacturing process through a dashboard. For further insights into the Machine Learning system implemented for this project, please refer to Oleksandr’s post.
- Historical Data Templates: These templates capture expected signal patterns for every manufacturing step. This is a crucial step as it forms the foundation for matching and detecting manufacturing steps. Process templates represent the ideal behaviour of each parameter during manufacturing process, we would use process requirement documentation that describes the settings of features per step. We create a dictionary that store features attributed to each step in a manufacturing process, for example, the pattern, optimal duration (if it is specified), and its distance threshold.
- Distance Threshold: As illustrated in Image 1, the distance threshold is an additional feature we use from FastDTW calculation, to gauge the similarity between the real-time readings’ observed pattern and our predefined pattern (the historical pattern template). The threshold is determined by taking historical readings and determining the typical distance values associated with each step. It is used in the model to flag if the observed pattern is a match with the reference pattern, thus marking a step has occurred. At times, it’s straightforward to identify the start of a step, while in other instances, multiple similar minima are computed throughout the historical examples’ duration. That’s why it’s crucial to establish and thoroughly test a globally defined threshold for each step, before it is passed in as a feature into the model. With a globally defined threshold, we can apply the same threshold across the entire duration of the manufacturing process.
4. Model Logic for Step Detection: To ensure the model accurately identifies manufacturing steps in real-time, we’ve implemented several logical aspects. For instance:
- The model concurrently scans the data while searching for both step N and N+1. This enables the model to persist in detecting steps even if one is missed, preventing it from getting stuck in the search for step N. (There’s a chance that step N may have already occurred and, therefore, wouldn’t be found.)
- The model needs a minimum of X data samples, where X corresponds to the length of the step currently under investigation. This requirement ensures we have ample data for calculating the FastDTW distance and locating the specific step.
5. Data pre-processing: For FastDTW, it’s essential to scale all features involved in step detection so that they share a similar range. For this, data standardisation is used — it ensures that the mean of the values is 0 and standard deviation is 1. This guarantees that no single feature becomes overly dominant, preventing any weighting compared to other features.
Combining these elements to create a step detection system facilitates the optimisation of the toothpaste production process. Such approach can be replicated across diverse products and processes. It provides manufacturing sites and operators with the opportunity to have real-time visibility into the processes, allowing for swift adjustments to uphold quality standards. If a step happens to take longer than anticipated, site operators are promptly notified, enabling them to proceed to the next step efficiently.
Conclusions
In conclusion, Haleon’s Data Science Team leverages FastDTW as a key element in optimising toothpaste manufacturing processes, providing real-time insights and recommendations for enhanced efficiency and quality control. While FastDTW’s computational efficiency proves advantageous in handling large datasets and maintaining responsiveness to ongoing manufacturing processes, it is important to acknowledge its trade-off, particularly in precision, when applied to manufacturing step detection. The accuracy can be increased by increasing the search window, however it will lead to reduced speed. Components such as data engineering, model design and testing as well as machine learning were crucial in creating a robust manufacturing step detection system. FastDTW was used in the model’s creation, where feature pre-processing, step template creation, threshold selection and testing as well as a general model’s logic implementation are the enablers of similarity distance calculation.
References
- W. Choi, J. Cho, S. Lee and Y. Jung, “Fast Constrained Dynamic Time Warping for Similarity Measure of Time Series Data,” in IEEE Access, vol. 8, pp. 222841–222858, 2020, doi: 10.1109/ACCESS.2020.3043839.
- Big O Quadratic Time Complexity | jarednielsen.com
- R. Wu and E. J. Keogh, “FastDTW is approximate and Generally Slower than the Algorithm it Approximates (Extended Abstract),” 2021 IEEE 37th International Conference on Data Engineering (ICDE), Chania, Greece, 2021, pp. 2327–2328, doi: 10.1109/ICDE51399.2021.00249.
- Local & Global Minima Explained with Examples — Analytics Yogi (vitalflux.com)
- Al-Jawad, Ahmed & Reyes Adame, Miguel & Romanovas, Michailas & Hobert, Markus & Maetzler, Walter & Traechtler, Martin & Moeller, Knut & Manoli, Yiannos. (2012). Using multi-dimensional dynamic time warping for TUG test instrumentation with inertial sensors. IEEE International Conference on Multisensor Fusion and Integration for Intelligent Systems. 212–218. 10.1109/MFI.2012.6343011.
