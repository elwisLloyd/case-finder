# Compatibility Challenges in Recommendation System

Источник: https://medium.com/manomano-tech/compatibility-challenges-in-recommendation-system-4d233c676d35

Compatibility Challenges in Recommendation System
What is a compatibility issue?
Imagine you’ve finally decided to tackle that long-overdue DIY project: building a new bed frame. After selecting the perfect design and placing your order, your shopping platform suggests a mattress to complete the setup. Trusting the recommendation, you eagerly await your items. But when they arrive, you discover a frustrating problem — the mattress doesn’t fit the frame. What seemed like a seamless suggestion has now become a true nightmare.
This scenario highlights a common yet critical challenge in the world of e-commerce recommendations: compatibility.
In many e-commerce sectors, such as clothing or books, compatibility issues are relatively minor. However, at ManoMano, where DIY and home improvement products often come with specific requirements — such as dimensions, voltage, or fittings — ensuring that recommended items work harmoniously together is crucial.
In this article, we will explore how ManoMano addresses this compatibility challenge. We’ll showcase one of our standout features, the “Often Bought Together” widget, which suggests complementary products based on user behavior and purchase patterns.
Trust user behavior
The first and most intuitive solution is to use our customers’ purchase history. If many users bought two products A and B together, those products are very likely to be compatible.
This straightforward method does have some drawbacks:
- Cold Start Issue: Behavior-based information is not available for new or rare products.
- Random Purchases: Users can make random purchases that do not reflect compatibility (for example, a user may buy an adult bed and a baby mattress at the same time for personal reasons that do not reflect compatibility between the two items.)
As a result, this approach allows us to determine compatibility only for products with many user interactions.
Find patterns with product attributes
The second method involves constructing generalized compatibility rules using product attributes. For pairs of co-purchased products, we analyze their attributes and values to identify frequent patterns. For example, we might expect to find a rule such as “for a category bed and category mattress, attribute length and attribute width must have the same values.” The goal is to extract and generalize these rules across our entire catalog, including new or rare products that may suffer from cold start issues, leveraging the extensive historical data we have available.
Association rules were used to find such frequent patterns. Association rules are a fundamental concept in data mining used to discover interesting relationships between variables in large datasets. The most popular usecase is to analyse market basket to identify products that frequently co-occur in transactions.
The typical form of an association rule is:
If item A is in transaction, then item B is also in the transaction
In order to find rules, the following key metrics are calculated:
- Support: Measures how frequently the itemset appears in the dataset.
2. Confidence: Indicates the likelihood of item B being purchased when item A is purchased.
3. Lift: Measures the strength of the association between item A and B compared to their independent probabilities.
In general, minimum thresholds are set for each metric, and item rules are ranked based on lift or confidence score. We used our customers’ purchase history at category pair level, and applied association rules in order to find these attribute rules.
Here are some rules found by association rules:
On the other hand, we encountered challenges in extracting and matching attributes from product descriptions. While some attributes may refer to the same characteristic, they often lack exact matches due to synonyms, variations in units of measurement, and differences in language. For instance, if an attribute rule is constructed using centimeters (cm), it will not match products whose attributes are in millimeters (mm) or inches. Additionally, extracting product dimensions can be problematic if they are presented as “140*190” instead of “length = 190 cm” and “width = 140 cm.” Attributes must be formatted precisely to ensure compatibility, and variations in language can further complicate this process. Although we tried to extract and reformat attributes, we encounter certain limitations.
These challenges led us to explore additional approaches using a large language model, which is adept at processing raw text.
Apply Deep Learning
Ideally, we want to assess compatibility between two products from textual information and image, similar to how humans do! To achieve this, we fine tuned a Large Language Model to understand all the complexity of our market.
Sentence transformer models are neural network architectures designed to generate fixed-size vector embeddings from sentences. These embeddings capture the semantic meaning of the sentences, allowing for effective comparison and analysis of similarity. Here, we chose a pre-trained model for sentence similarity task and fine-tuned it for our dataset.
Get Moeka S’s stories in your inbox
Join Medium for free to get updates from this writer.
The goal is to train a model that can determine if two products are compatible based on their textual data. If two products are compatible, the distance between their embeddings is reduced; if not, the distance increases.
Now let’s see a step by step how we fine-tuned our model !
#Step 1 Prepare training dataset
To train a Sentence Transformers model, it requires for each pair of sentences a label indicating compatibility. We treated this as a binaly classification:
- Compatible pairs: label=1
- Non-compatible pairs: label=0
Thanks to the experts working at Manomano, some product pairs are manually labeled as “compatible/non-compatible”. However, due to the sheer volume of products in the catalog, this is a long way from processing products across all categories. Therefore we had no choise but to create our own large training dataset.
For compatible pairs (positive examples), we selected products co-purchased at least N times in the past. Although it does not guarantee the compatibility as explained in the first section, a larger value of N increases our confidence in the reliability of the data.
Non-compatible pairs (negative examples) were more challenging to build. At first, we created random product pairs as negative examples, but this was too easy for a model to distinguish and did not work well. To improve this, we decided to first identify pairs of categories that are frequently purchased together, known as complementary categories. We used Association Rules to analyse historical co-ordered categories, similar to the approach used in attribute compatibility rules. This methodology enabled us to identify patterns such as: if category A is purchased, there is a significant likelihood that category B will also be purchased together.
From these complementary categories, we then created random pairs of products. We also included products that were suggested to users through our recommendation system but were never clicked on, ensuring that these products had never been purchased together before. It’s important to note that we consider a lack of co-purchases as an indication of incompatibility, although this assumption is not infallible.
The text data included product names, category names, attributes, and descriptions.
Finally our training dataset look like this:
All the text data is concatenated with a separator:
Product Name [sep] Category Name [sep] Attribute1: Value1 Attribute2: Value2…
#Step 2 Define loss functions
The next step is to choose a suitable loss function for our training data, which consists of pairs of sentences with binary labels.
The loss function optimizes such that (1) the sentences with positive labels are near in the vector space, and (2) the sentences with negative labels are as far as possible. We decided to use ContrastiveLoss, which is mathematically defined as follows:
In our scenario, while the target is binary, we recognize that confidence in compatibility increases with the number of users who have purchased the paired products. Specifically, the penalty for misclassifying a pair should be greater when more users have bought those products. Therefore, we customized the loss function to incorporate this factor.
#Step 3 Fine tune a Sentence Transformer model
We selected the sentence-camembert-base model, pre-trained for sentence similarity tasks in French text because the majority of our products is written in French. Fine tuning a model is straightforward with hugging face library.
#Step 4 Integrate the fine-tuned model to our recommendation system
The fine-tuned model now provides compatibility scores for product pairs. This enhances our recommendation system in two key ways:
- Filter incompatible recommendations
Our model is capable of identifying products that are not compatible, even if they have been co-purchased in the past. It assigns a low score to products deemed incompatible. For instance, if a mattress of the incorrect size is recommended, the model will give it a low score, whereas a correctly sized mattress will receive a high score. We filtered recommendations having a low score to ensure compatibility.
2. Generate recommendations for new/rare products
Our current recommendation system is based on user interaction data, thus we cannot propose recommendations for products without any user history. Thanks to the fine tuned model, we are able to find proper compatible candidates for the new or rare products by exploring complementary categories and products that have a high compatibility score.
For the following example, no products have been purchase together with this bed. But the fine tuned model has been able to find mattresses that match the bedframe size.
Conclusion and next steps
In conclustion, we explored leveraging user behavior, finding patterns in product attributes, and applying advanced deep learning techniques to adress compatibility. Notably, the fine-tuned model has improved the quality of our recommendations, enabling us to better ensure product compatibility.
However, we recognize several key areas for improvement. One major challenge lies in evaluating the effectiveness of our fine-tuned model. While we constructed a validation dataset from our training data and assessed various binary classification metrics, these measures do not fully capture the model’s impact on real-world recommendations. We still lack reliable metrics that can confidently indicate whether we have successfully eliminated incompatible product suggestions.
Additionally, constructing negative examples for our training datasets presents its own complexities. It is crucial not only to create accurate non-compatible product pairs but also to ensure that these pairs are not too obvious.
By addressing these challenges, we aim to further refine our recommendation system, ensuring it delivers reliable and compatible suggestions that enhance customer satisfaction.
