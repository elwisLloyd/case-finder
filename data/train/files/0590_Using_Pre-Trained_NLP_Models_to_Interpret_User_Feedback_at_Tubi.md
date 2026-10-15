# Using Pre-Trained NLP Models to Interpret User Feedback at Tubi

Источник: https://code.tubitv.com/using-pre-trained-nlp-models-to-interpret-user-feedback-at-tubi-6dffecf46510

Special thanks to Lifan Zhang for her amazing contributions to this project!
Introduction
Tubi receives a variety of text feedback from users, from comments that accompany Net Promoter Score (NPS) submissions, customer support tickets, and app store reviews. We receive thousands of these comments every day and there is no scalable way to have people read through all of them. However, within these comments lies valuable user insights.
So how can we extract and leverage these insights?
Our approach first categorizes each user response into relevant buckets. By leveraging unsupervised ML algorithms, we can quickly categorize each comment into a high-level topic and track the topic trends over time. Then using this information, we can identify where to focus our product initiatives.
This process can technically be replaced with a team of people going through every individual comment and manually tagging them with the categories, but doing it with a set of models allows us to achieve similar results in much less time scalably. Furthermore, this process is much easier to replicate as our user base grows and when we want to apply this to more use cases.
In the last decade, significant developments in the natural language processing (NLP) domain have made it easier to utilize these methods in a repeatable way. One example is publicly available pre-trained models that can be applied to a variety of business applications. In this blog post, we’ll give an overview of how Tubi uses NLP to help us identify trends and extract insights from large amounts of user-submitted text data.
Applications
Before we get into the methodology, let’s talk about some of the business applications at Tubi. Currently, we’re using NLP to derive insights from two sources of text feedback: net promoter scores and customer support tickets.
Use Case 1: Net Promoter Score Comments
Our first use case is NPS comments. The original purpose of NPS is to capture user satisfaction in a numerical value unrelated to the text comment we collect. At Tubi, we ask viewers how likely they are to recommend us to a friend on a scale of 0 to 10. Along with that score, we also ask them to comment on why they submitted that score. These comments contain valuable information, and we wanted a way to track any trends in what users are communicating to us. For example, are users talking about bugs more frequently in the past week?
From reading through a sample of the NPS comments, we know that they tend to fall into the following categories (figure 1):
- Content: feedback about Tubi’s content library. Some examples include requests for new genres and requests for specific titles.
- App: general feedback about the Tubi app. This is essentially an “other” category.
- Ads: feedback about ad duration, frequency, timing, etc.
- Features & Bugs: feedback about specific app features or buggy experiences.
With NLP, we created a set of classification models that categorize NPS comments into the above categories every day. We then created a dashboard to track the counts and distribution of classes over time. This data allows us to highlight areas in our product to prioritize and is currently being used by our product management team to spawn ideas for product improvements.
Use Case 2: Customer Support Tickets
Our second use case is customer support tickets. Tubi users are given many different avenues (like email or Facebook) to open support tickets and describe any problems they are experiencing. Similar to NPS, we defined a set of comment types that we wanted to monitor. For each category, we then created a classification model to identify whether any given comment belongs to that category. Finally, just like with NPS, we created a dashboard to monitor trends over time.
Our amazing customer support team defined the following categories based on their experience reading through tickets (figure 2):
- Request: users requesting a feature, functionality, or content that will improve their experience.
- Issue: problem with a function that should be fixed.
- Inquiry: anything from a third party, non-user. For example, job seekers, content partners, legal matters, etc.
- Complaint: the user is not happy with something that we are doing, and the issue is not something that we can easily fix.
- Question: user asking how something works, why, when, etc.
We’re currently exploring how to use these models in a more automated way in order to route support tickets to the appropriate teams and hopefully cut down on our customer support team’s time commitment to reading all of these tickets (figure 3).
Methodology
Now that we understand the use cases at Tubi let’s discuss how we developed the classification models.
Embeddings
The first step in developing the classification model is to develop embeddings.
As noted above, a block of text containing user feedback is a data point. The main difficulty lies in how to translate the meaning of that data point to something a machine learning model can more easily interpret. We’re getting closer every day to having robots that can understand human languages, but for now, we have to do a little bit of legwork to translate it for them (figure 4).
This is where text encoding techniques can help. At the heart of it, we need to convert a sentence to a set of numerical values, or a vector, that represents the semantic meaning of the sentence. These vectors are called embeddings and we can use these to calculate distances or similarities between pairs of embeddings.
Get Billy Zou’s stories in your inbox
Join Medium for free to get updates from this writer.
If you’re unfamiliar, an embedding is an n-dimensional object that encodes the information from a sentence. Each sentence has its own unique meaning, but some are more similar in meaning to other specific sentences. To illustrate this concept further, imagine every word in the English language lives in a 2-dimensional space. A very small sample of that space might look like figure 5, where each word is represented by an (x, y) vector:
Now imagine, instead of individual words in two-dimensional space, we’re working with sequences of individual words (sentences) in n-dimensional spaces. An embedding represents that text in the form of a vector in that space. As shown in figure 6, once they are in vector format, we can calculate distances between the values and derive similarities between different texts.
Two (among many) popular encoders are Universal Sentence Encoder (USE) and Bidirectional Encoder Representations from Transformers (BERT), both published in 2018. We won’t go into detailed explanations of each, but at their core, both do the same high-level process: take in text and output a vectorized embedding. Both of these encoders leverage transfer learning; they are pre-trained by different teams at Google and are available for public use on TensorFlow Hub.
Despite the similarities between the two, the core goals are different:
- The goal of USE is to “provide a single encoder that can support as wide a variety of applications as possible, including paraphrase detection, relatedness, clustering, and custom text classification.” The developers haven’t provided information on how much data they used but stated that they trained the models on a variety of text sources such as “Wikipedia, web news, web question-answer pages, and discussion forums.” USE has two versions, one that uses the Transformer architecture and another that uses deep averaging networks (DANs). (blogpost source)
- The goal of BERT is two main tasks: 1) it hides some of the words in the text input and trains to predict these words (AKA masked language modeling), and 2) it learns sentence relationships to predict whether a given sentence comes after another (AKA next sentence prediction). The developers have stated that the models are pre-trained with BooksCorpus data (800M words) and English Wikipedia (2,500M words). It has many different versions; all are based on the Transformer architecture. (blogpost source)
We tested both but ended up using USE due to better performance (more on this later). This aligns with our expectations because we need a way to bucket together similar sentences, in other words, perform custom text classification. This is one of the applications USE is designed to tackle; BERT’s ability to predict words and next sentences doesn’t directly help us here.
Classification Modeling
Armed with high-dimensional representations of our user feedback text, we can now build classification models.
As mentioned above, we already know that comments tend to fall into a handful of buckets. To convert our problem into a supervised learning task, we manually labeled a sample set of comments. We now have a target variable (or dependent variable) that we can use to train our model.
Great, but how do we use the embeddings? We can think of embeddings as a list of predictors (or independent variables) to input into a classification model. That model can then take those predictors to make a prediction and identify whether it belongs in a category or not. Couple these embeddings with our manually created target variable and we now have training data (figures 7 and 8). We took further steps to tune hyperparameters and thresholds to give us the best performance, but we won’t go into details here.
Now that we’ve boiled our problem down to supervised learning and classification, there is a whole world of classification algorithms that can be leveraged. We chose LightGBM due to its ease of use and lightweight nature which makes it the perfect candidate to deploy in production. It also exhibited strong performance on our data. As we iterate, we’ll continue to test other techniques like multiclass logistic regression, random forests, or naive Bayes.
Results
Leveraging the above techniques, we trained four sets of models where we compared USE and BERT for our two use cases. We focused on optimizing ROC AUC but also monitored other performance metrics like accuracy and F1 score (for all three metrics, a higher score is better):
NPS
Example texts:
- “because you have a lot of good movies I have been looking for. this is what I needed after working all day.” → content
- “the ads but its still good because you have a lot of good movies I like to watch.” → ads
Customer Support
Example texts:
- “Could you please add ‘Welcome Back Kotter’ to Tubi” → request
- “how to turn off autoplay” → question
USE ended up performing better in all three metrics across the board for each category. This aligns with our expectations because one of the primary strengths of USE is custom text classification.
Summary
With USE and LightGBM, we created a process that takes in text and spits out classifications. We first input a sample set of manually classified comments into an encoder, which outputs embeddings in the form of numerical vectors. Then, we throw it into a machine learning model for training.
The resulting classification model has the ability to take in new embeddings and predict whether each comment belongs to a pre-defined category or not. Finally, we save these predictions and create visualizations to track trends and highlight potential areas for focus.
Future
We’ve only scratched the surface of optimizing this process. To iterate on our current models, we can explore modeling techniques like multi-class modeling or deep neural nets, as well as other popular embedding techniques like the transformer version of USE, larger versions of BERT, BERTScore, XLNet, ELMO, etc. We can also apply these models to other applications such as sentiment analysis or keyword extraction.
If you’re interested in data science problems like these, please reach out! We’re always looking for eager people to join our team.
Thank you to our partners throughout this project (Sudeep Agarwal, James Jones, Danielle Alailima) and everyone who contributed ideas and feedback to this blog post.
