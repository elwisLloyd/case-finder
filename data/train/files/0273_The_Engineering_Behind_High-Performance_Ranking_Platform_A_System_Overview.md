# The Engineering Behind High-Performance Ranking Platform: A System Overview

Источник: https://medium.com/booking-com-development/the-engineering-behind-booking-coms-ranking-platform-a-system-overview-2fb222003ca6

An Introduction
Booking.com employs sophisticated ranking to optimize search results for each user. The system uses advanced machine learning algorithms and leverages extensive data, including user behavior, preferences, and past interactions, to tailor hotel listings and travel recommendations.
In this article, we will take a peek into the architecture of the Ranking platform that underpins personalized ranking across various verticals (Accommodations, Flights, etc.)
Where does Ranking Platform fit in the broader ecosystem
The diagram below gives an overview of where the Ranking platform sits within the broader ecosystem. For simplicity, multiple systems have been condensed into a single block or omitted entirely to highlight the role of the Ranking platform.
A typical search flow unfolds as follows: the user initiates a call from their device or browser, and it traverses through various front-end systems, including micro-frontends and gateways, before reaching the search orchestrator. The core search engine then takes charge, orchestrating the search process and generating a list of properties for the search results page and maps. This task involves interfacing with an Availability Search Engine, which tracks the availability of tens of millions of properties across Booking.com over time. Given the extensive nature of this data, the Availability Search Engine is sharded to manage heavy queries efficiently. A coordinator distributes workload across shards and aggregates results within the availability system.
The ranking platform is behind the Availability Search Engine. It uses ML models to score the retrieved properties that match the search criteria.
An Overview of the Ranking platform
Before we examine the ML model-serving aspects of the Ranking platform, let’s briefly examine some of the key components and workflows related to model creation and deployment.
Model Creation & Deployment: Big picture
Data is collected from disparate sources (OLTP tables, Kafka streams, etc.) and stored in a data warehouse. A machine learning scientist then works on this data, exploring, preprocessing, creating features, and selecting suitable algorithms for model training. They train and evaluate machine learning models, optimize hyperparameters, and deploy the model for serving once it performs satisfactorily in offline testing.
The features of such a model can be classified into
- Static features
- Dynamic features
- Slow-changing features
- Realtime features
Static features are computed once using historical data and do not change during model training or inference. Still, they need to be re-computed regularly (every day, week, or month) to maintain data freshness. Some examples are accommodation location, amenities, room types, etc.
On the contrary, dynamic features are calculated as quickly as new data becomes available. Some examples are current room prices and room availability.
The feature engineering section in the diagram above illustrates this difference. Batch features are pre-computed and stored in a Feature store, with a scheduled workflow recomputing them regularly for slow-changing features. In contrast, real-time features are computed based on a stream and sent to a feature store.
Any application that wishes to use ML capabilities utilizes the ML platform to invoke the deployed models.
An expanded view of the Ranking ecosystem
In the case of Accommodations, ranking millions of properties for a vast number of users presents a significant technical challenge that demands sophisticated algorithms and substantial computational power. The system must efficiently process numerous variables, such as user preferences, past behavior, property attributes, and real-time data like pricing and availability, to deliver personalized recommendations in milliseconds, ensuring relevance and accuracy. This complexity highlights the necessity for a robust serving infrastructure, as illustrated in the diagram below, which is an expanded version of the broader ecosystem previously discussed.
As shown above, the Availability Search Engine interacts with the Ranking platform twice: first, from the worker shards to score all fetched properties, and later, from the coordinator after it has merged results from each worker. This second call enables for any final re-ordering of the results.
The Ranking platform has dedicated services for each vertical ranking or use case (Accommodations Ranking, Flights Ranking, Accommodations Recommendations, etc.). For simplicity, all such services except the Accommodations Ranking Service are marked as hidden in the diagram above. Also, as indicated in the image, the Ranking Platform extensively uses continuous experimentation (Interleaving and A/B testing) to optimize search results.
Get Jz’s stories in your inbox
Join Medium for free to get updates from this writer.
Model serving or inference is offloaded to the ML platform, which tracks models, features, and model performance. Due to the scale of Ranking, there is a dedicated cluster within the ML platform that serves all Ranking ML models, ensuring proper resource isolation and reliable performance.
Accommodations Ranking Service Setup
In the section below, we will look into the setup of the Ranking service and some of its key components.
As shown above, the Accommodation Ranking service is deployed across three different Kubernetes clusters. Each cluster contains hundreds of pods to handle search traffic. The diagram on the right illustrates the key components within a single pod. Several infrastructure containers exist alongside the main Java service, which receives requests via Nginx. The Java service retrieves features from a distributed cache before invoking the ML platform. This distributed cache is essential due to latency requirements, which will be discussed later.
Delving into the Java service, you will notice the following components, which are mostly self-explanatory:
- Dropwizard Resources: These are the API endpoints.
- Feature Collector: This component collects features from the incoming search context and also retrieves static features from the distributed cache.
- Experiment Tracker: It tracks all running experiments and the corresponding models associated with the experiment variants. It also ensures that the results are properly interleaved from various variants.
- Model Executor: It handles chunking the request into manageable sizes, invoking the ML platform, and aggregating the scores from parallel calls.
Technical challenges
This section outlines some technical challenges in operating the ranking system at scale.
Being in the Critical Path
Since the ranking system is in the critical path, it must serve results under a fraction of a second at the 99.9th percentile (p999). This necessitates optimizing the operation of heavy models to meet these stringent performance requirements.
Fan-out Problem
Because the ranking system operates behind the workers/shards of the Availability Search Engine, the number of API calls to the system is multiplied by the number of workers.
For example, if the search orchestrator receives K requests per second and if the Availability Search Engine has N workers, the Ranking service will have to handle N * K requests per second.
Wildly Varying Payload Sizes
The number of properties requested to be ranked can vary greatly, ranging from a few tens to several thousands, depending on the density of properties in a particular area and the search area’s size. To manage this, the Ranking service breaks down the payload into manageable chunks before requesting inference from the ML platform. While this ensures consistent model inference latency, it introduces other complexities, such as the need to manage parallel calls effectively without causing memory leaks. Additionally, it exacerbates garbage collection issues and increases the load on the ML platform.
How these challenges are addressed
Fallback to static scores
If the service fails to produce scores within the specified timeframe due to any reason, we resort to static scores for properties. These scores are pre-calculated, stored within the Availability Search Engine, and periodically updated. They serve as a fallback option, enabling the system to offer rankings that, while less personalized, remain relevant to the user during system failures.
Multi-stage ranking
This approach involves breaking ranking into multiple phases or levels, each with its own criteria or parameters, to achieve a more refined and accurate final ranking. This enables running models of varying complexity, personalization and performance at different stages.
Performance optimization
We have extensive monitoring in place to gauge the performance of various components and continually refine them. Additionally, we maintain mirrored setups in production, which can handle shadow traffic to execute any benchmarks exclusive to the production environment.
Model Inference Optimization
Inside the ML platform, continuous efforts are made to optimize model inference to speed up the running of machine learning models. This process typically focuses on reducing latency, memory usage, and computational resources required for inference without compromising accuracy. Techniques for optimization include model quantization, pruning, hardware acceleration, and leveraging specialized inference frameworks.
Conclusion
In conclusion, the Ranking platform plays a pivotal role within the broader ecosystem of Booking.com’s search architecture. It employs sophisticated machine learning models and ranking algorithms to ensure that search results are tailored to individual user preferences. As technology advances and user expectations evolve, the Ranking platform remains at the forefront of innovation, committed to delivering personalized and relevant search results for Booking.com users worldwide.
