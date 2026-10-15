# Personalized Ranking Model for Lodging

Источник: https://medium.com/expedia-group-tech/personalized-ranking-model-for-lodging-5be43ae975fe

The Egencia®️ (an Expedia Group™️ company) data science team builds AI into its platform in various different ways to create experiences that are personalized for travelers and travel managers.
One of our approaches is to personalize flight and hotel search results for travelers who book on our platform. Recently, we’ve published how the Egencia Smart Mix Flight ranking model has helped personalize flight search results. Below, we discuss Egencia’s personalized Smart Mix Lodging ranking model that enhances user experience and efficiency in hotel search, as well as booking.
Booking a hotel on Egencia: Opportunity to personalize the shopping experience
Egencia’s hotel search UI provides users with the flexibility to set their preferences in a variety of ways, such as in-policy rates, price range, minimum star rating, amenities, etc. Based on these preferences, as well as the location of a search, the appropriate hotels are retrieved, ranked, and displayed. We’re also able to save their individual search, as well as booking preferences over time.
This means based on historical data, we can summarize information such as the amenities and prices of booked hotels and the booking frequency at certain hotels. With this information, alongside the information available from user profiles (for example, stored loyalty cards for certain hotel programs), coworker booking data, and available features at hotels, we have an opportunity to utilize machine learning (ML) models to personalize the search results for most users on Egencia’s platform.
Egencia’s personalized lodging ranking model: Smart Mix for hotels
The objective of the lodging ranking model is to personalize and rank the list of retrieved hotels from a user search. The data we use for this purpose, the ML model and the results are discussed below.
DATA FEATURES: What data goes into search result personalization?
In terms of features of the available data, we use:
(i) historical search and booking preferences (e.g. users’ historical bookings at the hotel and co-workers’ historical bookings at the hotel, price preferences as reflected from past bookings)
(ii) users’ or his/her company’s profile (e.g. brand loyalty, negotiated rates at hotel)
(iii) hotel features (e.g. available rates, amenities, location, star-rating, reviews, etc.)
(iv) context of the search (e.g. distance of the search location from available hotels, type of search — whether the search location was based on an address, airport code, or point of interest)
We’ve typically used historical data from the past 6 months. Data is sourced from Hive stores, AWS (Amazon Web Services) Redshift and AWS S3, Snowflake data lake, and processed on AWS EMR (Elastic MapReduce) Spark clusters. Total data typically consists of tens of millions of records.
Recently, we’ve expanded the amount of historical booking data used to summarize users’ hotel preferences to three years. By doing this, we capture historical booking patterns prior to the pandemic, as well as utilizing the recent changes in booking patterns.
ML MODEL: What is the ML model for personalized ranking?
Our task is to rank a list of hotels based on personalized relevance for the user after their search retrieves an inventory of available hotels.
The hypothesis is, when most preferred hotels are ranked at the top, users will find their choices easily, giving them an improved and efficient booking experience.
Problem formulation
There are multiple ways to formulate the problem and apply ML algorithms to rank hotels retrieved in a search, for example:
1. We can formulate it as a binary classification problem (booked vs. not-booked being the positive and negative classes) and apply ML algorithms for classification to predict a booking score or probability for each hotel retrieved in a search. Then the hotels can be sorted by decreased booking score, ranking the most preferred hotels at the top.
2. We can apply learning to rank algorithms where ranks of the relevant hotels are optimized directly based on information retrieval measures, such as the proportion of bookings at the top ranks or nDCG (normalized discounted cumulative gain).
3. We can apply a collaborative filtering approach using users’ hotel ratings or bookings (implicit ratings), then rank the hotels based on the predicted ratings.
Of these, we describe the application of the classification approach in this article. The application and results of other methods will be described in future articles.
We’ve developed and deployed a model to predict if a hotel will be booked or not (binary classification) based on the historical data features of users, hotels, and current search context. This is a point-wise ranking, where the final ranking is based on decreasing order of the predicted booking score (a higher score indicates a higher probability of booking). We developed and evaluated using tree-based models, such as RandomForest and Gradient Boosting Trees (GBTs), and based on online A/B testing performance (below), we deployed a RandomForest model.
Get Debraj G.’s stories in your inbox
Join Medium for free to get updates from this writer.
For model training, we use AWS EMR Spark clusters.
Model performance: How do we measure performance?
Since repeat booking patterns are frequent in corporate travel, the shopping experience of corporate travelers is in general less exploratory and more focused on finding their preferred hotels with efficiency. Therefore, our objective was to improve customer experience (efficiency). The metrics we measure are related to shopping efficiency include (but not limited to):
1. Proportions of hotels booked within top 1, 3, or 10 ranks: More selected hotels from the top ranks are more convenient for users.
2. Search conversion (Proportion of searches converted to bookings): Fewer searches taken to make a transaction (or higher proportion of searches converting to bookings) is more efficient for users.
3. Time needed to make a booking: Less time needed is more efficient for customers.
We’ve tested the RandomForest model online using A/B testing and compared it to a previously used model without personalization. The model with personalization showed a significant improvement in the above user metrics relative to a gradient boosting tree-based model that was previously developed without personalization using data from Expedia Group’s leisure brands.
Bookings within top 1 displayed rank: Increase of 7.4% (p < 10e-10)
Search conversion (Proportion of searches converted to bookings): Increase of 1.3% (p < 10e-10)
Proportion of bookings made within 5 mins: Increase of 1.3% (p < 10e-10).
Currently, about 90% of users’ selections are made within the top 10 ranked properties, and about 75% of selections are made from top 3 ranked properties (see model monitoring section below).
Model interpretation: Relative importance of features
The importance of the features in the model are discussed below. The five most important features for this model were (in decreasing order):
(i) historical self- booking frequency of traveler at the hotel,
(ii) historical same-company traveler booking frequency (incl. coworkers),
(iii) distance of the hotel from search location,
(iv) if the user’s company had negotiated rates at the hotel, and
(v) historical overall booking frequency of the hotel.
Together, these accounted for ~90% of the total feature importance. The traveler and company-based personalization features — such as self and co-worker historical booking percentage at the same hotel, as well as the loyalty of the user for specific brands, account for about 80% of the feature importance.
Model deployment
After training, we ‘bundle’ the model using the MLeap library using Scala, which can then be put in deployment in JVMs on AWS VMs running Kubernetes. During online prediction, the model utilizes both live and cached features. Cached features are refreshed on a daily basis.
Model monitoring
We have a data pipeline to monitor the performance metrics of the model. An example figure is given below.
Summary
Currently, Egencia enables the personalized lodging ranking model for all Egencia customers. In cases where there are client negotiated or preferred hotels, we rank the remaining hotels retrieved in a search.
Personalized search ranking with users’ search and booking history at Egencia translates to significant improvement of users’ hotel shopping efficiency metrics.
We regularly monitor and respond to model performance issues and customer feedback. Several months ago we received interesting feedback about an unexpected position of a hotel in the search results. Among the root causes, we identified a degradation of the personalization features due to low booking volume in the previous year. We were able to respond quickly and make the necessary changes to historical features. We continue to closely monitor model performance and improve where needed as customers return to business travel.
We’re also in the process of improving our models with additional ML approaches (some of which were discussed above) as well as enhancing user personalization. We’ll discuss models and their performance in future articles.
Author information
Nicholas Maquillan is an ML Engineer; Claudio Aldana-Rosenberg, Achyuta Jha, and Debraj GuhaThakurta are ML Scientists at Egencia.
