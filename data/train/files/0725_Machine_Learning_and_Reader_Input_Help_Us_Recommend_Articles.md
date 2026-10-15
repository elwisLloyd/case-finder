# Machine Learning and Reader Input Help Us Recommend Articles

Источник: https://open.nytimes.com/we-recommend-articles-with-a-little-help-from-our-friends-machine-learning-and-reader-input-e17e85d6cf04

Machine Learning and Reader Input Help Us Recommend Articles
By Joyce Xu
If you create an account with The New York Times, you are presented with a list of popular interests you can choose to follow. It’s a simple idea: tell us what you’re interested in and we will recommend stories in email newsletters and in certain sections of our apps and website.
From a technical standpoint, executing on that idea is less straightforward. If you choose to follow interests like innovation, education or pop culture, we need to know whether a given story fits one of those interests.
In the past, we determined whether an article belonged under an interest by querying tags attached to the story by its editors.
Our taxonomy includes thousands of tags, ranging from broad to hyper-specific, that are arranged hierarchically (the “Food” parent tag has “Seafood,” as well as “South Beach Wine and Food Festival” as children). Some tags are used often, while others are used only once or twice. Some articles are labeled with many tags, while others just have a few.
While the tags represent valuable semantic data about the subjects in a story, the queries to manage them have run into issues:
- Interests might not correspond to the tags for articles. In such cases, the query must be approximate and must string together many related tags, with an ever-growing list of items to include or exclude. For example, there is no single tag for the interest “Parents & Families,” but instead many component tags. At the time of this writing, the query for “Parents & Families” filters over a hundred different tags.
- Query writing requires knowledge about how the tags are applied, and how they have been used over time. The guidelines for tagging Times articles date back to 1851 and require that articles are tagged as specifically as possible. For example, to query all movie content, one would need to know that from 1906–2013 articles about movies were tagged “Motion Pictures”; we now use “Movies.”
- Tags represent a literal topic, while interests often represent a nuanced interpretation of that topic based on context. For example, “Children” is one of the component tags that feeds the “Parents & Families” interest. Yet, many stories that have children as their subject might get the tag, such as this news story about children who fled the conflict in the Tigray region of Ethiopia. While that story does focus on children, it is not a good fit for an interest channel about parenting.
Algorithmic Recommendations — the team I interned with this past semester — was convinced there was a better way. We thought that if we could automatically detect whether an article fits in an interest by programmatically reading article text, we could move away from these cumbersome queries.
How it started: discovering hidden topics
For years, the Algorithmic Recommendations team has been applying a variety of natural language processing models to rank and recommend relevant content.
One of our longest-standing recommender algorithms is based on Latent Dirichlet Allocation, or LDA, which models each article as a mixture of underlying “topics.” To decide whether to recommend an article to a user, we compare the distribution of topics across the user’s reading history to the distribution of topics in the article. We call the distributions “topic vectors.” The closer the user’s and the article’s topic vectors are, the more likely we are to recommend the article.
Unfortunately, we do not directly control which topics the LDA algorithm learns, only the number of topics. In LDA, topics are learned based on the co-occurrence of words across the documents. We have no way of guaranteeing that one of these topics corresponds to one of our established interests — or even that these topics are human-interpretable at all.
In order to develop a representation of the interests that users sign up to follow, we needed a new model that associates articles with specific topics of our choosing.
How it’s going: classifying explicit interests
We tackled this problem by building a machine-learning model that predicts interests based on the text of an article. This approach is known as “multi-label classification” because each data point (in our case, an article) is classified into zero or more labels (or interest groups).
To create a training dataset of articles paired with interest labels, we used the existing hand-crafted queries, even though we knew they were imperfect and often miss articles that belong to the dataset.
In the table above, the article about cuff links could very reasonably be recommended to a user who follows “Fashion & Style,” but due to imperfect queries, the article is missing the correct label. Similarly, the article about buying jewelry on Instagram is labelled only “Business & Technology” because it is missing the relevant tags to be labelled “Fashion & Style.”
Get The NYT Open Team’s stories in your inbox
Join Medium for free to get updates from this writer.
Noisy labels can still be useful, as long as the model does not memorize and reproduce occasional inaccuracies in the training data.
To minimize the risk of inaccurate labels unduly influencing our model, we preferred small, simple models over large, complex ones, and we averaged predictions from multiple different models. We used an ensemble of logistic regression models: each model independently leverages its previously predicted labels to help predict the next label. This approach is known as an ensemble of classifier chains.
Since our classifier models were relatively simple, we made sure to extract rich and expressive feature representations of articles for the classifiers to use. After many rounds of testing, we landed on a final representation with three components:
- An LDA topic vector, as discussed above.
- A vector based on keywords: words that are unusually common in the article.
- A Universal Sentence Encoder embedding.
The Universal Sentence Encoder, or USE, is a neural network that transforms input text into a vector representation: texts that are close in meaning produce vectors that are close in distance.
[If this type of project sounds interesting to you, come work with us.]
To encourage the model to encode semantic knowledge, the original researchers at Google trained it on tasks such as predicting Q&A responses or inferring logical implications. It is one of the few models that is designed to handle longer-than-sentence-length inputs, making it handy for encoding our articles.
While the first USE model was trained on datasets pulled from Wikipedia and online discussion forums, we retrained our instance of the model on Times articles. Because The Times has been publishing journalism for nearly 170 years, we had plenty of content to fuel our dataset.
Once we obtained these embeddings and combined them with the LDA and keyword vectors, we applied the classification model, which produced a probability score for each interest. We were able to establish a cut-off probability for each interest, and compare them to the query-based labels for evaluation.
We win some, we misclassify some
As we suspected, the machine-learning model casts a wider net for each interest than the hand-crafted queries, and it returns more relevant articles.
When we took a deeper look at a few of the incorrect labels, we could often understand why the model assigned the label, but saw that correcting the mistake requires human judgement. It takes knowledge of history and society, as well as the ability to recognize context to intuit that some articles are better suited for some interest categories than others.
Building human-in-the-loop workflows
We came to realize that even though our model outperforms the existing query-based system in many ways, it would be irresponsible to let it curate interests without human oversight.
Readers trust The Times to curate content that is relevant to them, and we take this trust seriously. This algorithm, like many other AI-based decision-making systems, should not make the final call without human oversight.
This interest classifier is already in use as one of a number of inputs our algorithms use to calculate article recommendations.
Looking forward, we intend to set up a collaborative editor-in-the-loop workflow with the newsroom and incorporate this algorithm further into our personalized products.
With more precise recommendation algorithms and editorial oversight, we can offer readers better reading experiences across the wide range of content that The Times produces every day.
Anne Bauer, director of data science at The New York Times, contributed writing.
