# Categorising Customer Feedback Using Unsupervised Learning

Источник: https://medium.com/expedia-group-tech/categorising-customer-feedback-using-unsupervised-learning-8608c1e62d48

Categorising Customer Feedback Using Unsupervised Learning
Introduction
At Expedia Group™, we strive to improve our travellers’ satisfaction by providing frictionless ways for them to raise their queries, complaints or feedback. We receive thousands of customer messages every day and need an efficient way to send each message to the correct Expedia Group teams. To do this we automatically classify the received feedback, which can then be forwarded to the correct teams. This article describes how we are leveraging Unsupervised learning techniques to perform Multi-Label Classification without requiring a training dataset.
Initial attempts
Multi-label classification using supervised learning models
Employing a pre-trained ML model, which can be fine-tuned for our custom text (feedback) to classify into a custom multi-label taxonomy.
To be able to do this, all the existing machine learning models need thousands of pre-classified/labelled dataset for fine-tuning. As we do not have any pre-classified data for fine-tuning, we would have to put in significant efforts to do manual classification. Hence, this approach becomes tedious and time-consuming.
Multi-label classification using word synonym
The second approach: Rudimentary way of classification of text based on keywords and their respective synonyms.
At first, it appeared to be a good solution to begin with as it does not need any pre-classified data for training, also it seems quicker than first approach.
Now, let us consider this with a few examples of Traveller’s Complaints/Feedback:
Traveller 1. My plane was delayed.
Traveller 2. We flew an hour late.
In the examples given above, both the travellers want to report their respective flights getting delayed. Here, in the first statement, the keyword ‘plane’ is a synonym of the word ‘flight’, so we can easily classify it as a ‘flight issue’ while in the second statement, the keyword ‘flew’ is not a synonym of the word ‘flight’, thereby making it difficult for the algorithm to classify it as a ‘flight issue’.
Understanding and further decoding the issue indicated above:
Let’s take another example here. When we hear the words ‘tea’ and ‘caffeine’, what do we generally associate them with? Probably, we would say that tea is a beverage, which contains a considerable amount of caffeine. The point is, that our minds can easily recognize that these two words are associated with one another. However, when we enter the words ‘tea’, and ‘caffeine’ into the above algorithm, unlike us, it is unable to recognize the association between the two words.
Now, this poses a problem for us because the first approach needs time and effort to manually classify thousands of feedback messages for training ML models while the second approach is not able to provide rich classification results.
Building our own heuristic algorithm
Our team devised a way to overcome the problems mentioned above by writing a heuristic algorithm that leverages pre-trained word-embedding models. These models help in wielding the distance between the keywords from the feedback with each classification bucket, eventually enabling our algorithm to understand the context of the feedback. This helps with the first level of classification, without the need of pre-classified dataset. To further enrich the results, our team built custom classification rules as well (details of its functionality is not under the scope of this article).
To understand the above solution(first level of classification), let us first see how we leveraged a pre-trained ‘word-embedding model’ in order to understand the context of the feedback.
Finding least distant bucket
In the NLP world, the words are represented in the form of vectors. These vectors occupy the embedding space with certain dimensions which can be quite large, depending on the size of the corpus.
Example: 
have = [1, 0, 0, 0, 0, 0, … 0]
a = [0, 1, 0, 0, 0, 0, … 0]
good = [0, 0, 1, 0, 0, 0, … 0]
day = [0, 0, 0, 1, 0, 0, … 0] …
Word2Vec is one of the most popular representations of document vocabulary in the form of word embeddings using a shallow neural network. It is capable of capturing the context of a word in a document, in terms of its semantic and syntactic similarity to other words. It was developed by Tomas Mikolov at Google.
Word2Vec architecture
Word2Vec can make strong assessment about a word’s meaning based on their occurrences in the text. These assessments yield word associations with other words in the corpus. Let’s look at an example with just two dimensions for sake of simplicity. In a real implementation we use more dimensions, we will talk more on that later. In our simple example, words like ‘King’ and ‘Queen’ would be very similar to one another. When conducting algebraic operations on word embeddings you can find a close approximation of word similarities. For example, the two dimensional embedding vector of ‘King’ - the two dimensional embedding vector of ‘Man’ + the two dimensional embedding vector of ‘Woman’ yielded a vector which is very close to the embedding vector of ‘Queen’. 
Note, that the values below were chosen arbitrarily for the example.
King    -    Man    +    Woman    =    Queen
[5,3]   -    [2,1]  +    [3, 2]   =    [6,4]
In our actual solution we used pre-trained word embedding from GloVe, which provides similar functionality to Word2Vec.
GloVe is an unsupervised learning algorithm for obtaining vector representations for words. Training is performed on aggregated global word-word co-occurrence statistics from a corpus, and the resulting representations showcase interesting linear substructures of the word vector space.
GloVe pre-trained word-embeddings can be downloaded from here
If you want to know more about word embeddings check out this guide from Tensorflow.
Get Aman Gupta’s stories in your inbox
Join Medium for free to get updates from this writer.
Unlike the simple two dimensional example above, the GloVe embeddings have high dimensionality which are difficult to visualise. To visualise the word-embedding for this article, we will be using PCA as a common dimensionality reduction technique, to read more about dimensionality reduction technique, which you can read it over here.
Now that we have some basic understanding on word-embeddings, let us do some classification…
Consider we have to classify the feedback into three categories ‘Flight’, ‘Hotel’ and ‘Car’. Let us first see how these category keywords and some related keywords to the above mentioned categories are embedded in the vector space.
Visualising word embedding by GloVe with PCA [3D]
Below we can see some words related to the category ‘Flight’.
In ‘Figure 2’ we can see that the keywords such as ‘flew’, ‘flown’ etc. which have a similar context to the keyword ‘flight’, are placed near to one another in the 3D space.
Now lets look at all the categories together.
Categories ‘Flight’, ‘Hotel’, ‘Car’
In ‘Figure 3’ we can see, the categories like ‘Flight’, ‘Hotel’, & ‘Car’ are placed far from each other in the embedding-space. While the keywords which are semantically and syntactically similar to the categories are positioned near to their respective categories.
Circling back to our example, let’s see how this message would be classified.
Traveller 2: We flew an hour late.
The classification pipeline uses a pre-processing step to clean the data. After cleaning the remaining keywords will be ‘flew’, ’hour’, ’late’.
Next the classification pipeline will calculate the linear distance. It does this by finding the linear vector distance of the keywords from the feedback with respect to our category keywords ‘Flight’, ‘Hotel’ & ‘Car’. The Heuristic Algorithm assigns the feedback to a category if the resulting linear distance is less than ’N’ (can be different for each category). Let’s look at the results.
Keyword: flew
Distance from category
Flight: 3.8168625831604004
Hotel: 5.281632900238037
Car: 5.459691047668457
Keyword: hour
Distance from category
Flight: 4.56382942199707
Hotel: 5.3469719886779785
Car: 5.401400089263916
Keyword: late
Distance from category
Flight: 5.427463531494141
Hotel: 5.393815517425537
Car: 5.658353805541992
As we can see above the keyword ‘flew’ is closest to category ‘Flight’ (3.8168625831604004). The eventual classification result of the feedback will be ‘Flight’ , provided the value of ’N’ for category ‘Flight’ is configured as 4.
Note: By making small changes to the value of ’N’ and analysing the results, we enriched the classification results.
This is how we are able to understand the context of the feedback message using an un-supervised learning approach, in order to perform Multi-Label Classification. Which we are then able to send classified feedback messages to the correct teams so they can take action on the feedback.
Conclusion
In this article, we have presented a methodology of classification of data when there is no dataset available for training in order to mitigate the shortcomings of ubiquitous supervised classification models by leveraging word-embeddings using GloVe.
Acknowledgements
The Conversation Platform Voice of Traveller Team at Expedia carried out this project and I would like to thank and acknowledge my colleagues for their contribution to this project.
Click here to learn more about technology at Expedia Group.
References
PCA: https://en.wikipedia.org/wiki/Principal_component_analysis
GloVe stanford link: https://nlp.stanford.edu/projects/glove/
Glove github link: https://github.com/stanfordnlp/GloVe
Word embedding: https://www.tensorflow.org/text/guide/word_embeddings
