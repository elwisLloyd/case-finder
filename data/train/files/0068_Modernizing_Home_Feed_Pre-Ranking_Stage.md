# Modernizing Home Feed Pre-Ranking Stage

Источник: https://medium.com/pinterest-engineering/modernizing-home-feed-pre-ranking-stage-e636c9cdc36b

Bella Huang | Machine Learning Engineer, Homefeed Candidate Generation
Dafang He | Machine Learning Engineer, Homefeed Relevance
Yuying Chen | Machine Learning Engineer, (formerly) Homefeed Candidate Generation
James Li | Engineering Manager, Homefeed Candidate Generation
Dylan Wang | Director, Homefeed Relevance
Modern recommendation systems typically follow a multi-stage design involving retrieval, pre-ranking, ranking, and reranking. Pinterest home feed recommendation system has similarly adopted these strategies over the years. We are excited to announce the big milestone in this journey with a sophisticated pre-ranking layer (aka Lightweight Scoring) that significantly improved our business metrics.
In this blog, we’d like to share the most foundational improvements in this stage, including both end-to-end system design and model design specifically tailored for this stage. Figure 1 illustrates the end-to-end Pinterest funnel design:
Limitations of the Initial Design
Many industrial level pre-ranking layers adopt a two-tower based approach [1][2]. In [1], we described how Pinterest home feed built our first generation of light-weight rankers. One key part is that in this design, the light-ranker runs separately on each retrieval source output. We then aggregate all the results from each retrieval source in the home feed logical server and send them to the full-ranking stage.
This design decision has various limitations. First, due to the fact that new model iterations need to be deployed on separate services, there is significantly more effort needed. We need to make sure all the experimental models are deployed in different services, and for each user request, we use the same model across different services. Second, due to various services involved, model auto-retraining becomes significantly challenging, as all different services need to be synchronized. Third, from a model architecture perspective, the two-tower based architecture typically cannot learn user item interactions well: all the interaction happens at the last stage as a dot-product. This late fusion mechanism significantly reduces the model’s capability in leveraging powerful features such as user action sequences.
In the sections below, we’ll share several foundational improvements the team has made to modernize this layer both from system perspective and model perspective.
Model and System Design
This section illustrates the end-to-end system design of the new pre-ranking layer. The model includes one request level sub-component and one item level sub-component. They are jointly trained and decoupled during serving for efficiency. Figure 2 illustrates the end-to-end system and model design.
For the request level sub-component, they take user and context features as input and generate a compressed user representation. As this is a request level model, we are able to scale up the model complexity significantly, as it only needs to be computed once per request.
On the item level, we are computing everything in an online manner including item feature extraction, processing, and user item feature crossing. Both parts of the models are trained end-to-end with designed loss, and each sub-component is decoupled during serving.
Logging Pipeline Design
As we are building a pre-ranking model that scores N times more candidates early in the funnel, it is important to distinguish it from Ranking in terms of training data. Various literature researches [3] have illustrated the Sample Selection Bias (SSB) in early funnel models. We designed and implemented an early funnel logging pipeline from scratch and combined it with final impression data as our training data. Figure 3 illustrated the end-to-end pipeline:
This data pipeline helps us bring unbiased data into our training and makes sure training and serving are more aligned.
Serving Architecture Design
As shown in Figure 2, in the item model we fetch raw item features and do the inference on the fly. The benefits of doing so are:
- Early crossing on user representation and item features
- Light weight model management and version sync, comparing to pre-computing item embeddings
- Ability to utilize real time features
However, fetching raw item features could bring CPU and memory overhead, as size of raw features is much larger than item embeddings. It’s also not possible to cache all items’ features into one single host, given our large corpus.
To mitigate this, we introduced a root-leaf architecture in the online inference service. The items are sharded by the keys, and each leaf host is assigned to always handle a specific shard of items. One request will firstly go to a root host, and the root host splits out the items and sends them to leaf, as shown in Figure 4.
This method limits the size of corpus on one single host and makes it possible to cache nearly all non-realtime features the host needs to handle. In practice, we observe a higher cache hit rate with significantly less the infra cost
Model Distillation
Once we have built the joint impression and unimpressed data for training, we are able to get rid of two-tower architecture with in-batch-negative sampling. Instead we can use “real negative” samples that are logged during our serving flow. These early funnel candidates provide more representative negative samples for our model.
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
In order to better align the pre-ranking model with L2 ranker, we adopted two loss as our major pre-ranking loss:
The Lʙᴄᴇ is a binary cross entropy loss trained with engagement as positive while all other samples as negative.
is the distillation loss where we tried to minimize the KL divergence between L2 calibrated scores and our pre-ranking model prediction.
Both losses are jointly optimized with a hyper-parameter w controlling the relative weight for the distillation loss.
Online Experiments
In this section, we describe several foundational improvements on the pre-ranking layer including the model architecture, training data and serving pipeline.
Initial Launch
The initial launch of this next generation of pre-ranking comes with the deprecation of all legacy light rankers described in [1]. The model we launched was still a two-tower architecture with the item-side tower doing online computation and dot-product interaction with the user tower. We are able to achieve significant top line engagement wins. Also, the launch has significantly driven new use case adoption and various other metrics.
The gain of this mostly comes from the following aspects:
- More standardized feature fetching
- Larger embedding dimensions as we are computing purely in an online manner
- More coverage on different retrieval sources that couldn’t be covered previously
Early Funnel Log Adoption
In the first launch, we are still leveraging a two-tower-based approach. While modern pre-ranking models usually leverage a more complicated architecture to enable better user item feature crossing. In order to onboard non-two-tower model architecture with relatively more complicated interaction, we found out that it is critical to enable early funnel log in training.
In the original pre-ranking model, we are leveraging a two-tower architecture with in-batch-negative sampling and sampled soft. We combine it with sample probabilistic correction [4]. In-batch negative and sampled softmax [4], though pretty effective for two-tower model training as it created a rich amount of contrastive examples for the positive engagement, is relatively hard to be adopted in a non-two-tower model. This is because of the challenges in creating such pairs for contrastive learning efficiently in training non-two-tower models. Fortunately, as we enabled early funnel logging, we are able to use the more representative negative samples and make it possible to onboard non-two-tower architectures.
Here we list four versions of the model architecture categories and loss designs together with their experiment results:
Through various analyses we found that with a non-two-tower architecture to improve user, item interaction and combined it with early funnel log (unimpressed candidates) and impressed candidates, we are able to achieve the best performance.
Auto-Model Retraining
In order to leverage fresh engagement data to improve timeliness of our recommendation, we also worked on setting up the auto-retraining framework. Even though the same model would be decoupled into two serving components, they are served in the same model server cluster, so it is much easier for auto-retraining synchronization between different model versions. This is also one of the major motivations to deprecate the legacy pre-ranking component. We do see significant improvement in user engagement when we conduct frequent retraining.
On-going Works
In this post, we described several foundational works leading to our next generation of pre-ranking. We will share more on-going works with modeling innovations that have kept improving our user engagement. There are several directions for further improvements:
- Data sampling and better understanding of our data composition including both early funnel logging and impression data
- Model architecture improvement
- Loss exploration
- Serving Optimization
We will discuss these components in future blogs.
Acknowledgement
We would like to express our thank various engineers who supported and made contribution to this project: Bowen Deng, Hedi Xia, J.J Hu, Devin Kreuzer, Yichu Zhou, Haoyu Chen, Zach Fan, Piyush Maheshwari, Matthew Lawhon, Aditya Mantha, Abhinav Naikawadi, Dhruvil Deven Badani, Jiahuan Liu, Lucy Qiao, Shun-ping Chiu, Cheng Duan, Jay Adams, Nazanin Farahpour, Chi Zhang, Se Won Jang, Saurabh Vishwas Joshi
[1] Pinterest Home Feed Unified Lightweight Scoring: A Two-tower Approach
[2] Scaling the Instagram Explore recommendations system
[3] Rethinking the Role of Pre-ranking in Large-scale E-Commerce Searching System. 2023
[4] On the Effectiveness of Sampled Softmax Loss for Item Recommendation 2022
[5] An Empirical Study of Selection Bias in Pinterest Ads Retrieval, KDD 2023
