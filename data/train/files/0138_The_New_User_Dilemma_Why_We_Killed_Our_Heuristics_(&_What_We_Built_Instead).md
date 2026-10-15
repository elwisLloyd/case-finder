# The New User Dilemma: Why We Killed Our Heuristics (& What We Built Instead)

Источник: https://medium.com/whatnot-engineering/the-new-user-dilemma-why-we-killed-our-heuristics-what-we-built-instead-0d7a834fda5f

The New User Dilemma: Why We Killed Our Heuristics (& What We Built Instead)
Miguel Fernandez-Montes Cuberta, David Kawashima, Ford Bohrmann | Feed and Personalization
TL;DR: Until recently, Whatnot’s personalized For You Feed used an ad-hoc heuristic to generate recommendations for new users. While effective, this approach missed out on the benefits from machine learning, required dedicated maintenance, and added complexity to our systems. Migrating new users to machine learning was the obvious path forward, but how exactly to do so wasn’t trivial. Consolidating feed ranking into one unified predictive model and adding new user input signals as features proved to be the right solution. Thanks to it, we achieved better recommendations for recent signups, reduced maintenance costs, and simplified our architecture.
Recommendations are crucial for a great user experience in a hyper-growth marketplace like Whatnot. Our crown jewel of recommendations is the For You Feed, which you can read about in our previous post.
For new users, recommendations are an especially challenging problem. Normally, we rely on a user’s past behavior to infer what content will be relevant to them. When a user has no history of interactions in the app, how can we serve them an exciting and relevant experience? This is what’s known as the cold-start problem.
Imagine this: you are an avid Pokemon card collector who also likes to occasionally shop for cool sneakers. You just signed up on Whatnot and told us a bit about what you like when onboarding onto the app. We don’t know much else about you but we want to provide you with a delightful experience the moment you land on your first For You Feed.
Historically, solving the cold-start problem at Whatnot relied on simple but effective heuristics. We decided to bid them farewell and usher in machine learning recommendations — with some great learnings along the way.
The Problem with Heuristics: when “Good Enough” isn’t Good Enough
So how were we handling the cold-start problem originally? Until recently, we considered new users a separate species for feed ranking. While feeds for regular users were ranked using predictions from machine learning models, feeds for new users were ranked with a rule-based system (aheuristic).
Our new user ranking heuristic was essentially a lookalike model, implemented through a complex mix of data pipelines. We grouped together new users with similar characteristics and inferred their preferred content based on historical engagement from users with those same characteristics. For example, we took recent signups who liked Pokemon cards and sneakers, and looked at aggregated summaries of the type of content they interacted with. When someone with the same preferences signed up, we would use these broad interaction summaries to recommend content to them.
This heuristic was able to deliver good enough results, but it was a far cry from a machine learning model. Besides, it had several disadvantages:
- Complex hand engineered logic: the lookalike logic mentioned above was designed through careful manual tweaking. Under the hood, our solution was fairly complex. This meant that it was complicated to grasp how each piece functioned, especially for engineers unfamiliar with it.
- Separation from the general feed ranking path: in the backend, new user feeds were generated following a completely different path from the regular feed generation. This includes retrieval, enrichments from key-value storage, applying business logic, filtering, sorting, etc. Monitoring and maintaining this path added significant load to our engineers’ bandwidth.
- Bespoke data assets: similarly, our heuristic approach relied on a bespoke set of orchestration jobs and datasets, requiring their own maintenance, subject matter expertise, and resources.
More importantly, new users are a critical segment for Whatnot, so why should ranking for them not be on par with ranking for mature users?
The Obvious Solution: Machine Learning
Some time ago, we transitioned our general population feed ranking from batch to online inference, unlocking significant performance gains. Online inference promised to solve our challenges for new users, too:
- Unlike heuristics, machine learning models directly learn patterns in the data. Instead of manually constructing user lookalikes and estimating their preferences, a predictive model can be directly trained to optimize an objective function.
- With online inference (as opposed to batch inference), we no longer need to have users in our offline warehouse to make predictions for them. This means we can generate predictions for new users “on the fly”.
- In addition, moving to ML-based ranking for new users meant we could get rid of all those high maintenance datasets and pipelines.
Not So Fast: Roadblocks and Dilemmas
While ML seemed like the obvious solution to improve new user recommendations, we bumped into some tricky problems.
First, while we wanted to use a machine learning model, it was not obvious how to model this use case. Should we build an ad-hoc recommendations model, trained exclusively on new user data? Or should we completely unify new and old user’s recommendations logic with one big model?
Get Whatnot Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
Second, despite the wonders of online inference, the cold-start problem was still… a problem. New users have no history in the app and our existing predictive model relied heavily on features built from past user interactions, which simply don’t exist for recent signups.
The Not-So-Obvious Solution: One Model, More Features
One Model to Rule Them All
Dealing with the first problem (one big model vs a new user model) meant weighing a set of pros and cons that looked more or less like this:
As you can see, there are good a priori arguments for both a tailored new user model and a single global model, but how the models perform would end up being the key factor. Offline model evaluation helped us make a decision, with an interesting conclusion: a global model trained on all data performed better than a model trained only on new users. Our hypotheses behind why a single ranking model worked well are:
- Gradient boosted decision trees (GBDT), which are the type of model we use, are high-performing models even with skewed data distributions. New user examples represent a small percentage of all training examples, but GBDT are still able to fit their decision rules to those small “pockets” of data.
- A global model trained on full population data can better learn patterns from all users that might transfer well to new users.
- There is no exact rule to determine when a new user becomes a “mature” user. In some cases, users with short tenures will have enough interactions to inform recommendations. In others, longer tenured users will still look like fairly recent signups. With a global model for users of all tenures, we let the model itself figure out which signals to rely on for the best recommendations.
Given these positive offline evaluation results, we decided to go for one global ranking model and, as a bonus, reap the maintenance benefits of this unified approach.
Features at Request Time
In the absence of historical user interactions, we had to rely on the few pieces of information that users provide when they sign up e.g. the categories they are interested in. However, using onboarding selections as features in our production online inference system was not trivial. We needed to ensure that:
- Features are available at request time. Unlike historical activity features, which are managed by and stored in our feature store, these new user signals have to be supplied to the model directly from the client
- Features are available for training. Models have to be trained with the new features to learn the relationship between them and the model’s target
- And most importantly: both request time features and training features have to match
In any ML system, training-production parity is critical. We want to make sure that our deployed models are receiving data from roughly the same distribution as the one seen during training.
Training-production parity for pre-computed aggregated features is provided by our feature store, Chalk
- Chalk stores and keeps track of the features available for online consumption at any given time
- When creating training data offline, it guarantees point-in-time correctness of the features added to our training set
- Training-production parity for features that are passed to the model in the request is a different story
These features are not stored in Chalk
- Instead, they have to be added to our training data in a different way that also guarantees point-in-time correctness. We rely on database Change Data Capture (CDC) to our offline data warehouse
- With appropriate data joins using CDC timestamps we can guarantee consistency for these features
On top of ensuring training-production feature parity, we designed a general framework so that our online inference system could accept and validate arbitrary features supplied in the request. This pattern allows us to use other request-based features in the future.
Results: better recommendations, less tech debt and a tide that lifts all boats
Launching online inference feed ranking for new users was a success. For You Feed engagement from new users increased by 10%. When A/B testing against the prior system, the positive effect in these metrics was measured with high statistical significance, giving us confidence in the benefits from our unified ML solution.
Besides these performance gains, we were able to get rid of a lot of technical debt and maintenance costs. We no longer need to maintain a separate set of data pipelines or a bespoke feed generation path in the backend, which required their own monitoring and relied on siloed knowledge.
Finally, by consolidating feed ranking into one unified architecture we ensured that future ML improvements are a “tide that lifts all boats”. One of these improvements is capturing near real time app activity. Whatnot is different from traditional marketplaces because supply changes rapidly depending on which shows are live.The Feed & Personalization team has been focused on capturing these dynamics to provide even better recommendations. With a unified feed ranking system this will have a much broader impact, helping out old time Whatnot veterans as well as users who are brand new to the platform. Stay tuned to hear more in an upcoming post!
If you enjoyed learning about our experience getting new users onto ML models for feed ranking, and you are interested in exciting challenges at a rapidly growing marketplace, check out our career opportunities!
