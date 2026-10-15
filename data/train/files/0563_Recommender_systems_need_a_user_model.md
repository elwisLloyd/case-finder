# Recommender systems need a user model

Источник: https://medium.com/criteo-engineering/recommender-systems-need-a-user-model-c3b3790311bf

Co-author: Flavian Vasile
In this blog post, we elaborate on the observation that recommender systems rely on unstated user choice models. We argue that making those models explicit and studying their characteristics could be insightful and unlock new approaches. We propose some guidelines to specify such models.
This post provides motivation for doing RecSys research with the user’s perspective in mind. Instead of approaching the Recommender System problem as a pattern recognition task, we should instead view it as a task of figuring out the user’s preferences and then giving them the best browsing experience. Because we aim at modeling its short-term effects, we will not include the effects of the RecSys on the evolution of users’ preferences.
RecSys current state of affair
Recommender Systems (or, for short, RecSys) are a core component of the digital economy. Surprisingly, the question of how they affect people is not as studied as it would be expected. A simple answer to this question is that they help people decide what to browse, read, watch, listen to, follow, and buy. But such an answer isn’t really satisfying. First, it doesn’t tell us how this help is supplied. Second, it is hard to come up with an experiment to prove a claim of this nature. Indeed, being a good assistant isn’t something that can easily be distilled into a mathematical formula.
This post discusses a narrower, but more workable, version of the question: How can a recommender system change a user decision? (NB for the scope of this post, we will not be concerned with the long-term effects of RecSys on user preferences, neither will we be asking how much a RecSys can change a user decision — we are still a few steps away from that.)
Ongoing research work
A lot of research has been done on how to design recommender systems that guess what the user might do next or what the user might like, following a recommendation as auto-complete philosophy [1,2]. This body of literature is mostly built on approaches coming from Machine Learning and Information Retrieval [1,2,3,4].
There is also a recent trend of bandit-signal recommendation [5,6,7], fuelled by reinforcement learning [8,9] and causality theory [10], that departs from the traditional pattern recognition perspective. One reason for embracing the new approach comes from the discrepancy between offline and online metrics that occurs when employing traditional RecSys approaches. However, while addressing the offline — online alignment issue, bandit reco is still mostly about building black-box recommender systems. These systems are able to optimise for a given user feedback, such as clicks or conversions, in the absence of an explicit model of what is driving the desired user reaction.
In other words, bandit reco models are not user models, and while they provide us with a way to operate in an unpredictable environment that reacts to our actions (aka the system users), the laws of the environment (users) are seen as a black-box.
One framework to explain them all
This post is not meant to argue against the merits of reinforcement learning and causality-based recsys, but to suggest a complementary approach that would consist of opening the black box. If we look closer, it becomes apparent that most recommender systems do operate with an implicit user choice model in mind, but that the model is rarely specified. We believe that specifying the user choice model is a research effort worth pursuing because it would bring many benefits:
- First, this could be an opportunity to create a unifying framework that would cover the many models developed by the RecSys community and help build a general theory. For instance, if we are allowed to make some assumptions about the user, then we could be able to expect additional theoretical guarantees.
- Second, we can reasonably hope to get a deeper understanding of the relation between offline and online metrics by specifying the user behavior. By stating our assumptions in a way that can be tested, we can improve our understanding of user behaviour and recommender systems through experiments. Moreover, it is possible that a set of user behaviour models could serve as unit tests for testing the limitations of RecSys models/metrics. For example, it could help predict what could go wrong when moving from offline analysis to online A/B test.
- Third, we could start explaining the incremental effect of recommendation and performance advertising on consumption. By opening the black box of user behaviour, we can compare this behaviour both in the presence and in the absence of recommendations and highlight the sources of added value and the mechanism by which this is obtained.
- Fourth, this is a path towards bridging RecSys, econometrics and mechanism design. Indeed, in typical applications, several actors (such as the user, the platform, the website, the merchants, the advertisers, the media producers, etc.) have conflicting objectives for the user’s choices. A research program like this will be important for fully addressing the ethical, business, and economic issues raised by recommender systems.
- Fifth, it is a way to bridge RecSys, simulations, and reinforcement learning since a reasonable understanding of user behaviour will bring a more granular, first principle way to build simulation environments.
A basic user model proposal
For our proposal, we argue that the user gravitates around two major activities:
- gathering information around the (shopping, watching,…) options
- ranking the options based on the gathered information
As such, it seems natural to decompose user’s behaviour into two distinct policies:
- the browsing policy, which corresponds to the user looking for information, and
- the consumption policy, which shall be responsible for the user conversion process
Note that the decomposition of the behaviour into two separate policies is made purely for conceptual simplicity, as it allows distinguishing browsing, which requires a sustained research effort and is time-intensive, and deciding/converting, that is relatively instantaneous and that (we assume) produces an immediate observable reward.
As a simple extension, we can bring user’s rationality into the model by supposing that the two policies are optimizing a utility function. Furthermore, to account for the users’ heterogeneity in shopping preferences, the users can be allocated a private type, unobserved by the RecSys, which could be used as a policy parameter. While such private types are by construction not observable, they could be modeled, for instance, using a Bayesian prior.
The recommender system’s added-value
Now we are ready to identify two important contributions of the recommender system to the user’s decision:
- the “shortcut effect”, where recommendations help the user navigate faster by providing them links toward what they are looking for
- the “information effect”, where recommendations help drive the user’s attention to a given piece of information. For example, the RecSys can:
(a) make the user aware of the existence of new items
(b) make the user aware of the existence of additional features belonging to known items
Get Benjamin Heymann’s stories in your inbox
Join Medium for free to get updates from this writer.
(c) remind the user of the existence of some items (if assume the user is forgetful)
In terms of economic utility, the two recommendation effects on user behaviour have different impacts:
- the “shortcut effect” reduces the frictions. For instance for e-commerce, it switches — through facilitation — from the default “no buy” to a “buy” decision.
- the “information effect” changes the utility computation for the user and, as a result, changes the final ranking of the products. This is a net positive for a rational user, since expanding the information available should always lead to a better choice for the user.
Relationship with the incrementality of advertising
We can see that, under this model, personalization is tightly related to incrementality. The added value of a Recommender System is the extra user utility produced by switching borderline no_buy decisions to buys by removing the access friction and by switching the default buying option to the recommended option. This additional utility corresponds to the incremental value of recommendation / advertising over the status quo.
Example: the user’s perspective in a bookshop
Now, to make these effects clearer, let’s take an example:
Let’s assume that we need to decide whether to buy the last novel by George Martin, or to buy a comic:
Step 1: The Recommendation System displays a slate with multiple items and additional information, namely:
- The recommender system informs us that the latest George Martin novel got a 5-out-of-5 rating (case 2.b: new item feature effect).
- It also shows us the cover of a classic comic we might like. We realize that we do not know it (case 2.a: new item effect).
Step 2: We decide to click on it and read the classic comic synopsis.
Step 3: We don’t really like it, so we decide to buy the novel by George Martin. We write the name of the author in the search bar, and the last novel appears second in the results (case 1: shortcut effect).
Step 4: We click on the search result and land on the novel page, we see a banner for Dune, another novel that we forgot we wanted to read (case 2.c: reminder effect).
Step 5: We click on the banner and buy this novel.
Final words
Echoing economist Jack Hirshleifer’s words, “Information is of value only if it can affect action” [11,12], we underscore the role of Recommender Systems in shaping user behavior through informed choices. Recommender Systems are not merely about predicting behavior or matching products with users; they are about comprehending the complexity of user decision-making.
Looking towards the future of recommender systems, we envision the potential impact of conversational AI. Indeed, chatbots can efficiently gather and present information around shopping options and recommender system designers can make explicit the division between “shortcut effect” and “information effect”. The potential integration of advanced AI holds promise for transforming user interactions and leveraging user choice models.
The future of Recommender Systems lies in these exciting new avenues. With continual innovation, we can shape a more user-centric digital economy, crafting systems that truly understand and meet user needs.
[1]: Grbovic et al., E-commerce in Your Inbox: Product Recommendations at Scale. https://dl.acm.org/doi/10.1145/2783258.2788627
[2]: Vasile et al., Meta-prod2vec: Product embeddings using side-information for recommendation. https://dl.acm.org/doi/10.1145/2959100.2959160
[3]: Liu, Learning to rank for information retrieval.
[4]: Rendle et al., BPR: Bayesian personalized ranking from implicit feedback. https://dl.acm.org/doi/10.5555/1795114.1795167
[5] Swaminathan et al., Batch learning from logged bandit feedback through counterfactual risk minimization. https://jmlr.org/papers/v16/swaminathan15a.html
[6] Faury et al., Distributionally robust counterfactual risk minimization. https://arxiv.org/abs/1906.06211
[7] Jeunen et al., Joint policy-value learning for recommendation. https://dl.acm.org/doi/10.1145/3394486.3403175
[8] Chen et al., Top-k off-policy correction for a REINFORCE recommender system. https://arxiv.org/abs/1812.02353
[9] Afsar., Reinforcement Learning based Recommender Systems: A Survey. https://dl.acm.org/doi/abs/10.1145/3543846
[10] Bonner., Causal embeddings for recommendation. https://dl.acm.org/doi/10.1145/3240323.3240360
[11] Hirshleifer, The private and social value of information and the reward to inventive activity.
[12] De Lara et al. , Payoffs-Beliefs Duality and the Value of Information. https://epubs.siam.org/doi/abs/10.1137/18M1230049
