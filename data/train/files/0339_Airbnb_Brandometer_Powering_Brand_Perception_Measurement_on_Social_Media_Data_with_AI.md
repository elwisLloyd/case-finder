# Airbnb Brandometer: Powering Brand Perception Measurement on Social Media Data with AI

Источник: https://medium.com/airbnb-engineering/airbnb-brandometer-powering-brand-perception-measurement-on-social-media-data-with-ai-c83019408051

Airbnb Brandometer: Powering brand perception measurement on social media data with AI
How we quantify brand perceptions from social media platforms through deep learning.
How we quantify brand perceptions from social media platforms through deep learning
By Tiantian Zhang, Shuai Shao (Shawn)
Introduction
At Airbnb, we have developed Brandometer, a state-of-the-art natural language understanding (NLU) technique for understanding brand perception based on social media data.
Brand perception refers to the general feelings and experiences of customers with a company. Quantitatively, measuring brand perception is an extremely challenging task. Traditionally, we rely on customer surveys to find out what customers think about a company. The downsides of such a qualitative study is the bias in sampling and the limitation in data scale. Social media data, on the other hand, is the largest consumer database where users share their experiences and is the ideal complementary consumer data to capture brand perceptions.
Compared to traditional approaches to extract concurrency and count-based top relevant topics, Brandometer learns word embeddings and utilizes embedding distances to measure relatedness of brand perceptions (e.g., ‘belonging’, ‘connected’, ‘reliable’). Word embedding represents words in the form of real-valued vectors, and it performs well in reserving semantic meanings and relatedness of words. Word embeddings obtained from deep neural networks are arguably the most popular and evolutionary approaches in NLU. We explored a variety of word embedding models, from quintessential algorithms Word2Vec and FastText, to the latest language model DeBERTa, and compared them in terms of generating reliable brand perception scores.
For concepts represented as words, we use similarity between its embedding and that of “Airbnb” to measure how important the concept is with respect to the Airbnb brand, which is named as Perception Score. Brand Perception is defined as Cosine Similarity between Airbnb and the specific keyword:
where
In this blog post, we will introduce how we process and understand social media data, capture brand perceptions via deep learning and how to ‘convert’ the cosine similarities to calibrated Brandometer metrics. We will also share the insights derived from Brandometer metrics.
Brandometer methodology
Problem setup and data
In order to measure brand perception on social media, we assessed all Airbnb related mentions from 19 platforms (e.g., X — formerly known as Twitter, Facebook, Reddit, etc) and generated word embeddings with state-of-the-art models.
In order to use Social media data to generate meaningful word embeddings for the purpose of measuring brand perception, we conquered two challenges:
- Quality: Social media posts are mostly user-generated with varying content such as status sharing and reviews, and can be very noisy.
- Quantity: Social media post sparsity is another challenge. Considering that it typically requires some time for social media users to generate data in response to certain activities and events, a monthly rolling window maintains a good balance of promptness and detectability. Our monthly dataset is relatively small (around 20 million words) as compared to a typical dataset used to train good quality word embeddings (e.g., about 100 billion words for Google News Word2Vec model). Warm-start from pre-trained models didn’t help since the in-domain data barely moved the learned embeddings.
We developed multiple data cleaning processes to improve data quality. At the same time, we innovated the modeling techniques to mitigate the impact on word embedding quality due to data quantity and quality.
In addition to data, we explored and compared multiple word embedding training techniques with the goal to generate reliable brand perception scores.
Word2Vec
Word2Vec is by far the simplest and most widely used word embedding model since 2013. We started with building CBOW-based Word2Vec models using Gensim. Word2Vec produced decent in-domain word embeddings, and more importantly, the concept of analogies. In our domain-specific word embeddings, we are able to capture analogies in the Airbnb domain, such as “host” — “provide” + “guest” ~= “need”, “city” — “mall” + “nature” ~= “park”.
FastText
FastText takes into account the internal structure of words, and is more robust to out-of-vocabulary words and smaller datasets. Moreover, as inspired by Sense2Vec, we associate words with sentiments (i.e., POSITIVE, NEGATIVE, NEUTRAL), which forms brand perception concepts on the sentiment levels.
DeBERTa
Recent progress in transformer-based language models (e.g., BERT) has significantly improved the performance of NLU tasks with the advantage of generating contextualized word embeddings. We developed DeBERTa based word embeddings, which works better with smaller dataset and pays more attention to surrounding context via disentangled attention mechanisms. We trained everything from scratch (including tokenizer) using Transformers, and the concatenated last attention layer embeddings resulted in the best word embeddings for our case.
Brand perception score stabilization and calibration
The variability of word embeddings has been widely studied (Borah, 2021). The causes range from the underlying stochastic nature of deep learning models (e.g., random initialization of word embeddings, embedding training which leads to local optimum for global optimization criteria) to the quantity and quality changes of data corpus across time.
With Brandometer, we need to reduce the variability in embedding distances to generate stable time series tracking. Stable embedding distances helped preserve the inherent patterns and structures present in the time series data, and hence it contributes to better predictability of the tracking process. Additionally, it made the tracking process more robust to noisy fluctuations. We studied the influential factors and took the following steps to reduce:
- Score averaging over repetitive training with bootstrap sampling
- Rank-based perception score
Score averaging over repetitive training with upsampling
For each month’s data, we trained N models with the same hyper-parameters, and took the average of N perception scores as the final score for each concept. Meanwhile, we did upsampling to make sure that each model iterated on an equal number of data points across months.
We defined variability as:
where
CosSim(w) refers to the cosine similarity based perception score defined in Eq. 1, A refers to the algorithm, M refers to the time window (i.e. month), V refers to the vocabulary and |V| is the vocabulary size, and n refers to the number of repetitively trained models.
As N approaches 30, the score variability values converge and settle within a narrow interval. Hence, we picked N = 30 for all.
Rank-based perception score
Based on Maria Antoniak’s work, we used the overlap between nearest neighbors to measure the stability of word embeddings, since the relative distances matter more than the absolute distance values in downstream tasks. Therefore, we also developed rank-based scores, which shows greater stability as compared to similarity-based scores.
Get Tiantian Zhang’s stories in your inbox
Join Medium for free to get updates from this writer.
For each word, we first ranked them in descending order of cosine similarity via Eq. 1. The rank-based similarity score is then computed as 1/rank(w) where w∈V. More relevant concepts will have higher rank-based perception scores.
The score variability is defined the same as Variability(A, M, V) in Eq. 2 except that
where RankSim(w) refers to the rank based perception score. With rank-based scores, when N approaches to 30, the score variability values converge to a much narrower interval especially for DeBERTa.
Selection of score output by designed metrics
One challenge of this project was that we didn’t have a simple and ultimate way to conclude which score output was better since there is no objective ‘truth’ of brand perception. Instead, we defined a new metric to learn some characteristics of the score.
Average Variance Across Different Period (AVADP)
- We first picked the group of top relevant brand perceptions for Airbnb: ‘host,’ ‘vacation,’ ‘rental,’ ‘love,’ ‘stay,’ ‘home,’ ‘booking,’ ‘travel,’ ‘guest’.
- Higher value indicates more fluctuations across different periods — likely a bad thing, because the selected brand perception is assumed to be relatively stable and hence should not vary too much month by month.
We checked these statistics on the calibrated results as shown above. We can see that the ranked-based score is the winner as compared to similarity-based scores:
- Lower AVADP: More fluctuations than the non-ranked across a different period — likely a good thing, because the selected brand perception is assumed to be relatively stable and hence should not vary too much month by month.
Use cases of Brandometer
Though we set out to solve the problem of brand measurement, we believe use cases can go above and beyond:
Use cases deep dive
Industry Analysis: Top Brand Perception among Key Players [Monthly Top Perception]
With top perceptions such as “Stay” and “Home,” Airbnb provides a brand image of “belonging”, echoing our mission statement and unique supply inventory, while other companies have “Rental,” “Room,” “Booking,” a description of functionality, not human sensation.
Top emerging perception reveals major events discussed online [monthly top perception]
The Top 10 Perceptions are generally stable month to month. The top standing perceptions include
- Home, Host, Stay, Travel, Guest, Rental, etc.
Meanwhile, we use Brandometer to monitor emerging perceptions that jump to the top list, which may reflect major events associated with the brand or user preference changes.
Major campaign monitor (time series tracking)
Businesses create campaigns to promote products and expand the brand image. We were able to capture a perception change on one specific Brand Theme after a related campaign.
These use cases are just the beginning. Essentially, this is an innovative way of gathering massive online input as we learn the needs and perception of the community. We will constantly reflect on how we leverage these insights to continually improve the Airbnb experience for our community.
Next steps
Airbnb’s innovative Brandometer has already demonstrated success in capturing brand perception from social media data. There are several directions for future improvement:
- Better content segmentation for clearer and more concise insights.
- Develop more metrics reflecting social media brand perception.
- Enhance data foundation, not just Airbnb, but other companies in the same market segment to get more comprehensive insights.
If this kind of work sounds appealing to you, check out our open roles — we’re hiring!
Acknowledgments
Thanks to Mia Zhao, Bo Zeng, Cassie Cao for contributing the best ideas on improving and landing Airbnb Brandometer. Thanks to Jon Young, Narin Leininger, Allison Frelinger for the support of social media data consolidation. Thanks to Linsha Chen, Sam Barrows, Hannah Jeton, and Irina Azu who provide feedback and suggestions. Thanks to Lianghao Li, Kelvin Xiong, Nathan Triplett, Joy Zhang, Andy Yasutake for reviewing and polishing the blog post content and all the great suggestions. Thank Joy Zhang, Tina Su, Andy Yasutake for leadership support!
Special thanks to Joy Zhang, who initiated the idea, for all the inspiring conversations, continuous guidance and support!
All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this website are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.
