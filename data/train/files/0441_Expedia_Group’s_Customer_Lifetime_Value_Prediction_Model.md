# Expedia Group’s Customer Lifetime Value Prediction Model

Источник: https://medium.com/expedia-group-tech/expedia-groups-customer-lifetime-value-prediction-model-7927cdd44342

Expedia Group’s Customer Lifetime Value Prediction Model
Authors: Anantharaman Janakiraman, Amresh Jha, Tatiana Maravina, Ali Ganji
Business context of CLV
Customer Lifetime Value (CLV) represents the customer’s future cash flows over a long-term horizon, such as one year and beyond. Having the ability to estimate the future value of each customer enables businesses to make better decisions about customer acquisition, retention, incentives, marketing communications, long-term investments, and growth.
In this blog, we describe development, implementation and deployment of the CLV prediction models on the Unified Machine Learning Platform at Expedia Group™ (EG). The models are re-trained monthly and future value predictions for hundreds of millions of customers are updated daily and are consumed by business units and teams within EG.
Model development
Why machine learning for CLV?
Many different approaches exist to calculate CLV, including Cohort Analysis, RFM (Recency, Frequency, Monetary Value) framework, and statistical Buy-Till-You-Die models. However, these approaches suffer from at least one of the following limitations:
- Calculate CLV only for predefined segments of customers, and as a result, the calculations should be redone to calculate CLV for any new segments.
- They are based solely on the purchase history and, therefore, fail to account for non-monetary inputs that drive CLV, such as customer engagement and satisfaction.
- Require multiple purchases for each customer as a result, they cannot be used to get accurate CLV predictions for new customers.
To address the above limitations, the classical supervised machine learning approach was taken for the CLV modeling. The initial CLV system uses gradient-boosted trees models to predict the future value of an individual customer as a complex function of many input features representing customer’s past purchase behavior as well as engagement.
Data
The CLV model is the EG-wide model that utilizes data from multiple brands (Expedia, Hotels.com, Vrbo, Orbitz, Travelocity, Ebookers, Wotif, CheapTickets) and line of businesses (Stays, Flights, Packages, Cars, Cruises). More than 200 input features were engineered and are divided into two main categories:
- Bookings
- Engagement
Bookings features can be further categorized into two distinct subgroups. The first subcategory encompasses detailed insights regarding the customer’s most recent purchase, including information like the country of sale, brand, line of business, booking platform (e.g., desktop website, app, etc.), booking value, domestic or international booking, days elapsed since the last booking, and the booking window (the number of days between the booking date and the travel start date), among others.
On the other hand, the second subcategory comprises historical data regarding past bookings, aggregated at the customer level across various time intervals, such as the last 3 months, the last 12 months, and so forth. Examples of features within this subcategory encompass the booking count, total booking value, the proportion of bookings for each EG brand, the number of days since the first booking, the average time gap between bookings, the average booking window, and more.
Engagement features represent the customer’s interactions with the EG brands outside of bookings. The initial CLV model includes features capturing engagement with the marketing emails (for example, number of clicks in the last 3 months) and loyalty-program tiers. More features will be added in the subsequent iterations of the model — more on this in the Future Work section.
It helps to introduce the concept of a cutoff date when describing a CLV data pipeline. The purchases and engagement before the cutoff date are used to calculate input features while the customer’s cash flows after the cut-off date are used to calculate the target values for training. To train a 12-month horizon prediction model, the cutoff date is set to 12 months ago. To score, or to predict a future 12-month value for an individual customer, the cutoff date is set to today.
Modeling approach
CLV model
For initial implementation, the CatBoost was chosen as the machine learning model due to the following advantages:
- It handles high-cardinality categorical features
- It handles missing values for numerical features
- It is fast to train
- It can effectively capture complex non-linear relationships and interactions
Various customer types are individually modeled. Initially, customers are categorized into five geographical regions, and within each region, they are further grouped based on metrics like booking recency and frequency, resulting in a total of 30 segments. A dedicated CatBoost model is trained for each of these segments. This approach allows for:
- Using different sets of features for each recency/frequency segment to better capture input-output relationships within each segment
- Better handling of the differences between countries, both in the distribution of the target variable as well as in the input-output relationships
- Reducing skewness in the distribution of the target values
To further limit the impact of outliers on the training process, the target values are clipped at the 99.9-th percentile within each segment.
In this post, all 30 models are still referred to in a singular form as the CLV model.
CLV multipliers
The core CLV model predicts gross future cash flows of an individual customer. Granular multipliers have been additionally developed to scale gross CLV predictions to the net CLV to account for potential future cancellations.
Model evaluation
The CLV model evaluations are focused on the following two questions:
- How well can the model differentiate high-CLV customers from the rest?
- Lorenz curve and Gini coefficient
- How well do predictions match actuals?
- Bias and RMSE
- Calibration Plots
The customers are randomly split into train (90%) and test (10%) sets. As the names suggest, the customers in the train set are used to train the models, while the remaining customers in the test set are used for evaluations. The above performance metrics are computed overall and by customer segments at the various levels of granularity. Customer segments for evaluations are dictated by the business applications and do not have to match the 30 segments used for modeling.
Evaluation examples below are based on test set predictions by the recent production version of the CLV model. The values on the axes are hidden due to confidentiality.
The calibration plot on Figure 1 suggests that the CLV model is well calibrated as all points are close to the 45-degree line. To draw this plot, customers are sorted in the ascending order of their predicted CLV and divided into 10 equally sized groups (deciles). Then, for each group the average actuals (y-axis) are plotted vs average predictions (x-axis).
Get Anantharaman Janakiraman’s stories in your inbox
Join Medium for free to get updates from this writer.
The Lorenz curves on Figure-2 suggest that the CLV model (red curve) can more effectively sort and differentiate the high-CLV from the low-CLV customers than a simple Historical CLV baseline (blue curve). To draw a Lorenz curve for a model, the customers are sorted in the descending order of their predicted CLV and the cumulative percentage of the actual CLV (y-axis) is plotted vs cumulative percentage of the customers (x-axis). The lower bound is formed by the 45-degree line that represents a random sorting (black line). The upper bound is formed by the perfect ranking that is based on the actual CLV (green line). The closer the model curve to the perfect ranking curve the better the model is at differentiating customers. Numerically, this can be measured by the Gini coefficient, which equals (2x) the area between the model curve and the 45-degree line curve.
The curves on Figure-3 suggest that the CLV model is unbiased with respect to days since last booking. To draw this plot, customers are sorted in ascending order of their days since last booking and divided into 10 equally sized groups (deciles). For each group, the average CLV predictions (orange curve) as well as the average Actual CLV values (blue curve) are plotted vs average days since last booking (x-axis). This plot illustrates decay in the CLV as time from the last booking increases (likely due to increased churn probability) and that CLV predictions made by the model effectively pick up this trend.
Challenges
The massive size of the bookings data and the complex processing involved in generating customer-level input features meant that, when prototyping the CLV models, extra care and thought were needed to make pipelines run in a reasonable amount of time and without (memory) failures. For example, the following steps resulted in 10x speed ups:
- Dropping expensive features with no significant impact on the model.
- Optimizing calculation logic for certain features (for example, computing average days between bookings from the min and max booking dates and bookings count instead of using expensive sorts to calculate actual times between bookings).
- Tuning Databricks clusters (as model development was done on the Databricks Notebooks).
The irregular travel behavior during Covid-19 pandemic certainly affects accuracy of the CLV predictions and restricts meaningful out-of-time model evaluations (aka backtesting).
Machine learning operations
EG unified machine learning platform
For a company operating at EG’s scale, it is essential to establish a machine learning platform that facilitates streamlined and rapid deployment of machine learning models consistently across both test and production environments. The unified machine learning platform offers crucial capabilities to train, deploy, manage and govern models, monitor their health and performance, store and manage features — all with an appropriate level of abstraction so users can seamlessly integrate their solution without getting bogged down by the intricacies of the underlying setup and configuration.
The following section provides a visual representation (Fig-4) of the implementation architecture for the Customer Lifetime Value (CLV) prediction models on EG’s Unified ML Platform and subsequent sections describe the MLOps workflow which is symmetrical between test and production environments.
High-Level Implementation Architecture
Model experimentation and development
Databricks Notebooks are used by ML practitioners in EG for exploration, data analysis and development. The integration test and prod environments are symmetrical environments where the machine learning workflows can be deployed through preconfigured CI/CD workflows.
The development environment has read-only access to the Production data sources to facilitate model development using actual production data; however updating or writing to the Production environment is not possible.
Code
At EG, GitHub is used for storing code and version control. The Machine Learning Scientist and/or Engineer creates new or updates existing pipelines in the development branch of the Git project. The changes are merged to the production branch after the integration test is complete and when the model pipeline is ready for deployment in the production environment. The platform provides a standard backstage template along with the deployment pipelines to integrate with other EG platform-compliant software components.
Data sources and pipelines
The CLV model is an EG-wide model that requires input data from numerous data sources across brands and lines of businesses and aligns data across brands. The data lakes are built on AWS using S3 as the storage platform and Apache Hive is used on top of S3 to process structured data in a distributed environment. The Hive federation across data lakes is made possible through Waggle Dance. The data pipeline tasks required distributed data processing capabilities and were processed using Spark on Kubernetes.
EG compute platform for training and scoring
The model training and scoring pipelines were executed on EG’s fully managed compute platform which is a common container runtime and service mesh platform based on Kubernetes. The individual steps/tasks in the training and scoring pipeline were containerized to support execution on the K8s-based compute platform. The EG-managed compute platform provides ML Scientists and Engineers with a single-managed platform to run all their workloads. Out of the box, the platform provides operational capabilities for logs, metrics, tracing, observability, and security so ML Scientists/Engineers can focus on the business problem by deploying the solution with minimum set of integration points. Scheduling of jobs on the EG-supported compute platforms is made possible through a customized EG-developed service for different job types.
Model management
For Model management, the EG Machine Learning Platform provides a Model Repository Service that is designed to be a single source of truth for models developed in EG. The service provides the ability for ML Scientists and Engineers to store, register and discover and reuse existing models through a programmatic API.
Workflow orchestration
Keeping the models up to date requires robust pipelines for training and deployment/model persistence. Airflow is the primary choice for workflow orchestration on EG’s Machine Learning Platform specifically for batch- inferencing use cases like CLV. Airflow supports running containerized application pipelines that can easily integrate with other EG services seamlessly.
CI/CD
The ML platform template-generated codebase includes predefined CI/CD workflows for automating the build and deployment pipeline. The following are supported tools on EG’s ML platform for CI/CD in both test and prod environments and their role in CLV implementation.
- GitHub Actions: Build Python artifact, publish wheel file, perform Docker build and push to Artifactory.
- Spinnaker: Spinnaker pipeline syncs dags to Airflow.
- Artifactory: Artifact storage and management for test/production environments.
Infra monitoring
There are alert mechanisms in place for the CLV training and scoring jobs that send job success and failure notifications over Slack. The platform provides capabilities to monitor the health of the cluster, workloads and services as well as job execution status; and investigate the logs for any issues.
Datadog is an enterprise observability tool that is integrated with the platform and helps with monitoring performance and infrastructure metrics. There is integration with Splunk as well for log analysis.
Future work
The natural next step after releasing the first model version is to iterate to improve predictions accuracy. Several new features are already in the process of being added to the model. These features measure customer satisfaction and customer engagement (such as app install and app/website visits) and are expected to lead to a significant gain in accuracy for the new and churned customers where recent bookings signal is limited or unavailable. Other ML avenues to explore include the following: more hyper-parameter tuning, target-variable transformation or changing loss function to account for the skewed heavy-tailed CLV distribution, two-stage predictions (the churn probability and the value if not churned), and even revisiting modeling design and switching to a deep neural network.
An equally important task to improving model accuracy is conducting interpretability and explainability analysis to understand what drives the CLV predictions.
Also, in the next blog post we will discuss integration of the scoring pipeline with the EG model monitoring tool that helps monitor inputs to the model, drift, and model behavior to gather insights about different performance metrics.
Author information
Anantha Janakiraman — Principal MLE; Amresh Jha — Senior MLE; Ali Ganji — ML Scientist; Tatiana Maravina — Senior ML Scientist
References
Yandex, CatBoost documentation
A. Vanderveld, A. Pandey, A. Han, R. Parekh (2016), An Engagement-Based Customer Lifetime Value System for E-commerce
X. Wang, T.Liu, J.Miao, A Deep Probabilistic Model for Customer Lifetime Value Prediction
C. Molnar, Interpretable Machine Learning: A Guide for Making Black Box Models Explainable
