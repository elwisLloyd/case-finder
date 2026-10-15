# How to Monitor a Recommender System

Источник: https://code.tubitv.com/how-to-monitor-a-recommender-system-6d720c922c90

How to Monitor a Recommender System
Authors: Qiang Chen and Bin Chen.
Tubi is an advertiser-based video-on-demand (AVOD) streaming company that lets viewers watch content for free. Tubi’s extensive content library is made up of movies, TV series, live news, and sports.
The recommender system is a crucial part of Tubi because it helps users discover the next, best content to watch. It is important to monitor the recommender system to make sure it works as expected.
We know that monitoring a recommender system as a traditional service is not enough. There are significant differences between a recommender system and traditional software. For instance, a web page can be down or it can be up. On the other hand, a recommender system can be up, but it can also be seriously downgraded at the same time.
It is a challenge to detect the change in recommendation quality. Keep reading and see how Tubi solves this problem.
Where are the Recommender System quality issues?
In order to detect the change in recommendation quality, we have to identify the places where errors could occur that impact the recommendation quality. Once we identify these places, we propose solutions for monitoring them.
To identify the recommender system quality issues, let’s go through what will happen when a user requests the recommender system.
(1). The client sends the user information to the backend for recommendation.
(2). The backend forwards the user information to the recommender server.
(3). The recommender feeds the user information into models and returns results.
(4). The backend post processes the recommendations.
(5). The post-process rules apply to results. For example, removing unavailable content.
(6). The backend returns the recommendations to the client.
(7). Models are trained on data asynchronously with the user requests.
(8). Trained models are synced to recommender servers asynchronously.
Potential issues
(1)(2): User information could be abnormal — Based on the garbage in, garbage out principle, the model is likely to make inaccurate predictions when user information is wrong. For example, when a user’s location is lost, the prediction is based on other user information. This causes the quality of the recommendation to downgrade.
(5)(6): Process outside of the recommender system could be wrong — For instance, the logic that determines that a title is expired may be wrong. This is why it is necessary to monitor the recommendations returned to the client.
(7)(8): The dotted lines on the diagram represent the recommendation system model update process — The process involves data cleaning, generating training data, training a new model, and delivering the trained model to the server. The quality of the model depends on the quality of the training data.
Abnormal training data can appear in the following areas:
- Content feature — The content metadata may be missing.
- Context feature — Information passed to the model can lead to inference problems and training data problems.
- Labels — Improper data processing could significantly reduce positive samples.
- Upstreaming data — This data is key to training data but is outside Machine Learning Team’s scope. For example, third-party content metadata, and homepage impressions. Monitoring and catching unexpected data issues due to upstream changes is crucial to keeping your machine learning system on track.
Proposal for monitoring potential issues
With a comprehensive understanding of potential issues, we propose to monitor three key types of data to monitor the recommender system:
- The data passed to the model which is used for inference prediction.
- The final recommendation results that appear on the user’s screen.
- The model training data that determines the quality of models
Data passed to the model
Data passed to the model is the earliest step in the recommender system workflow. Once an error occurs, the recommendation deteriorates because of the incorrect information.
This kind of issue is hard to identify because it is sent by the client, received by the backend and then passed to the recommender system. In addition, the client and backend teams may not be sensitive to the abnormal changes on recommendation.
Get Qiang Chen’s stories in your inbox
Join Medium for free to get updates from this writer.
It is important to log and monitor the data passed from the client. For example, the percentage of users with language passed into the models.
Final recommendation results
The final recommendation results for users are determined by the recommender models and the post-process step. Our team needs to figure out important properties based on the final recommendation results and monitor them. For example, each content type recommendation percentage. Building monitors based on recommendation results requires a deep understanding of the business.
Model training data
The quality of the training data determines the quality of the model and the quality of the recommendation. We found that key properties do not change much for training data over time, but that large changes in those properties indicate potential issues. For example,
- Changes in the row number of training data.
- Changes in positive label ratio in the training data.
- Missing value ratio of feature fields in the training data.
Monitoring the final training data ensures that its properties meet expectations. The same monitoring concept can also be applied to basic data.
Implementation design and considerations
Monitoring models primarily involve monitoring changes in data distribution (while following the garbage in, garbage out principle).
The initial version was a result of our learning from failures in a post-mortem culture. This has allowed us to accumulate valuable use cases that have contributed to the construction of the entire platform.
Given the focus on data monitoring, there are several aspects to consider based on the characteristics of the data:
• Timeliness — As a monitoring system, timeliness is crucial. We aim to detect anomalies as soon as possible. In a recommendation system, we observed two types of data (user requests and responses) form a real-time data flow. It is essential to conduct real-time monitoring of this data to promptly identify any anomalies in the deployed models or services to enable timely intervention.
• Data characteristics — In real-time monitoring, the support of a time series database is indispensable. This type of data possesses a specific trait where processing time closely aligns with event time. Consequently, we can overlook the disparity between processing time and event time during the processing of data instances like (1), (2), (5), and (6). Conversely, when dealing with another type of data commonly known as batch processing, profiling data at this scale is relatively modest. Batch processing is characterized by updates at the hourly or daily level. Notably, the distinguishing feature lies in the substantial and erratic difference between event time and processing time. When handling this category of data, it is imperative to prioritize event time during processing. Consequently, the two data types necessitate distinct treatment, with a majority of cases falling under this category, including (7) and (8).
• Scalability — Given the evolving nature of business requirements, it’s crucial that monitoring metrics remain independent of each other. This ensures ease of deployment or decommissioning for any metric without impacting the monitoring of others, especially those in real-time scenarios.
Horizontal scaling to accommodate the expansion of business requirements is also essential. For instance, when introducing a new model, a default set of monitoring metrics should concurrently be deployed to guarantee the basic stability of the system that is detectable through the monitoring system.
- Scalability of Data Volume — The system should seamlessly handle an increasing volume of data without compromising performance.
- Scalability of Supported Types — The system should be flexible enough to support the addition of different types, adapting to new business requirements, or the introduction of diverse models.
To achieve these objectives, we implemented the following:
- Defined flexible and explicit proto — We established a proto with a relatively loose and clear structure that employs a three-tiered framework of source, scope, and name to correspond to a metric. This allows users to define generic metrics. Different instances can also be distinguished through shared source and scope attributes, along with unique names to facilitate easy expansion.
- User-defined metrics with multiple approaches — Users have the flexibility to define metrics through Scala, Python APIs, or by utilizing our provided DSL language to configure metric extraction logic. Within the DSL, we employ a simple and effective JSON path representation for defining extraction logic. For example, we can check if there is enough content using .containers[*]{.slug == \\”featured\\” && .contents < 8}.contents
- Configuration file updates instead of job deployment — For real-time data monitoring, dedicated monitoring jobs need to run as stable services for extended periods. Considering resource efficiency, we configure a service for each real-time data source. However, we allow dynamic adjustments to metric extraction rules for a service through configuration file changes that ensure timely and efficient updates without the need for job redeployment. This configuration rule aligns with the DSL mentioned in the second point.
Key takeaways
The key takeaways are as follows:
- Monitoring the quality of the recommender system is a long-term project. Existing monitors may need to be adjusted and new monitors are needed to capture new types of issues.
- A key to make the monitor scalable is to delegate it to domain owners. The domain owner is responsible for managing alerts, setting alert thresholds, and identifying potential issues.
- It is important to focus on alert precision over recall as precision means the percentage of alerts are true issues and recall means the percentage of issues get alerted. This is because when the alert precision is low, there is a tendency for people to ignore them.
- A monthly summary of the monitoring would be helpful to the team to know what’s going on with the recommender system.
Summary
Monitoring a recommender system is challenging because of how difficult it can be to detect changes in recommendation quality. Based on the many real post-mortem issues and a full understanding of the recommender system, Tubi’s Machine Learning Team and Data Team have designed an efficient and scalable data-based monitoring solution that shows how these changes can be detected and monitored.
We’re hiring!
If you’re interested in large-scale, high-impact projects like how we monitor a recommender system, why not join us? Tubi Engineering is hiring across a range of positions in Machine Learning, Machine Learning Infrastructure, Data, and more. You can check out Tubi careers here.
