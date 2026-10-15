# Unlocking Efficient Ad Retrieval: Offline Approximate Nearest Neighbors in Pinterest Ads

Источник: https://medium.com/pinterest-engineering/unlocking-efficient-ad-retrieval-offline-approximate-nearest-neighbors-in-pinterest-ads-6fccc131ac14

Unlocking Efficient Ad Retrieval: Offline Approximate Nearest Neighbors in Pinterest Ads
Authors (non-ordered): Qishan(Shanna) Zhu, Chen Hu
Acknowledgements: Longyu Zhao, Jacob Gao, Quannan Li, Dinesh Govindaraj
Introduction
In the evolving landscape of advertising, the demand for real-time personalization and dynamic ad delivery has made Online Approximate Nearest Neighbors (ANN) a mainstream method for ad retrieval. Pinterest primarily employs online ANN to swiftly adapt to users’ behavior changes (depending on their age, location and privacy settings), thereby enhancing ad responsiveness and relevance.
However, offline ANN is also a valuable option, particularly when large-scale data processing, efficient resource utilization, and cost-effective operations are critical. By precomputing candidates offline, this approach is ideal for scenarios that require high throughput and low-latency query responses and relatively static query context. This article explores suitable use cases for offline ANN, outlines its advantages and disadvantages, shares insights from our experiences, and illustrates its application within Pinterest. We will also discuss potential future enhancements.
Problem Statement
Pinterest has successfully applied Online ANN to fetch from its large ads inventory, which has brought double digits gains on ads quality metrics across surfaces. However, we are encountering challenges as the ads inventory continuously expands. It is imperative to maintain a neutral impact on online request latency and infra cost.
One potential solution to this issue involves improving the efficiency of the ANN algorithm. We have successfully migrated from the Hierarchical Navigable Small World (HNSW) algorithm to the Inverted File (IVF) algorithm. This transition enables the launch of a larger tier index capable of encompassing more than 10x the number of ads previously accommodated. Nevertheless, the associated cost increase remains a substantial concern, significantly restricting our ability to leverage the expanded inventory integrated into the index.
To address infrastructure costs while enhancing online efficiency, an alternative approach involves utilizing the Offline ANN. This approach benefits from the ample computational resources and latency tolerance available in batch processing environments. Specifically, this method proves most effective and efficient for candidate generators with static query contexts.
Architecture of Online/Offline ANN Retrieval
The following illustration describes the architecture of online and offline ANN retrieval.
The primary differentiation between the online and offline approaches is determined by the timing of the ANN search. In an online approach, the ANN search is executed in real-time as part of the immediate service. Conversely, in an offline approach, the ANN search is conducted within an offline workflow.
On the left side of online ANN architecture:
- Offline Phase: Index embeddings are built into the online serving index.
- Online Phase: The Ads Online Serving System creates ANN requests using real-time query embeddings, with the ANN search being conducted within the indexing systems.
On the right side of offline ANN architecture:
- Offline Phase: A list of query embeddings is prepared, and an ANN search is performed for each query embedding. The <key, ANN neighbors> results are stored in a data storage.
- Online Phase: The Ads Online Serving System retrieves results by looking up the storage using the key.
Pros of Offline ANN Architecture:
- Cost Efficiency: Infrastructure costs can be cut by up to 80%, primarily due to:
- Reduced lookup time for online storage compared to ANN search.
- Elimination of repetitive ANN searches per query embedding.
- Extensibility: Easier to extend to larger embedding sizes and implement more sophisticated ANN configurations and complex ranking models for top ANN neighbors.
Cons of Offline ANN Architecture:
- Real-Time Limitations: It lacks the ability to process queries in real-time. Unlike online ANN architecture, which can generate query embeddings on demand using user real-time data, offline ANN may struggle with immediate query result retrieval.
- Fixed Neighbors: The number of neighbors is predetermined and not adjustable online. This limitation can sometimes conflict with dynamic criteria such as ad bids or targeting. However, this can be mitigated by generating a surplus of neighbors.
Given the pros and cons, there are naturally best use-cases for offline ANN architecture and online ANN architecture.
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
It would be best to use offline ANN architecture:
- In environments with stable query context where real-time search processing is unnecessary.
- When low latency and reduced infrastructure costs are priorities.
It would be best to use online ANN architecture:
- For applications requiring real-time processing or where significant performance enhancements are needed for ANN search queries.
Pinterest Application
At Pinterest, we have extensively evaluated offline ANN-based retrieval in several different use-cases. In the next section, we will go over two different use cases.
Similar Item Ads
Context
Advertisers can set up ads to retarget a user’s offsite engaged items on Pinterest (depending on the user’s age, location and privacy settings), which is called dynamic retargeted ads. This type of ad usually shows very high engagement and conversion metrics. To utilize the strong performance of dynamic retargeted ads, we can use ANN to find items that are very similar to offsite engaged items and also show these similar item ads to users. We experimented with both offline ANN and online ANN and will share the implementation and result below.
Implementation
The online ANN version is very similar in architecture. We will go over offline ANN, as an example.
We implemented with two-step retrieval:
- Getting list<similar_item_id> during feature expansion
- Using list<similar_item_id> to construct a id based retrieval query to retrieve from an indexing system
Successful Metrics
The experiment result has shown that similar item ads also have high engagement and conversion performance. Compared with the online ANN version, offline ANN version has a much lower infra cost and better engagement and conversion performance.
Limitation & Solution
In offline ANN, the result was initially limited by the number of similar item ads retrieved and was very small, even though we increased the number of similar items per query to up to 50. After targeting, budget, and index size constraints, the number of retrieved ads is small.
We solve that by increasing indexing size. It is very cheap to run each retrieval query for this specific type of ID, so we can easily scale to a much larger index.
Visual Embedding
Context
To enhance the visual relevance of Pinterest ads, there are a couple of efforts utilized to incorporate visual embedding-based candidate generators across various surfaces and modules. These candidate generators employ the Online ANN approach, which has notably improved the advertisement relevance for their respective surfaces. To address the associated infra costs and facilitate the expansion of visual candidate generators to other surfaces, we are considering the offline approach for the reasons previously outlined.
Implementation
- Based on the historical engagement data, we get the head query Pins to calculate their nearest neighbor.
- In Offline ANN workflow, we store the nearest K neighbors prediction for each Pin from step 1.
- After we push the prediction to KV store, we expand the ANN prediction in an online request.
- We fetch back the Pin promotion candidates by ID-based exact match query.
Successful Metrics
- Recall: with the hyperparameter K finetuned, the offline ANN CG is able to fetch a similar number of candidates compared with online ANN CG.
- Precision: offline ANN CG shows on par performance on CTR while much higher gCTR30 compared with online ANN CG.
- Infra Cost: offline ANN CG shows less than 50% infra cost compared with online ANN solution.
Future Plan
The offline ANN method can be seamlessly extended to other interfaces, such as search and home feed, by leveraging the navboost Pin or cached Pin alongside the shared offline workflow.
Furthermore, Pinterest is actively developing its own offline ANN framework and platform, which will facilitate easier and more scalable future advancements. This initiative promises a wealth of new features, including index hyperparameter tuning and recall monitoring, ensuring a robust and adaptable development environment.
