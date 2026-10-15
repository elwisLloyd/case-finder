# Serving Large Language Models to improve Search Relevance at leboncoin

Источник: https://medium.com/leboncoin-tech-blog/serving-large-language-models-to-improve-search-relevance-at-leboncoin-2a364e5b6f76

From Matyas Amrouche (Data Scientist @leboncoin)
leboncoin is the first French second hand marketplace. With almost 30 millions unique monthly active users and more than 60 millions different classified ads in our catalogue — each of them described by our users with their own words — it is a complex and technical challenge to deal with this high volatility and display relevant ads regarding our users’ queries.
As we all know, the search engine is a critical point for an e-commerce marketplace. Bad search results lead to frustration and make our users leave, while good search results bring more contacts for our buyers and sellers and an increased trust in our product. That’s why, in the Search team, we decided to improve search relevance with an ads Re-Ranker whose goal is to sort ads in the optimal order regarding a user’s query.
In this post, we describe this first iteration towards an improved search relevance. By the end of the post you will know how we successfully deployed in production, facing highly restrictive conditions specific to the search engine industry, large neural networks to facilitate users’ contact and improve their search experience on leboncoin.
📊 The Dataset
The first step of every Machine Learning (ML) project is to build a learning dataset to feed our models. In the Search field, it is the world of the Click-Models, or in plain English, how to make good use of our users’ clicks.
This research area deserves a whole article by itself, but it is not our purpose for today and we will remain brief. We used statistical filtering [1] and example weighting [2] approaches to leverage our users’ implicit feedbacks to build a multimodal dataset for a contrastive learning task [5]. In short, we built a dataset that says what is a good ad or a bad ad regarding a query.
Now let’s see the model architecture we implemented to learn that !
🤖 The Model
In the short animation above ☝️ we can see how information flows in our neural network so we can compute the desired probability score that will tell us how likely an ad is to be clicked given a user’s query.
This two-towers architecture model, whose main bricks are the Ad Encoder & Query Encoder is called a bi-encoder [4]. The two encoders, made of a large language model (LLM) [3] and custom layers are jointly trained to produce both an Ad and Query representation (a.k.a embedding or vector). Finally, the learned representations are concatenated and processed by the Scorer which produces the click propensity score between the input ad and query.
Great ! 👍 Now that we have seen the overall model’s architecture let’s see how we make it face our millions of users in real time settings.
🚀 The serving
As we mentioned earlier, a search engine must not only be relevant, it must also be blazing fast. More precisely, being able to answer our users’ queries within low latencies time window (few dozens of milliseconds allowed) while facing high throughput (up to few thousands of requests per second at peak time). And that’s a challenge when serving deep neural networks.
- Ads Embedding
Despite being jointly trained, the Ad Encoder and Query Encoder are used separately at serving. Indeed, having a two-towers model architecture allows us to compute the ads and queries representations at different times.
There is no need to overload the real-time serving with computation that can be made before. So, the first step is to trigger the embed_ad entrypoint of our Re-Ranker model (which only triggers the Ad Encoder brick) and compute a representation of all the ads available in our catalogue.
Once all the ads in our catalogue are embedded in the vectors database (), we are ready for the real-time work, the re-ranking task !
2. Ads Re-Ranking
As its name suggests, the Re-Ranker takes a list of ads and re-sort it. Indeed, a pool of ads is first retrieved and ranked by our ElasticSearch (with a TF-IDF like algorithm and custom functions). Only the top k of the pool of retrieved ads are sent to the Re-Ranker to compute a relevance score. Then, those new Re-Ranker’s scores are combined with the ElasticSearch’s ones and the final sort takes place. The residual ads (which were not sent to the Re-Ranker) are simply appended after the top k that have been re-ranked to produce the final listing displayed to our user.
NB: The terms retriever and ranker (or re-ranker) often appear together in search. Retriever and ranker are complementary to each other, while the retriever focuses on the recall, the ranker purpose is to sort the retrieved items by their relative relevance to a query.
Et voilà ! 👌
Get leboncoin tech’s stories in your inbox
Join Medium for free to get updates from this writer.
This was our first iteration of the Re-Ranker project, which showed great results, improving both our business targets (click & contact rate up to +5%) and user experience KPIs (nDCG and average clicked & contacted positions up to +10%).
We have some very nice improvements in our roadmap to make it even better and we hope we will soon share some new ML success stories.
Stay tuned ! 😉
All images are by the author unless otherwise specified
References
Appendix
A. Information Flow details
- Step 1: Input Ad and Input Query are made of multimodal signals (text, numerical and categorical data).
- Step 2: The text part of the Input Ad and Input Query are sent to the LLM while categorical and numerical data to custom MLP. The data preprocessing is embedded in the model (in both Query and Ad encoders), ensuring the data processing consistency between training and serving.
- Step 3: The pre-trained LLM are fine-tuned in a Siamese manner (shared weights). We take the text vector representation from a [CLS] pooling.
- Step 4: Both in the Ad and Query encoders, the text and tabular data representations are concatenated and mapped into a lower dimension space for storage and compute time gains.
- Step 5: Finally, the Ad and Query representations are concatenated and fed to the Scorer which outputs a probability, representing the ad propension of being clicked regarding the query.
B. Serving details
a) Retrieving & Ranking
- Step 1: At first, the query is sent to ElasticSearch (ES), which first retrieves and ranks the ads using a TF-IDF like algorithm and custom functions.
- Step 2: Then, the top k ads with the highest ES scores (purple border) are mapped to their respective vector in the vectors database.
b) Re-Ranking
- Step 1: The query and the top k ads vectors are sent to the Re-Ranker model’s rank_ads entrypoint (which triggers the Query Encoder and the Scorer model’s bricks).
- Step 2: The Re-Ranker produces a new score for the top k ads (green border).
- Step 3: The old scores (from ES) and new scores are combined. Enabling the re-ranking of the top k ads (pink border).
- Step 4: The re-ranked ads are added in front of the residual ads that were not selected in the top k pool at first (brown border), to produce the final listing order displayed to our users.
