# Module Relevance on Home Feed

Источник: https://medium.com/pinterest-engineering/module-relevance-on-homefeed-ae76f8b545b2

Usha Amrutha Nookala, Jason Madeano, Siddarth Malreddy, Lucy Song, Alekhya P
In the past, home feed on Pinterest recommended a grid of Pins that are most relevant to a user. The grid limits our ability to provide more context on the recommendations as well as show new topics the user might be interested in. To address this, we introduced modules to the home feed. We developed several components to ensure that the user’s home feed remains relevant with this new content type. This blog post details these components. The figure below provides an overview of our system and demonstrates how it interacts with the existing main feed of Pins.
Modules
Modules are a new content format that gives Pinners more context about their feed content and more ways to explore topics. Modules are heterogenous, with variations in UI and content based on factors like topics, boards, recent engagement, and shopping interests. We broadly have two types of modules:
- Landing page modules: In this type of modules, tapping on the module takes the user to a separate landing page with Pins the user can interact with.
- Carousel modules: This type of module is a collection of Pins in the horizontal shelf on the feed that are shown to the user.
Modules on home feed (HF) can give Pinners greater control of their browsing and more context about their recommendations, but new modules need to compete with the highly optimized HF grid. The HF Module Relevance Platform aims to dynamically blend modules and Pins to better optimize each Pinner’s HF experience. In the subsequent sections, we touch upon important components of Module Relevance Platform.
Module Fatiguing
When adding modules to the feed, the new content displaces the existing Pins. This made it hard to launch new modules to the platform without taking a hit on core company metrics. We were able to resolve this by introducing module fatiguing.
Fatiguing is underpinned by a simple idea: If a particular user has seen a particular module many times without interacting with it, we should (at least temporarily) stop showing that module to that user. We achieved this by running a daily workflow that aggregates each user’s historical module engagement with a focus on the number of impressions since the user’s last click on the module. If, over the past n days, the number of impressions without a click was above some threshold k, then that module would be hidden for that user for d days.
While this heuristic-based fatiguing approach is simple in theory, it was very effective in practice and directly enabled the launch of the first few modules on home feed by enabling personalization before any other relevance components were introduced.
However, as the module ecosystem grew, fatiguing was not sufficient for three main reasons.
- Fatiguing decides whether or not to show a module but does not inform how or where to show a module within a feed.
- Simple, heuristic-based fatiguing is not sufficiently granular as it only works at the module-type level. For example, for a particular shopping module type that displays shoppable clothing content, the user may like it when the module shows shoes but not when it shows hats.
- The fatiguing signal is not real-time, meaning that it was not sufficiently responsive.
As we continued building the module ecosystem, we invested in better signals to help with point number 3, but the first two points required building entirely new relevance components such as a module ranking and module blending.
Module Ranking
The module ranker deals with ranking modules amongst each other so the most relevant modules are shown higher on the page. We started with a heuristic-based approach while leveraging existing components before building a dedicated ranking model.
Baseline Approach
We used home feed’s Pin Ranking model for ranking modules. For each module, we take the first four cover Pins and score them with the production Pin Ranking model. The module score is computed as the maximum of the calibrated save scores across those four cover Pins. We rank the modules based on this score. Then we filter “low quality” modules. By default, we filter modules with scores lower than x percentile, but some modules have their own filtering thresholds that overrides this default.
Deep Ranking Model
The off-the-shelf Pin Ranking model is already a large and complex model, and it serves a very important role in HF pin ranking. This makes it very difficult to make adjustments directly to the HF Pin ranker to improve module ranking performance. Furthermore, the Pin Ranker does not take into consideration the user-module engagement, thereby making it difficult to personalize the module distribution to Pinners.
So, we built a dedicated module ranking model that is trained on user engagement data on modules. Whereas the pin ranking-based scoring approach only considers module cover Pins, the dedicated ranker has a much more comprehensive feature set of modules and users. This also enables a feedback loop between user and module engagement and improves the module distribution.
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
The Module Ranker is a multi-head model optimizing for module actions such as module taps, Pin clicks on the carousel/landing page, and saves on the carousel/landing page. Those positive actions are mapped to binary labels, and we use binary cross entropy loss for optimization during the training process.
Sampling Strategy
We retain all positive labels leading to module engagement and impressions are downsampled in order to maintain a balance between positive and negative labels.
Selected Features
Module Features
- Aggregated (both overall + per user) features such as taps, impressions, repins, closeup, and click/long click across one, seven, and 28 day windows per module type
- Module Title embedding(s), Module Type, UI type
- Cover images Pin Ranker Predictions
- Various pretrained embeddings widely used in Pinterest — encoding information related to visual information, shopping intent, Pin representations, and other onsite signals — of the first four cover Pins of the Module
User Features
- Viewer engagement features
- Viewer characteristics (such as gender, language, user state) and Context features
Calibration
Since we downsample impressions, we need a calibration layer to map the predicted scores to empirical rates. The calibration training window with dates/data are distinct from normal model training. The calibrated scores are explainable and are further used in the blending layer to dynamically place modules on HF.
Utility
We combined the predictions from these multiple heads to get a single score used to rank the modules. Given business insights about the relative importance of each action along with offline and online tuning, we determine a utility value that is a weighted sum of all prediction scores from the module ranker.
Once we have the scores for each module from the module ranker, Module Blending decides how we dynamically blend modules and Pins together to generate the feed.
Module Blending
Our initial approach placed ordered modules in static fixed slots within the feed (such as 15, 35, 55, 75), regardless of the surrounding Pins. This could cannibalize home feed user engagement by potentially replacing a highly engaging Pin with a Module. To address this, our ‘skip slot’ approach dynamically blends Pins and Modules, ensuring a Module only replaces a Pin if its predicted engagement is higher.
Skip-slot Blending
Skip-slot Blending aims to dynamically place modules in the feed based on the predicted engagement of the surrounding Pins. To achieve this, we computed an Pin Utility score for each Pin using the outputs of the Pin ranker:
Comparison Function
Our comparison function simply checked for the greater of the two, along with a weighting coefficient.
In theory, wₚ could be distributed to the other weight terms to reduce the number of weights, but the weight is useful for tuning in practice (i.e. it determines how much preference to give modules versus pins). The weight is also useful if the number of terms on each side of the equation and/or the score distributions between the module ranker and the Pin ranker are not sufficiently similar.
Modules are blended in the feed based on the predicted engagement of surrounding Pins. We order the modules based on their Module Utility score from the module ranker. Before placing a module at slot s, we check whether the Module Utility score > weight_coefficient times the Pin Utility score of the Pin at that slot. If the module score is higher, we place the module. Otherwise, we repeat the check k slots lower. We repeat this process until all modules have been placed or there are no more slots remaining. This naturally allows us to move modules with lower scores further down in the feed (or remove them entirely).
Future Plans
As we rolled out these systems in production, we developed a broad set of real-time monitoring metrics to monitor the health of the Module Platform. We plan to iterate on these components to further improve relevance by using magnitude-based ranking/blending and Pin displacement based blending.
Acknowledgement
We would like to thank the home feed relevance and product teams for their support: Lianghao Chen, Matt Chun, Felix Zhou, Xinyuan Gui, Dhruvil Deven Badani, Jesse Andersen, AJ Oxendine, Yujiao Guo, Sarah Tao, Megan Blake, Jennifer Kong, Hanfei Ren, Minely Pereyra Rodriguez, Moises Antonio Hernandez Lopez, Jonatan Luna, Dylan Wang
