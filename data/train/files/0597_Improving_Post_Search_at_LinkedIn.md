# Improving Post Search at LinkedIn

Источник: https://engineering.linkedin.com/blog/2022/improving-post-search-at-linkedin

Co-authors: Amol Chandla, Jagadeesan Sundaresan, Siddharth Pratap Singh, Saipriya Kumar, and Anand Kishore
At LinkedIn Search, we strive to serve results that are most relevant to a member’s query, from a wide variety of verticals such as jobs they may be interested in, people they may want to connect with, or posts that are trending within their industry. Post search saw strong organic growth in 2020, with a 35% year-over-year increase in user engagement. As we watched content continue to grow and diversify on the platform, the Flagship Search team saw an opportunity to improve the Post search tech stack’s agility, with a strategic priority to enable members to create, find, share, and have productive conversations around high-quality content on LinkedIn.
The Post search tech stack was originally built on top of the well-established Feed systems and services and leveraged the Feed platform. Removing the unnecessary dependency on Feed systems and simplifying our stack allowed us to successfully leverage several machine learning (ML) techniques and improve the relevance of Post search results while providing a superior member experience. This blog post outlines our journey as we re-architected the Post search stack and describes how we addressed many of the unique challenges faced along the way.
Background
The life of a search query at LinkedIn begins in a search bar, which interacts with a frontend presentation layer that fetches the search results from a midtier service and decorates them for the best member experience.
The search midtier at LinkedIn follows the federated search pattern: it fans out calls to various search backends and blends the results together. The Post search stack, however, is different, as it was designed to be compatible with the Feed ecosystem at LinkedIn. For Post search, the fanout and blending logic depended on Feed services, including feed-mixer and interest-discovery.
Figure 1. View of the Search stack before simplification
Apart from the different service architecture, Post search also uses an intermediate language called Interest Query Language (IQL) to translate a user query into index-specific queries used to serve search results. At the time of its inception, Post search was served by two search indexes, one for posts that you see on the Feed and one for articles. However, as more content types were supported at LinkedIn over time, it was easier to augment the existing Post index instead of adding a new index each time.
Due to the complex architecture, increasing our development and experimentation velocity proved to be difficult, as any search relevance or feature improvements required changes to multiple points throughout the stack. It was challenging to address many of the unique needs of Post search, such as balancing multiple aspects of relevance, ensuring diversity of results, and supporting other product requirements.
Our approach
Simplifying system architecture
We set out to simplify the system architecture to improve productivity and facilitate faster relevance iterations. To achieve this, we decided to decouple the Feed and Post search services in two phases. The first phase removed feed-mixer from the call stack and moved fanout and blending into the search federator. The second phase removed interest-discovery. This enabled us to get rid of all the cruft built up over the years and simplified the stack by removing additional layers of data manipulation.
Figure 2. Phased approach to simplify the stack
Improving Post search relevance
As we thought about ways to improve the relevance of results from Post search, we realized that the user’s perceived relevance of results is a delicate balance of several orthogonal aspects, such as:
- Query-document relevance
- Query-agnostic document quality (i.e., static rank)
- Personalization and user intent understanding
- Post engagement
- Post freshness/recency (especially for trending topics)
In addition to those aspects, we wanted to easily implement other requirements from our product partners to satisfy searcher expectations (e.g., ensuring diversity of results, promoting serendipitous discovery, etc.). To meet these goals for post relevance, we implemented a new ML-powered system; the high-level architecture is shown in Figure 3, and we'll cover the details in the remainder of this section.
Figure 3. Design of our ML system
As a single, unified model did not scale well for our needs, we invested in modeling the First Pass Ranker (FPR) as a multi-aspect model, wherein each aspect is optimized through an independent ML model. As a FPR typically scans a large number of documents with the goal of optimizing for recall, latency constraints require the aspect models to be lightweight (e.g., gradient boosted decision trees). We combine the scores from all these aspect models in a separate layer to determine the final score for ranking. This approach enables us to:
- Have separation of concerns for each aspect
- Decouple modeling iterations for each aspect
- Add more explainability to our ranking
- Control the importance of each aspect based on product requirements
With the re-architecture of the stack, we were able to easily launch two additional layers of re-ranking on top of the FPR: Second Pass Ranker (SPR) and Diversity re-ranker. SPR, which resides in the federation layer and can support complex ML model architectures (e.g., neural nets), is geared toward improving precision and ranks the top k documents returned from the FPR. It enables personalization by leveraging deeper and real-time signals for members' intent, interests, and affinities. The Diversity re-ranker forms our last layer and helps us inject diverse content in the top k positions. This includes increasing discovery of potentially viral content for trending queries, reducing duplication of similar content, etc.
To iterate quickly on a multi-layered, complex ML stack, testing and validation was a foundational piece we had to get right. We built a suite of internal tools to assess the quality of new candidate models and quantify how they differed from the current production model. This enabled us to have a principled approach to testing relevance changes and ensured we did not regress on the core functionality/user experience.
- Pre-ramp evaluation: This tool helps compute and plot descriptive statistics for the results of a collection of user queries to test and validate intended effects. For example, we are able to validate how we changed the distribution of recent posts in the results for our experiments. This helps us to understand our models better before ramping any change to members and to catch any unintended side effects early on.
- Validating table stakes: The Build Verification Tool (BVT) helps generate model reliability tests to assert if a specific expected document is correctly surfaced for a certain queries and members. For example, using this tool, we can validate if certain table stakes—like searching for an exact match using quoted phrase queries— are not regressing with any of our improvements.
- Human evaluation: To have a better understanding of basic query-document relevance, we invested heavily in crowdsourcing human ratings for the search results. We leverage this crowdsourced data to evaluate performance of offline ranking models with respect to search quality, to ensure it meets the basic quality bar. Crowdsourced human annotation data also provides valuable training data to improve the ranking of results.
Results
These changes to the system architecture have helped us unlock several wins, such as:
- Developer productivity: We reduced the developer effort to add new features from 6 weeks to 2 weeks. Additional productivity wins include faster developer onboarding time and lower maintenance costs.
- Latency: Already, we’ve seen P90 latency reduced by ~62ms for Android, ~34ms for iOS, and ~30ms for web. We expect additional latency reductions from future work as well.
- Leverage: Because search federation was already integrated with newer machine learning technologies, this migration has also empowered relevance engineers to iterate faster and run more experiments to improve the Post search results.
- End-to-end optimization: With the extra layers removed, search federator now has access to all the Post-related metadata from the index. This data is being used to improve the ranking of posts when blended with other types of results, help reduce duplication, and increase the diversity of content.
- Engaging and personalized results: Pertinent results, which are highly relevant to the user’s search query, have led to an aggregate click-through rate improvement of over 10%. Increased distribution of posts from within the searcher’s social network, their geographic location, and in their preferred language have led to a 20% increase in messaging within the searcher’s network.
- Superior navigational capabilities: Better navigation allows members to search for posts from a specific author, for posts that match quoted queries, for recently viewed posts, and more, leading to an increase in user satisfaction, reflected by a 20% increase in positive feedback rate.
| Metric | Impact | 
| Click through rate on Posts cluster | +6.2% | 
| Messages originating from Posts search | +21% | 
| Overall session success rate | +0.15% | 
Table 1. Impact of the first ML model using performant min-span featuresw
| Metric | Impact | 
| User engagement (Likes, Reacts, Comments, Shares) | +5.4% | 
| Total downstream member actions converted from Post search | +5.3% | 
| Positive explicit feedback rate | +19.8% | 
Table 2. Impact of combined model including multiple aspects such as Engagement, Personalization (In-Network, Geo), and Quality
Limitations and future work
Although our current solution has been a huge improvement, we acknowledge its limitations and plan to address them in our future work. Some of the areas we’ll focus on include:
- Further simplify: Removing IQL from the stack will help remove two layers of query translation from the flow, making it much easier to add new, useful filters for Post search. To do this, we plan to merge all of the Post search backend and translate directly from the member query to the Galene query.
- Semantic understanding: We will be investing in Natural Language Processing (NLP) capabilities to understand the deeper semantic meaning of queries. We plan to implement Embedding Based Retrieval (EBR) and use DeText embeddings in our neural network-based SPR model.
- Detect trending content: To quickly detect trending, newsy, or viral content on our platform and surface fresh results for queries on trending topics, we plan to use a real-time platform for computing engagement features to reduce the feedback loop from hours to minutes.
- Promoting creators: Results are ranked today mainly by using viewer-side utility functions such as likelihood of a click, user action originating from search, etc. To support our creators, we will evolve this ranking, along with our experimentation and testing stack to also optimize for creator-side utilities, such as content creation or distribution for emerging creators.
- Multimedia understanding: Expanding our document understanding capabilities beyond text data to include handling multimedia content such as images, short-form videos, and audio, is another opportunity for future investment. As web content becomes increasingly diverse and newer content formats become popular, it will be important to ensure these content types are easily discoverable on Post search.
We would like to conclude with a reminder to our readers that in large complex systems, the existing state can be suboptimal due to incremental solutions to problems over time. By stepping back and taking a high level view, it is possible to identify several areas of improvement, as we have shared in this blog. It takes an open mind and support from engineering, product, and leadership to entertain these improvements, but in the end, your users and fellow engineers will thank you. Please share any similar experiences from your work, and reach out to us if you have any questions or just want to chat about how we broke the status quo.
Acknowledgements
We would like to thank the following teams and individuals involved for their support: Search Apps Infra, Flagship Search AI, Search Federation, Feed Infra, Discover AI, Verticals and Platform, Search SRE, Bef Ayenew, Rashmi Jain, Abhimanyu Lad, Catherine Xu, Alice Xiong, Steven Chow, Lexi He, Margaret Sobota, Xin Yang, Justin Zhang, David Golland, Sean Henderson, Pete Merkouris, and many more.
Related articles
