# Reinvent your recommender system using Vector Database and Opinion Mining

Источник: https://medium.com/dailymotion/reinvent-your-recommender-system-using-vector-database-and-opinion-mining-a4fadf97d020

Reinvent your recommender system using Vector Database and Opinion Mining
With its new positioning, Dailymotion wants to give its users the possibility to get out of their filter bubble. The new home feed is designed to allow everyone to debate and confront their opinions.
One feed, several opinions
Dailymotion mobile app offers a single feed with vertical videos from a broad list of content creators. The aim is to offer diversified and stimulating content that adapts to the user’s desires, while allowing them to challenge or express their opinions.
Download the app on Google Play or App Store and try it yourself!
Significant work has already been done to build this new Homefeed using an architecture inspired by the multi-armed bandit and multi-stage recommender system. You can learn more about our very first steps in building this model here.
This article presents a newly created recommender system built on top of this existing architecture. The goal of this new feature is to provide our users with a different point of view on videos or topics they have already engaged with.
Overview of the Home Feed architecture
In order to understand this new recommender system, a very quick explanation of the Home Feed architecture may be necessary.
If we simplify the architecture, the algorithm responsible for recommending videos within our home feed can be considered as a combination of different small recommender systems, each with its own behavior: one to recommend videos based on their performance metrics (watch time, number of views, freshness…), another to recommend videos based on the user’s history or subscribed channels.
This article will focus on our new “opinion-based” recommender, a more original recommender system which goal is to recommend personalized content while also attempting to challenge the user’s opinions.
While writing this article, the recommendations provided by this new recommender system are available through a button “Show me a different POV” appearing on each eligible video. The feature will evolve in the coming months.
Bring more perspective
Before going into detail on every aspect of this recommender system, it might be useful to describe its overall approach.
First of all, the new recommender system is designed at a video level. In fact, for each video on a user’s home feed, the first step of the “opinion-based” recommender (or “Perspective BETA” feature) is to find similar videos, i.e, videos also talking about the same topic as the input video.
This brings up an important aspect of this new feature: not all videos are eligible. For example, some videos may be too “niche” in their subject matter, making it impossible to find similar videos.
The second and undoubtedly most important aspect of this recommender system is to rank these videos according to the opinion they express.
Finally, we have, when it’s possible, a list of similar videos ranked by the intensity of the opinion they express.
This quick explanation of our new “opinion-based” recommender system makes it possible to divide it into two main steps:
- Candidate Generation: responsible for finding videos evoking the same subjects as those already enjoyed by the user.
- Re-ranking: order the resulting videos and recommend videos having a strong and/or different opinion.
The following schema details the subparts of this 2-step architecture :
Candidate Generation
Dailymotion’s catalog contains several hundred million videos. The goal of the candidate generator is to transform this video catalog into a short list of dozens of relevant videos for a user.
The first filter is done using simple heuristics: for instance, for French users, we only want to recommend recent content, in French, from content creators and traditional media. By doing this, we can already narrow down the list to a few hundred thousand videos.
Nevertheless, we still need to reduce the number of videos while also finding videos that are similar to the ones the user has already watched. To achieve this, we need to represent each video as a vector.
Textual embeddings to represent videos
In order to embed a video object, i.e represent a video as a vector with real numbers in a continuous vector space, several options are available: Frame-Level embedding, Multi-modal embedding… All these options have an important drawback: they are computationally heavy.
Get Samuel Leonardo Gracio’s stories in your inbox
Join Medium for free to get updates from this writer.
Fortunately, each video uploaded to Dailymotion is also associated with several textual metadata: a title, description, and some tags. Transforming a textual information into a vector is both simpler and cheaper. To do that, we use the Multilingual Universal Sentence Encoder (MUSE), a pre-trained and open-source multilingual sentence embedding model handling 16 languages, including French.
Nevertheless, the video metadata can sometimes be too limited. Some videos may have textual metadata that does not showcase the real content of the video. For example, a video where the only information available is a title “My Daily VLOG” and no description at all may not provide enough textual information.
However, a solution to this lack of textual information can be found. Recent advances in speech-to-text models have led to the emergence of a pre-trained and open-source solution that makes it easy to obtain a transcript of a video: Whisper.
The Machine Whisperer
Whisper is an open-source speech recognition model developed by OpenAI capable of providing automatic video subtitles. Based on a Transformer sequence-to-sequence model, Whisper has been trained with 680k hours of training data in several languages and with different audio quality, making it robust for all types of audio soundtracks.
Subtitles are an essential feature to make our mobile app accessible to everyone. Moreover, they can also be used as transcripts of our videos, i.e., a written record of the spoken content in a video.
These auto-generated transcripts, typically of very good quality, allow us to extract much more textual information than the video title or description.
By using Whisper to obtain the transcript and MUSE to embed the text contained in this transcript, we can now obtain a complete representation of the actual video content using only textual metadata.
The following diagram describes how this pipeline works but also introduces a new element in the overall architecture of our recommender: Qdrant.
Qdrant: build a K-NN
Qdrant is an open-source vector search database. Qdrant is designed to efficiently handle high-dimensional vector data and enables retrieval of similar vectors based on their cosine similarity scores. It is based on an algorithm called Hierarchical Navigable Small World (HNSW), an approximate K-NN algorithm with a very short response time (≈20ms).
A Qdrant database can easily store hundreds of thousands of embeddings, along with various associated metadata such as the video’s language, creation date, or other useful information if we wish to filter certain videos when querying the server.
Qdrant is the final step of the candidate generator: it enables quick retrieval of similar videos from any video liked by a user on the home feed. For instance, for any video in the Qdrant database, we can use its embedding to retrieve N similar videos using its approximate K-NN functionality and cosine similarity.
Nevertheless, even if among some of these N closest videos some contain different points of view, we still need to re-rank the output of this approximate K-NN in order to give priority to videos with a strong or different opinion.
Re-ranking: express your opinion
Now that we have our candidate videos, i.e, the N closest videos to an input video, we can now re-rank this short list of videos in order to push content that will challenge the opinion of the user.
Opinion mining, also known as sentiment analysis, is a subfield of natural language processing (NLP) and machine learning that aims to determine the sentiment or emotional tone expressed in a piece of text.
With the recent dominance of Large Language Models (LLM) like GPT (OpenAI), LLaMA (Meta) or PaLM (Google), sentiment analysis has also received a significant boost. These complex models are also capable of analyzing text and assigning it an opinion score.
In our case, we send each video transcript to Google’s PaLM API. The model predicts a score, ranging from -1 to 1, which reflects the video’s opinion on the subject it addresses. The higher the score in absolute value, the stronger the opinion. A score of zero means that the video is neutral and does not express any particular opinion.
In this re-ranking stage, we also use other video metadata such as the aspect ratio of the video or the freshness to build our final ranking.
Finally, we have the final output of this new recommender system: for each video liked by a user, we can now retrieve similar videos ranked in terms of opinion intensity.
Create your own opinion
We are proud to have presented you a more original recommender system, not only personalizing content for users using a content-based approach but also challenging their opinions by re-ranking the result using sentiment analysis.
The two main subparts of this opinion-based recommender system, namely Candidate Generation and Re-ranking, play crucial roles in building this key feature for Dailymotion.
Would you like to be part of upcoming meaningful Data and AI products at Dailymotion? Check our open positions.
