# Learning Embeddings for Lodging Travel Concepts

Источник: https://medium.com/expedia-group-tech/learning-embeddings-for-lodging-travel-concepts-99165700cdbd

Learning Embeddings for Lodging Travel Concepts
Introduction
Searching for appropriate accommodation can be time-consuming and frustrating for travelers. Usually, the traveler has specific needs or desires within a certain context, such as “hotels with family-friendly beaches for summer vacation.” While associating the entity “beaches” with certain hotels can be straightforward using geographical information, it is not evident how to associate the concept “family-friendly beaches” with a hotel in a beach destination. To do so, one should try to learn a similarity space that embeds both hotels and concepts as depicted in Figure 1. This can enable many use cases, like the search “Luxury hotels in Geneva” or personalized recommendations.
In this blog, we describe an approach to learning a common embedding space for hotels and travel concepts. Particularly, we leverage traveler reviews to supervise the learning task and thus skip expensive human annotation tasks.
Data
To build such a model, we leverage traveler reviews to capture the value of a certain concept. For example, “free breakfast” could be represented with a Boolean value, but this is not enough as we would like to consider the opinion of the travelers. To do so, we collect one year of reservations with their corresponding reviews. From the reviews, we extract the concepts using an in-house tagging system along with their sentiment that is positive, neutral or negative.
Model
We leverage the two-tower approach to learn a similarity space for hotels and concepts. This approach has the benefit of requiring a simple inference architecture, as the embeddings can be stored in a cache, and fast search methods can be used to retrieve candidate items. The architecture of the model is depicted in Figure 2.
Given a hotel “h” and a concept “c”, the model calculates an embedding for each. Then we calculate a score via a scoring function f(h,c). For example, the inner product or cosine similarity could be used. Additionally, the hotel embeddings could be warm-started from a pre-trained model [3].
Get Ioannis Partalas’s stories in your inbox
Join Medium for free to get updates from this writer.
To train the model, we need to define positive and negative examples which will be used to calculate a ranking loss as follows [1]:
Results
We evaluate the model by running retrieval tasks where given a concept, we retrieve the most similar hotels. In Figure 3, we show the retrieved hotels for the concept “Sea” and within three large markets in Greece. The recommended hotels are near the beach and also have high guest ratings. It is interesting to see that hotels further away from the beach but close to the sea can also be retrieved.
In the next query, we ask for “Wedding hotels.” The top-ranked hotels are from Santorini island in Greece, a destination known for weddings. Usually these hotels are well rated and also the reviews tend to have higher scores in terms of sentiment.
Conclusion
In this blog post, we have showcased how we can learn a common embedding space for hotels and travel concepts leveraging traveler reviews. The important aspect of the approach is that it does not require human-labeled data, which can be expensive to acquire. Additionally, the two-tower approach has the benefit of fast inference as one needs only to store the embeddings and perform the similarity search on request.
References
[1] Jason Weston, Samy Bengio, Nicolas Usunier: Wsabie: Scaling Up To Large Vocabulary Image Annotation, IJCAI 2011.
[2] Jason Weston, Sumit Chorpa and Keith Adams: #TAGSPACE: Semantic Embeddings from Hashtags, EMNLP 2014.
[3] Ioannis Partalas, Anne Morvan, Ali Sadeghian, Shervin Minaee, Xinxin Li, Brooke Cowan, Daisy Zhe Wang, Hotel2vec: Learning Hotel Embeddings from User Click Sessions with Side Information, RecTour Workshop @ Recsys 2021
