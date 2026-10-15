# Identify User Journeys at Pinterest

Источник: https://medium.com/pinterest-engineering/identify-user-journeys-at-pinterest-b517f6275b42

Lin Zhu | Sr. Staff Machine Learning Engineer
Jaewon Yang | Principal Machine Learning Engineer
Ravi Kiran Holur Vijay | Director, Machine Learning Engineering
Pinterest has always been a go-to destination for inspiration, a place where users explore everything from daily meal ideas to major life events like planning a wedding or renovating a home. Our core mission is to be an inspiration-to-realization platform. To fulfill this, we recognized a critical challenge: we needed to move beyond understanding immediate interests and comprehend the underlying, long-term goals of our users. Therefore, we introduce user journeys as the foundation for recommendations.
We define a journey as the intersection of a user’s interests, intent, and context at a specific point in time. A user journey is a sequence of user-item interactions, often spanning multiple sessions, that centers on a particular interest and reveals a clear intent — such as exploring trends or making a purchase. For example, a journey might involve an interest in “summer dresses,” an intent to “learn what’s in style,” and a context of being “ready to buy.” Users can have multiple, sometimes overlapping, journeys occurring simultaneously as their interests and goals evolve.
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
Inferring user journeys goes beyond understanding immediate interests, it allows us to comprehend the underlying, long-term goals of our users. By identifying user journeys, we can move from simple content recommendations to becoming a platform that assists users in achieving their goals, whether it’s planning a wedding, renovating a kitchen, or learning a new skill. This aligns with Pinterest’s mission to be an inspiration-to-realization platform, and provides the foundation for journey-aware recommendations.
Our Solution Philosophy
From the outset, we knew we were building a new product without large amounts of training data. This constraint shaped our engineering philosophy for this project:
- Be Lean: Minimize the development of new components where no data exists.
- Start Small: Begin with a small, high-quality dataset of a few hundred human-annotated examples.
- Leverage Foundation Models: Utilize pretrained models, like pretrained SearchSage for keyword embeddings, to maximize cost efficiency and effectiveness.
- Make it Extensible: Design a system that supports more complex models as we collect more data, with a clear path to incorporating more advanced ML and LLM techniques.
System Architecture: A Walkthrough
To identify these journeys, we evaluated two primary approaches:
- Predefined Journey Taxonomy: Building a fixed set of journeys and mapping users to them. While this offers consistency, it risks overlapping with existing systems, requiring significant maintenance, and being slow to adapt to new trends.
- Dynamic Keyword Extraction: Directly extracting journeys from a user’s activities, representing each journey as a cluster of keywords (queries, annotations, interests, etc.).
We chose the Dynamic Extraction approach to generate journeys based on the user’s information. It offered greater flexibility, personalization, and adaptability, allowing the system to respond to emerging trends and unique user behaviors. This method also allowed us to leverage existing infrastructure and simplify the modeling process by focusing on clustering activities for individual users.
At a high level, we extract keywords from multiple sources and employ hierarchical clustering to generate keyword clusters; each cluster is a journey candidate. We then build specialized models for journey ranking, stage prediction, naming, and expansion. This inference pipeline runs on a streaming system, allowing us to run full inference if there’s algorithm change, or daily incremental inference for recent active users so the journeys respond quickly to a user’s most recent activities.
Let’s break down the key components of this innovative system:
1. User Journey Extraction and Clustering
This foundational component is designed to generate fresh, personalized journeys for each user.
- Input Data: We leverage a rich set of user data, including:
— User search history: Aggregated queries and timestamps.
— User activity history: Interactions like Pin closeups, repins, and clickthroughs, extract the annotations and interests from the engaged Pins.
— User’s boards: Extract the annotations and interests from the Pins in the user’s boards.
- User Journey Clustering: We treat all the queries, annotations, and interests as keywords with metadata. Then we adopt the pretrained text embedding for the keywords to perform hierarchical clustering to form journey clusters.
2. Journey Naming & Expansion
Clear and intuitive journey names are crucial for user experience.
- Journey Naming: The current production model is to apply a ranking model to pick the top keyword extracted from each cluster as the journey name. It balances personalization and simplicity by choosing the most relevant keywords from the cluster. We are working with scaling LLM for Journey Name Generation, which promises highly personalized and adaptable names.
- Journey Expansion: We leverage LLMs to generate new journey recommendations based on a user’s past or ongoing journeys, with an emphasis on balancing the predictive power of LLMs and efficiently serving through pre-generated recommendations. In the initial stage, we focus on creating non-personalized, related journeys based on a given input journey. Since the total number of journeys is limited, we can use LLMs to generate this data offline and store it in a key-value store. For personalized recommendations, we will apply the journey ranking model online to rank related journeys for each user.
3. Journey Ranking & Diversification
To ensure the most relevant journeys are presented, and to prevent monotony, we built a ranking model and applied diversification afterwards.
Journey Ranking
Similar to traditional ranking problems, our initial approach is to build a point-wise ranking model. We get labels from user email feedback and human annotation. The model takes user features, engagement features (how frequently the user engaged on this journey through search, actions on Pins, etc.) and recency features. This provides a simple, immediate baseline.
Journey Diversification
To prevent the top ranked journeys from always being similar, we implement a diversifier after the journey ranking stage. The most straightforward approach is to apply a penalty if the journey is similar to the journeys that ranked higher (the similarity is measured using pretrained keyword embedding). For each journey i, score will be updated based on the formula below. Finally, we re-rank the journeys according to the updated score.
Occurrence is the number of similar journeys ranked before the current journey, and penalty is a hyperparameter to tune, usually chosen as 0.95.
4. Journey Stage Prediction
Understanding a journey’s lifecycle helps us determine appropriate notification timing. We simplify this into two objectives:
- Situational vs. Evergreen Classification: Journeys are categorized based on user engagement patterns and activity duration. If users engage with a journey consistently over an extended period, we classify it as “Evergreen” — these journeys remain perpetually active. In contrast, journeys with engagement limited to a shorter timeframe are classified as “Situational,” as they are expected to conclude at a certain point.
- Journey Stage (Ongoing vs. Ended) Classification: For situational journeys, we evaluate whether the journey is still ongoing or has ended, primarily by analyzing the time since the user’s last engagement. Future improvements will include incorporating user feedback and developing a supervised model for more accurate classification.
5. User Journeys Output
The user journeys could be used in downstream applications for retrieval and ranking. The desired output is a list of distinct user journeys. Each journey should ideally be represented with:
- Journey Name: A concise and descriptive name (e.g., “Kitchen Renovation,” “Improving Home Organization,” “Engagement Ring Selection”).
- Keywords: List of keywords related to this journey; it could be the corresponding interests, annotations, queries, or any keywords.
- Stage: An indicator of where the user is within that journey (e.g., “inspiration,” “action”); we simplified it to “ongoing” or “ended” in the initial launch.
Confidence Score: The confidence score for this predicted journey.
6. Relevance Evaluation
We aim to establish a robust evaluation and monitoring pipeline to ensure consistent and reliable quality assessment of top-k user journey predictions. Because human evaluation is costly and sometimes inconsistent, we leverage LLMs to assess the relevance of predicted user journeys. By providing user features and engagement history, we ask the LLM to generate a 5-level score with explanations. We have validated that LLM judgments closely correlate with human assessments in our use case, giving us confidence in this approach.
Experiment Results
We applied user journeys inference to deliver notifications related to the user’s ongoing journeys. Our initial experiments demonstrate the significant impact of Journey-Aware Notifications¹:
- The system drove statistically significant gains in user engagements.
- Compared to our existing interest-based notifications, journey-aware notifications demonstrated an 88% higher email click rate and a 32% higher push open rate.
- User surveys revealed a 23% increase in positive feedback rate compared to interest-based notifications.
Ongoing Effort
As a follow up, we are working on leveraging large language models (LLMs) to infer user journeys given user information and activities, while offering several key benefits:
- Simplification: Many existing components of the journey inference system — including keyword extraction, clustering, journey naming, and stage prediction models — can be consolidated and replaced with a single LLM.
- Quality Improvement: By utilizing the advanced capabilities of LLMs to understand user behavior, we aim to significantly enhance the accuracy and quality of user journey predictions.
We tuned our prompts and used GPT to generate ground truth labels for fine-tuning Qwen, enabling us to scale in-house LLM inference while maintaining competitive relevance. Next, we utilized Ray batch inference to improve the efficiency and scalability. Finally, we are implementing full inference for all users and incremental inference for recently active users to reduce overall inference costs. All generated journeys will go through safety checks to ensure they meet our safety standards.
Acknowledgement
We’d like to thank Kevin Che, Justin Tran, Rui Liu, Anya Trivedi, Binghui Gong, Randy Tumalle, Tianqi Wang, Fangzheng Tian, Eric Tam, Manan Kalra, Mengtian Hu and Mengying Yang for their contribution!
Thanks Jeanette Mukai, Darien Boyd, Samuel Owens, Justin Pangilinan, Blake Weber, Gloria Lee, Jess Adamiak for the product insights!
Thanks Tingting Zhu, Shivani Rao, Dimitra Tsiaousi, Ye Tian, Vishwakarma Singh, Shipeng Yu, Rajat Raina and Randall Keller for the support!
¹Pinterest Internal Data, USA, April-May 2025
