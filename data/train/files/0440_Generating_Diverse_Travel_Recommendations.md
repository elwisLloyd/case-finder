# Generating Diverse Travel Recommendations

Источник: https://medium.com/expedia-group-tech/generating-diverse-travel-recommendations-76688f49c812

Generating Diverse Travel Recommendations
Background
At Expedia Group™, we aim to provide high-quality recommendations for travel to encourage bookings and inspire exploration. Traditionally, recommendation models have been evaluated by comparing relevance and ranking metrics, i.e., NDCG (Normalized Discounted Cumulative Gain), precision. And while being accurate is important, users prefer having some variety in what we show them. Empirically, we recognize that our travelers might be interested in seeing a wide range of options when exploring and planning for their next getaway. Consider the example of a price-sensitive traveler who’s looking to book a property with the most value, if we recommend a set of properties with a very similar price point, that traveler might become unhappy and unwilling to explore further on the website. Instead, it’s better to have different properties that are more distinguishable to our users.
Travelers can play around with destinations of different types, hotels with different price points, and activities with different themes to engage with everything that Expedia has to offer. Thus, on the EG Recommendations Team, we’ve worked on experimenting with ways to increase the diversity of our recommendation systems. For illustrative purposes, we’re including examples from the Expedia Group™ RecTour Research Dataset¹, introduced in the Recsys 2021 RecTour Workshop². This dataset is based on travelers’ searches and bookings on Brand Expedia Website and has been anonymized to preserve confidentiality. For simplicity, we’ve sampled 50,000 searches from the original dataset. Please note that the dataset is not representative of the true distribution of live searches. A baseline popularity model is used for demo purposes, with test-set properties ranked by their number of clicks in the training period.
Diversity metric definition
The diversity of our recommendation lists is measured by intra-list dissimilarity, defined as the average dissimilarity between all pairs of items in the result set. This metric measures how items within a recommended list are different from each other. This metric can be applied to all recommendation models, as long as an embedding is defined for each item in the recommended list. The higher the dissimilarity, the less the items share in common. The similarity function used is often an inverse Euclidean distance or Cosine Similarity — whichever fits the problem best.
The Python code snippet is shown below for reference:
def intralist_dissimilarity(
embeddings: numpy.typing.NDArray, 
prediction: numpy.typing.NDArray, 
k: int = 10
) -> Tuple[float, float, float, float]:
"""
Total diversity_score at rank k, calculated using both cosine and euclidean distance
Parameters
----------
embeddings : array-like, shape = 2darray (n_samples, embedding_dimension)
Embedding representation for all items
prediction : array-like, shape = [n_samples]
Predicted scores.
k : int
Rank. The top k number of items within a recommended list would be included in diversity score calculation.
Returns
-------
4 floats
total and average diversity metric using euclidean distance, total and average diversity metric using cosine distance
"""
num_rec = embeddings.size
order = np.argsort(prediction)[::-1][: min(num_rec, k)]
embeddings = np.asarray(embeddings)[order]
num_k = min(num_rec, k)
comb = int(num_k * (num_k - 1) / 2)
total_e = cdist(embeddings, embeddings, 'euclid').sum()/2
avg_e = total_e / comb
total_c = cdist(embeddings, embeddings, 'cosine').sum()/2
avg_c = total_c / comb
return total_e, avg_e, total_c, avg_c
The following features are considered when generating item embedding for each property using the sampled Expedia dataset:
- Numerical features:
- review_count: The number of reviews for the property
- num_clicks: Number of clicks for the property
- total_trans: Number of transactions for the property
- Single-value categorical features
- star_rating: The star rating of the property, from 1 to 5
- price_bucket: Price bucket (1–5) based on the percentile of the distribution of impressed prices; lower values of price_bucket correspond to lower prices
- List categorical features
- amenities: Amenities for the property
For illustration, we’ve included an example search below. To calculate the diversity metric for the top 5 properties recommended in this session, we’ve applied transformations to different features highlighted above, and have concatenated different transformed feature types into an embedding column. The intralist_similarity function shared in the screenshot above is then applied to this data frame, outputting the results below. With this diversity calculation, one can compare how diverse item recommendations are between different searches, or form an average across all test searches to compare performance between different models.
+----------------------------------+----------------+---------+-----+---------------------+-------------------------------+---------------------------------------+-------------------------------------------------------------------------------------+
|            search_id             | destination_id | prop_id | scr |   numeric_concat    |         onehot_concat         |           amenities_binary            |                                     embeddings                                      |
+----------------------------------+----------------+---------+-----+---------------------+-------------------------------+---------------------------------------+-------------------------------------------------------------------------------------+
| 005ba385a40aac5c37c46fec64c3c883 |           2053 | 6006894 |   1 | [0.42295,0,0]       | [0,1,0,0,0,0,0,0,1,0,0,0,0,0] | [0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0] | [0.42295,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0]       |
| 005ba385a40aac5c37c46fec64c3c883 |           2053 | 4325931 |   1 | [0.38323,0.17071,0] | [1,0,0,0,0,0,0,0,1,0,0,0,0,0] | [0,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0] | [0.38323,0.17071,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0] |
| 005ba385a40aac5c37c46fec64c3c883 |           2053 | 6924442 |   0 | [0.31533,0,0]       | [0,1,0,0,0,0,0,0,0,1,0,0,0,0] | [0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0] | [0.31533,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0]       |
| 005ba385a40aac5c37c46fec64c3c883 |           2053 |  475674 |   0 | [0.44261,0,0]       | [0,0,0,1,0,0,0,0,0,0,0,0,1,0] | [0,0,1,0,0,1,1,1,0,0,1,0,0,0,1,1,0,0] | [0.44261,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,1,1,0,0]       |
| 005ba385a40aac5c37c46fec64c3c883 |           2053 | 4466305 |   0 | [0.47299,0,0]       | [0,0,0,1,0,0,0,0,0,1,0,0,0,0] | [1,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0] | [0.47299,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0]       |
+----------------------------------+----------------+---------+-----+---------------------+-------------------------------+---------------------------------------+-------------------------------------------------------------------------------------+
Results after applying the intralist_dissimilarity (diversity metric) calculation:
total_diversity_euc: 23.8644
avg_diversity_euc: 2.3864
total_diversity_cos: 3.7109
avg_diversity_cos: 0.3711
In practice, one can include any combination of features that suit the “diversity” use case in mind. When generating item embeddings using explicit features, it is best to transform or scale the values based on feature type first, and then concatenate the values to represent each item. The higher the diversity metric, the more different items within the recommended list. The metric can be used to compare model performance.
Diversification approach
There are a few different positions in the recommendation process that we considered for adding diversity. Specifically, diversification could be placed in the model itself (scoring/training) or in post-processing after we have received a list of the model recommendations.
To enable diversity during model training, a multi-loss function or regularization would need to be configured, where we penalize larger similarity values of the reranked list. However, this would require individual work on every model to introduce diversity features while also being difficult to parameterize or switch off. In addition, model retraining is required to enable the new multi-loss function. In addition, these models would not have much flexibility in what to diversify on. Since everything is learned in training, we cannot decide on specific features or different weights for diversity at the time of the recommendation.
On the other hand, a model output post-processing algorithm can take the output of our recommendation systems and reorder the results. The advantage of adopting this approach is as follows:
- Typically, post-processing algorithms are easy to implement.
- We can adopt the same post-processing algorithm on different model outputs, and configure the features included based on various use-case requirements.
- If the Neighborhood Cosine Distance³ approach is adopted, we can configure the degree of diversity considered when re-ranking the model outputs, which offers more flexibility.
For this blog, we’ll introduce the post-processing algorithms the team experimented with, specifically the Neighborhood Cosine Distance and clustering techniques³.
Features used
We had a few options when deciding what features to diversify on. Nowadays, embeddings trained from neural networks tend to be quite successful in machine-learning tasks, so one option is to diversify in terms of our trained property embeddings. We can also simply diversify on the normalized explicit features of properties like price and amenities. There are various pros and cons to both listed below.
Embeddings
We found previous research on Hotel2Vec⁴, a Word2Vec-style technique that learns embeddings through user clicks, amenities, and the geo features of a hotel. Neural networks can learn better representations of the properties as continuous vectors. This representation makes more sense to machines in quantifying the attributes of a property and can capture more complex relationships between items based on how the network is trained. The enriched embedding comes from the concatenation of the clicks, amenities, and location vectors with fully connected layers in between. This brings similar properties that are viewed together closer in the embedding space. With these embeddings, we have standardized representations for each property in the same vector space.
This standardization is a benefit when it comes to implementing diversity algorithms. You can imagine that when diversifying, there might be different types of values we’d diversify on. For example, the price would just be a numerical value while the type of hotel or amenities available would be categorical or a list. With explicit features, you need to find a way to standardize them in a way that spreads the diversity on each of the features in a satisfactory way. With trained embeddings, we already have a standard vector for each property and do not require the manual step of finding a way to transform the features. Neural networks are also very successful at extracting higher-level interaction features that we otherwise would not be able to extract with less complex methods, and being trained on clicks allows the embeddings to contain information about property co-occurrence. Overall, the pros and cons are:
Pros:
- Standardized representation of property features. Using explicit features, we have different types of attributes (e.g. price, themes, amenities, etc.) that can be different scales or different types.
- Capture more complex property relationships and features. Neural networks can extract higher-order relationships that we otherwise could not with explicit features.
Cons:
- Inability to use changing features. Each time we want to include new features or update existing feature, a new neural network model needs to be trained.
- Explainability. It’s hard to explain how similarity/diversity in the embedding space directly relates to the properties’ features. The continuous embedding values don’t have an intuitive relationship to any of the attributes, so we would have to try and do some sort of investigation into seeing how they relate.
- Bias in the training. Since the neural network for Hotel2Vec is trained on co-occurring pairs of properties, there is inherently a bias in our data. Hotels that are popular have more data to train on, while hotels that don’t get much traffic do not have many examples. This can lead to an issue we see later on where we end up mainly having popular hotels close together, while everything else is far away.
Explicit features
With explicit features, we look directly at property attributes like price, amenities, location, etc. Opposed to embeddings, this is more intuitive in terms of diversification but requires more consideration and work in how we want to consider each individual feature (combined or separate diversity measures). The pros and cons are listed below.
Get Lucy (Jingyu) Zou’s stories in your inbox
Join Medium for free to get updates from this writer.
Pros:
- Explainability: With explicit features, it is very intuitive to explain to users and businesses what our diversification algorithms do. In general, we are trying to either cover a wide range of numerical values like price or a lot of topics for categorical ones like amenities.
- Live Data: With explicit features, we can grab live features from a table and use those as diversity measures. Thus, our metrics for diversity will always be applicable to the current recommendation.
- Flexibility/Control: We can adjust our algorithms, even choosing what attributes to use at the time if we use explicit features. This gives us more flexibility for users who want to use different types of diversity, as well as the ability to choose different features that the Hotel2Vec team didn’t use.
Cons:
- Handling different features: With explicit features, we will have to test and figure out different ways to handle multiple features. Different transformations would be required based on the feature type. An attribute like the price is very different from the amenities covered, so how much weight do we put on the diversity for each of these?
- We cannot capture more complex relationships compared to embeddings, given that we’re no longer training a neural network model.
Clustering³
Clustering is an unsupervised learning method where we group sets of objects together in a way where the objects in the same group are more similar compared to those in other groups. So, we might have a grouping of properties that are all beachside, or others that are more expensive and luxurious. To improve the diversity of the system, you would re-rank the output of your model by giving different recommendations from different clusters, thus covering various sets of topics. In general, there are quite a few different clustering algorithms you can take and whichever one works best really depends on the dataset itself. For this post, we’ll just be using K-means⁵ clustering, which is a centroid-based algorithm for our approach to clustering.
Running the algorithm on a trained Hotel2Vec embedding, we end up witnessing some of the problems that come along with using embeddings for diversity. For various reasons like presentation bias, properties that have more interactions (are more popular) are grouped together in one cluster while the rest are then clustered differently.
On one hand, recommending from different clusters, in this case, would diversify highly on popularity. Properties that are not often interacted with will be forced into recommendations since you are taking some from each group, which could be a benefit in showing customers distinct or new hotels. However, while we do want diverse recommendations, we still want to maintain relevancy. Following the algorithm here drops our ranking metrics like NDCG quite a bit, giving users a poor experience. Using embeddings separates us from the direct features we’re trying to diversify on. Even though we are using features like amenities and location in the training of Hotel2Vec, neural networks are a black box. It’s not intuitive as to what this newly trained embedding represents, whether it places a lot of importance on certain features or less on others, and what the direction or distance of 2 points in this vector space even means. For reasons such as these, embeddings don’t fit well for this use case.
On the other hand, clustering on explicit features like amenities is fairly straightforward. Using the same algorithm, we can cluster properties into groups shown below:
When looking at the distribution of interactions for our clusters here, the numbers are balanced. Since we take distance from the amenities features directly, the main distinction between the properties is the amenities rather than higher-level interaction relationships. In terms of performance, we found that clustering on explicit features lowers the NDCG again but by an acceptable amount and in return, we improve on our intra-list dissimilarity metric.
We can see the diversity metrics we obtain from applying the clustering algorithm to the test dataset below when looking at the top 5 recommendations for our unclustered popularity algorithm compared to the clustered popularity algorithm below.
|  Algorithm  | euclid_diversity | cosine_diversity | avg_review_count_diff | avg_interactions_diff | price_buckets | unique_star_ratings | unique_amenities |
|-------------|------------------|------------------|-----------------------|-----------------------|---------------|---------------------|------------------|
| Unclustered |            26.37 |             4.36 |                   691 |                  0.61 |          3.28 |                 2.3 |             11.2 |
| Clustered   |            27.62 |             4.51 |                  1098 |                  0.85 |          3.37 |                2.47 |            12.61 |We’ve also included a few examples of the top 5 recommendations reranked by the clustering method below:
| destination_id | original_clusters_recommendations | alternate_clusters_recommendations |
|----------------|-----------------------------------|------------------------------------|
|             10 | [0, 0, 3, 3, 2]                   | [0, 3, 0, 3, 2]                    |
|            121 | [0, 0, 0, 1, 0]                   | [0, 1, 0, 3, 0]                    |
|            350 | [0, 1, 0, 0, 0]                   | [0, 1, 2, 1, 3]                    |Neighborhood Cosine Distance approach³
The Neighborhood Cosine Distance approach, also known as MMR⁶, is a post-processing method that considers both item relevance and item dis-similarity into consideration when re-ranking the list. The goal of the MMR algorithm is to reduce redundancy and improve diversity by computing similarity scores between each of the possible candidates and then using both this similarity score as well as relevance to rerank the output. The final score calculated strikes a balance between item relevance and information novelty.
The algorithm for recommending the top K items is as follows:
- Compute similarity scores between all candidates
- Rank the most relevant document first
- For each subsequent recommendation
- Set score as in Figure 1
- Place the item with the highest score next to the list
- Repeat until top K items are supplied
In this method, we have a weight value "w" we refer to as the diversity weight that determines how much of a tradeoff you set between diversity and relevance. The closer w is to 1, the more weight you put on the distance between items, increasing the diversity of the list. We see then that the main parameter to tune is then what to set our diversity weight at. In general, as we increase w, we decrease the ranking metrics like NDCG. One method to set the parameter is to find or estimate the Pareto front and choose a value from the set of Pareto-efficient solutions. Ideally, you would end up with a range of possible weights from 0 to 1, giving our recommender the freedom to choose how much diversity we want to place in our re-ranking.
A bit of fine-tuning is needed before applying the Neighborhood Cosine Distance algorithm. Based on feature distribution, transformations are needed to make sure the similarity scores are calculated in a reasonable fashion. For instance, if we want to include a numerical feature that is highly skewed, then a log transformation and then a standard scaler might be the most appropriate. However, if we want to include categorical features, then a one-hot encoding would be required. Different feature types would also require different distance calculations. We’ve included metrics output for different diversity weights on the example dataset below.
| diversity_weight | avg_total_euclid_in_session | avg_total_cosine_in_session | avg_pairwise_review_count_in_session | avg_pairwise_num_clicks_in_session | avg_pairwise_total_trans_in_session | unique_price_bucket | unique_star_rating | unique_amenities |
|------------------|-----------------------------|-----------------------------|--------------------------------------|------------------------------------|-------------------------------------|---------------------|--------------------|------------------|
|                0 |                     26.3753 |                      4.3646 |                             691.8501 |                             0.6169 |                              0.1726 |              3.2834 |             2.3003 |          11.2086 |
|              0.1 |                     28.7981 |                      4.8085 |                            1240.6767 |                             1.1855 |                              0.3086 |              3.4774 |             2.5906 |          12.7497 |
|              0.3 |                     28.8126 |                      4.8262 |                            1244.8696 |                             1.1953 |                              0.3100 |              3.4520 |             2.5876 |          12.7610 |
|              0.5 |                     29.2089 |                      4.9463 |                            1267.4687 |                             1.1907 |                              0.3120 |              3.4619 |             2.6542 |          12.9343 |
|              0.7 |                     29.6699 |                      5.1382 |                            1343.5378 |                             1.2018 |                              0.3145 |              3.4521 |             2.6702 |          13.1093 |
|              0.9 |                     30.1836 |                      5.2980 |                            1373.3276 |                             1.2532 |                              0.3005 |              3.4635 |             2.6826 |          13.4382 |
|                1 |                     30.2697 |                      5.2827 |                            1397.6258 |                             1.2354 |                              0.3031 |              3.4310 |             2.6695 |          13.5648 |Adding diversity into model output post-processing will most likely result in a decrease in ranking/relevance metrics. Therefore, it is best to test out the resulting offline relevance metrics before setting a fixed diversity weight. Given that we sampled a small amount of data when running example outputs for this blog, the NDCG metric calculated on the test set is extremely low and isn’t realistic. We’ve included an example of what the diversity relevance tradeoff might look like.
Conclusion
In this blog post, we shared how the diversity metric could be an effective metric to monitor, and we discussed the potential approaches to add diversity into model output post-processing. After experimenting with various methods, the team ultimately decided to use the Neighborhood Cosine Distance approach to diversify the recommended items. We hope this blog could be useful for teams working on recommendation/ranking-related projects.
References:
[1] @inproceedings{WoznicaKrasnodebski2021,author = {Woznica, Adam and Krasnodebski, Jan},title = {Expedia Group RecTour Research Dataset},year = {2021},url = {http://ceur-ws.org/Vol-2974/invited1.pdf},abstract = {This document provides details on the dataset that Expedia Group released for the RecTour community. This dataset is based on real traveler lodging searches and bookings on Brand Expedia websites, which has been anonymized for the actual users and properties. The intention is to provide the recommendation system research community, and more specifically travel researchers, an open, rich dataset for their work.},booktitle = {Proceedings of the Workshop on Recommenders in Tourism co-located with the 15th ACM Conference on Recommender Systems (RecSys 2021)},pages = {1–6},location = {Online}}
[2] RecTour: Workshop on Recommenders in Tourism: https://recsys.acm.org/recsys21/rectour/
[3] Diversity Vs Relevance: A Practical Multi-objective Study in Luxury Fashion Recommendations: https://dl.acm.org/doi/pdf/10.1145/3477495.3531866
[4] Hotel2vec: Learning Attribute-Aware Hotel Embeddings with Self-Supervision: https://arxiv.org/pdf/1910.03943.pdf
[5] K-means: A Complete Introduction: https://towardsdatascience.com/k-means-a-complete-introduction-1702af9cd8c
[6] The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries: https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
