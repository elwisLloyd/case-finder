# NEP: Notification System and Relevance

Источник: https://medium.com/pinterest-engineering/nep-notification-system-and-relevance-a7fff21986c7

Lin Zhu; Staff Machine Learning Engineer | Eric Tam; Staff Software Engineer | Yuxiang Wang; Staff Machine Learning Engineer |
Importance of Notifications
Notifications (e.g. email, push, in-app messages) play an important role in driving user retention. In our previous system, which operated on a daily budget allocation model, the system relied on predicting daily budgets for individual users on a daily basis, constraining the flexibility and responsiveness required for dynamic user engagement and content changes. Notification Event Processor (NEP) is a next generation notification system developed at Pinterest, offering the flexibility to process and make decisions to send notifications in near real-time. By harnessing the power of machine learning, NEP determines various factors for sending notifications, such as content selection, recipient targeting, channel preferences, and optimal timing. The implementation of this system resulted in significant improvements in user email and push engagement metrics and weekly active user (WAU) growth.
NEP System
Goals and Rationale Behind the Project
- Expand types of notifications that support different functionalities across Pinterest
- Better real-time notification processing capabilities
- Dynamic and holistic control of the volume and send time of notifications
- Personalization on notifications user receives
- Reduce the number of irrelevant or unhelpful notifications
Design goals:
- Given a stream of notification candidate events, optimize notification experience by controlling:
- Frequency (less irrelevant notifications)
- Channel selection (Email vs. Push vs. In-App)
- Delivery time
- Aggregation (pool events until ready for notification)
- Holistically control a diverse set of notification types (e.g. Real-time activities, Content Recommendation, Updates from people you follow)
- Drive different objectives for different segments of users (e.g. Idea Pin engagement for Core users, WAC for Creators, etc.)
- Ensure onboarding new event types is easy for client Product teams
High-level Design
All NEP processing occurs in streaming fashion using Pinterest internal Pacer system. When an event is processed, it kicks off a Pacer job that is responsible for processing the events and making send decisions. Figure 1 below shows the overview of the system architecture.
- If ranking is not needed, a notification is either sent immediately or scheduled after filtering and channel selection.
- If ranking is needed, the event is first processed and written to the Event Pool, then the Event Ranker job is scheduled to rank user’s all existing events, and finally the Policy layer selects channels and makes send decisions.
Modeling High-level Components
The NEP model focuses on determining what to send, to whom, through which channel, at what time, and how to prioritize content. Here are the key modeling changes we made:
- Relax eligibility rules: users can be processed in the NEP system as long as they are opted in and reachable.
- Introduce daily candidate generation approach, facilitating the inclusion of more high-quality notification candidates with reasonable infrastructure costs.
- Employ Pin Ranker to rerank the content (Pins/boards/queries) in each notification candidate.
- Implement the NEP ranker, a multi-head model that predicts Pinner’s engagement probabilities such as push open, email click, and unsub. The model utilizes advanced architecture and rich features to enhance its effectiveness and content targeting.
- Introduce the Policy layer as the notification send decision-making component, which takes input from the NEP ranker model, current time, and determines the appropriate channel for delivery.
Notification Candidate Generation
In the NEP system, we pre-generate notification candidates/events for every push or email eligible user every day and store the events into the event pool. Event pool is a KV store storing the candidate events for each user. NEP Ranker Job will be scheduled multiple times a day at each user’s best delivery time slots according to user’s historical engagements. The job will take the events from the event pool, make model predictions, and decide whether to send it or not.
In order to save infra cost on iterating over all possible candidate sources, we apply optimization based on historical candidate availability from that type.
NEP Model & Policy
Data/Labels
Data Collection
We logged NEP data in different ways for different purposes.
- Production sent notification logging: randomly logs 10% of sent notifications, it has a large volume, mainly used for model training.
- Random data (1%): used for evaluation and policy tuning.
- random send: randomly select an event to send (0.5%).
- greedy send: force send the top ranked event regardless of scores (0.25%).
- greedy no send: force not send any notification within the next 24h (0.25%).
- User level logging: log all the event scoring history for 1% users, tracking all the sends/no-send decisions.
- Engagement time logging: data logged when users click emails or open push (all positives).
We applied negative downsampling on engagement labels and unsub labels. Since we have both push and email records in training data, during training we are forced to disabled email records to train push related heads and vice versa.
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
Labels
We consider three types of labels for model predictions:
- Engagement labels: push open, email click, etc.
- Session labels: user number of sessions within 1h, 1d, 3d, etc. after notification sent.
- Unsubscribe labels: email unsubscribe, push disabled, app delete, etc.
Features
- Content Signals: notification type, Pin embedding, notification event embedding, Pin historical engagement, etc.
- User Signals: user state, preference, aggregation of historical engagements across different time windows, engagements across different notification types, etc.
- User Sequences: user Pin engagement sequence, notification send sequence, and user notification engagement sequence.
- Delivery Time: request time as features, aggregated engagements in each hour of the week.
Modeling
- Multi-task model: We employed multi-task model architecture with a focus on information sharing and reducing inference cost.
- Sequence transformer: We applied a transformer to generate a representation from user sequences. This transformer is specifically designed to derive meaningful representations from user sequences, enhancing the model’s understanding of temporal patterns and context within the data.
- Transformer mixer: The transformer mixer plays a crucial role in this architecture by integrating transformer-based mechanisms to facilitate cross-feature learning.
Policy
Policy component is responsible for making notification send decisions. We calculate the linear utility for each notification event, then it makes email and push send decisions separately based on the utility scores. Figure 4 demonstrates the process: if the utility score is bigger than the per user segment threshold, we will send immediately; otherwise, we don’t send anything. We built a PID controller to tune the thresholds to guarantee daily send volume. We calculate the offline metrics based on utility ranking; however, testing different w in production usually gives us better sense.
Volume Alignment Using PID Controller
The threshold is crucial to decide overall notification send volume. If the threshold is too small, we will send more notifications to users; if the threshold is too large, we will send less notifications to users. We have different thresholds set for different user groups segmented by user activeness, and the volume is impacted on the timing and fatigue logics. It’s not possible to manually tune the thresholds, and it’s not accurate running offline replay to mimic online streaming decisions. As a result, we developed an automatic threshold tuning system using a PID controller to align the notification volume. We simplify the PID formula below for ease of use:
f(t) is target volume, p(t) is the actual volume, c(t) is the threshold at time t, and i is a tunable hyper parameter. In order to prevent the exploding gradient issue, we also introduce the learning_rate parameter, the final formula shows below:
Figure 5 shows the send volume between control and enabled groups are getting aligned soon after turning on the PID controller at 2PM.
Serving
The model is served in real-time fashion. We don’t have strict limitations on the scoring latency, but we need to make sure the throughput could satisfy our system requirements.
- We cache user features at send time while retrieving the cache at engagement time for logging in order to ensure feature consistency. Pin features are not cached as they change less frequently.
- Unity is our asynchronous framework that handles resource fetching, request understanding, and service calls.
- We use a GPU cluster for low latency and high throughput inference; we use CUDA graphs to reduce overhead on model serving; low-precision model serving is on the roadmap.
Experiment Results
This is a fundamental system change from an offline daily budgeting system to a streaming notification system. We tried to align current production behaviors and launched more than 100 experiment groups to test different models and tune parameters. The final launched experiment group shows large user email and push engagement lift and significant WAU gains. However, we also see unsubscribes increased, which is mainly due to sending more notifications to new users.
Acknowledgement
We’d like to thank Dimitra Tsiaousi, Arun Nedunchezhian, Hongtao Lin, Yiling He, Tianqi Wang, Anya Trivedi, Kevin Che, Grant Li, Fangzheng Tian, Justin Tran for their contribution.
Thanks Jiaqing Zhao, Robert Paine, Nikil Pancha, Ying Huang, Yang Yang, Kevin Kim, Olafur Gudmundsson, Bee-Chung Chen and Andrew Zhai for technical discussions.
Thanks managers Xing Wei, Tingting Zhu, Ravi Kiran Holur Vijay, Pradheep Elango, Ben Garrett, Koichiro Narita and Rajat Raina for the support.
To learn more about engineering at Pinterest, check out the rest of our Engineering Blog and visit our Pinterest Labs site. To explore and apply to open roles, visit our Careers page.
