# Channel-Smart Property Search: How Expedia Tailors Rankings for You

Источник: https://medium.com/expedia-group-tech/learning-to-rank-at-expedia-group-how-to-adapt-the-property-search-result-page-based-on-f4ebef78c94b

Expedia Group™ websites are dedicated to providing millions of visitors with the most relevant lodging rankings based on their search query and context. From a Machine Learning Science perspective, we adapt the lodging ranking algorithm to the channel the traveler comes from, such as from Google versus direct.
Destination vs Property searches
To understand the implications of coming from a different channel, let’s consider the two following scenario:
Destination search
Alice is planning a summer vacation. She wants to visit Sicily for two weeks and needs two ‘base camps’ so she can easily travel to every part of the island from Catania and Palermo. She comes to Expedia and performs two destination searches: one for Catania as the destination and one for Palermo to find the two properties that suit her needs.
Property search
Bob is scrolling on his favorite social media site and found a property advertized by a travel influencer that is perfectly romantic to invite his partner for their anniversary. He clicks on the affiliate link to reach Expedia. In the backend, for Expedia this is a property search, as the query here is not based on a specific destination but a specific property.
For the two cases, the listings won’t look the same.
In the first case, Alice is coming ‘organically’ to Expedia for discovery.
She is shown a ranking of properties which is taking into account:
- the relevance or utility of all the properties given the context of her search (destination, check-in/check-out dates, number of adults, children, etc.)
- different ‘business adjustments’ to account for several marketplace considerations (exposure of the property owners, long term traveler satisfaction, etc.). Cf. this article for more information.
Bob is coming from an external ‘channel’ and is redirected to Expedia from this other website. He is not redirected to the property details page of the hotel but instead to another search result page on which the property he looked for is ‘pinned’ on the top.
This is a cold shower for Bob. The property is fully booked for the dates of his anniversary. You might argue he can look for other dates but he really wants to do his romantic trip for the dates of their anniversary. Hence, he needs to find an alternative. He is in luck with Expedia as this is exactly the purpose of this specific property search ranking algorithm: providing a ranking which is a blend between the relevance of the properties (business adjustments are also… adjusted!) and the similarities between the properties with the property on top.
In the sequel, we will describe:
How to model differently the Property Search lodging ranking algorithm
General framework for lodging utility ranking
Let’s first give an overview of the destination search utility ranking algorithm (more details to follow in another blog post!):
A destination search utility ranking algorithm in our jargon focuses on only one task: sorting the properties selected for the given destination based on their utility or relevance for the traveler for the search context (e.g. search parameters). This ranking block arrives after the candidate generator selects a subset of properties to rank and before the final business adjustments are applied.
Overview of lodging utility ranking modeling
Training dataset and set of features
The training dataset is created using converted search logs (searches which led to a booking) with the corresponding displayed properties for which we got as implicit feedback the relevance of the properties towards the given search context in the form of a ‘booking’ or a ‘click’ by historical users. Relevance is defined so that a booking is considered as a stronger signal of property relevance than a click or a simple impression (meaning the property is shown to the traveler but there is no interaction with it).
Get Anne Morvan’s stories in your inbox
Join Medium for free to get updates from this writer.
booking > click > impression
The set of features is of a different nature:
- description of the search context: this includes the search parameters such as destination, check-in/check-out dates, number of rooms, number of adults, number of children but also point of sales of the website (.com, .ca, etc.), device and potentially other personalized features to describe the user profile.
- description of the properties: price, guest review, star rating, amenities, etc.
In particular, the property features contain an embedding which takes inspiration from the Word2vec model, adapted to the lodging domain.
Model architecture
The lodging utility ranking model is a deep neural network built around a well-established algorithm for supervised learning, particularly for learning-to-rank problems. The approach is suited to our very sparse feature set as we have to deal with lots of categorical features. The model has the capability to capture meaningful interactions between all the features by learning embeddings for each of the input feature.
Adaptation to the Property Search lodging ranking algorithm
Having set up the basics of the lodging ranking algorithm for destination searches, we can highlight the subtleties of the lodging ranking algorithm for property searches. If you want to go straight to the summary of common and different elements between lodging ranking algorithm for property vs destination searches, here it is:
We describe now more in details. We currently keep the same model architecture with the same ranking loss. What is tailored to the property search case are:
- the pre-processing of the training data set,
- the choice of features.
Training data pre-processing
For this use case, we focus naturally on converted property searches and not destination searches anymore.
Feature selection
We leverage all the existing features from the destination search lodging ranking algorithm:
- search context features
- property features
Moreover, what we add are elements reflecting similarity between the searched property features and ones of the properties to rank.
We performed a feature ablation study and the whole set of added features have been found to be useful for improving offline model performance. The final version of the model has been successfully AB tested. Moreover, we also tried a fully similarity-based lodging ranking model for hotel searches, so based uniquely on the similarity of the property embeddings. This version was not able to fully account for the also important relevance of the properties themselves towards the search query context, which lets us think there is value in finding a good equilibrium between relevance of the properties and similarity to the searched property.
Conclusion
In this article, we showed how we better serve our travelers by providing a more relevant lodging ranking when we slightly adapt the modelling part of the lodging ranking algorithm to their channel source, particularly when the traveler is reaching Expedia website with the strong intent of booking a specific property (what we call property search vs destination search). This relies on classic search context and property features and features to describe similarity of the properties to rank with the initially searched property.
Learn more about Data & Technology at Expedia Group™️ and stay tuned for the next upcoming blog posts around Lodging ranking! We plan to cover:
- Evolution of the lodging ranking utility model architecture: from a shallow to a deep neural network
- Challenges around one lodging ranking utility model for different brands and sites: how to reduce the number of models to maintain while maintaining performance and brand specificities
- Personalization of lodging ranking utility model: tradeoff considerations between long-term (based on booking history) vs short-term personalization (based on the few past sessions’ click interactions), features comparison between traveler raw data vs embeddings
