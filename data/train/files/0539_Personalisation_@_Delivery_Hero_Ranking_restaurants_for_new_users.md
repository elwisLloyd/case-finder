# Personalisation @ Delivery Hero: Ranking restaurants for new users

Источник: https://tech.deliveryhero.com/personalisation-delivery-hero-ranking-restaurants-for-new-users/

As it is said “First impression is the last impression”, providing tailored recommendations to new users goes a long way in the retention journey and maintains stickiness to the platform.
In this blog post, we’ll explore how we utilise machine learning to rank restaurants for our new app users and discuss the following topics:
- Ranking and the cold start problem
- Factors to consider for food delivery restaurant ranking
- Establishing a baseline model
- Going further with LambdaMART
Ranking and the cold-start problem
At Delivery Hero Tech, our mission is to provide the best app experience for our customers, with personalisation being key to achieving this. We aim to streamline the discovery of favourite foods and restaurants for our users.
One way to achieve this is through personalised restaurant ranking, offering greater visibility to establishments that resonate with our customers’ preferences.
To this end, our team has been hard at work developing tailored ranking systems that consider factors such as cuisine, budget, time of day, and location.
These personalised systems assign scores to restaurants, which are then used to sort the establishments. Restaurants with higher scores appear at the top of the list. The scoring can be represented mathematically as follows:
Many personalisation strategies we’ve explored utilise collaborative filtering, which leverages user-item interactions like clicks and orders to identify similar users and recommend relevant items. This approach becomes more effective with increasing user interactions, making it ideal for returning users.
However, we have found that collaborative filtering falls short for new customers, who have yet to interact with our platform. This is known as the cold start problem. To address this, we’ve developed a dedicated model using content-based filtering, which relies on item features rather than user-item interactions. In the next section, we’ll delve into the features used for this content-based filtering model.
Cold start models mitigate the challenge of not knowing much about new customers by trying to use aggregate information and signals/behaviours from long-term customers.
Food delivery… What factors should be considered for restaurant ranking?
Before modeling, we identified key factors influencing a customer’s decision to order from a restaurant. We listed some of the most significant below:
Relevance
Relevance is a crucial factor in a customer’s decision-making process, encompassing a range of elements such as restaurant cuisine, budget, ratings, time of day, and location.
Delivery time
Prompt delivery is vital in the food delivery industry. Customers prefer shorter delivery times, making it an important factor to consider.
Delivery fees
Similarly, delivery fees play a significant role in customer decisions. Lower fees make a restaurant more attractive to potential customers.
With these factors in mind, we constructed our feature set.
Figure 1: Distance distribution for randomly sampled ordered and non-ordered vendors. Customers prefer to order from restaurants which are closer.
Establishing a baseline model
In any data science project, starting with a baseline model is essential. It helps to grasp the problem, test an end-to-end solution, and save effort. It also serves as a benchmark for evaluating more sophisticated models. The baseline model should be kept simple.
For our cold start ranking scenario, we implemented the following baseline model.
This model assumes that for new customers, relevance can be approximated by popularity. Additionally, delivery time and fees are approximated by distance.
We used the Hyperopt package and Bayesian search to efficiently find the best values for a and b. To evaluate the performance of different combinations of a and b, we proceeded with backtesting the model on a large sample of past sessions with orders. For each session, we applied the model to rank available restaurants and recorded the rank given to the ordered restaurant. At the end of each round, we compiled the recorded ranks and derived an average NDCG value from each session NDCG.
NDCG (Normalized Discounted Cumulative Gain) is a commonly used ranking metric defined by the following formula:
In our case, restaurant relevance is simply defined by 1 if it is being ordered and by 0 otherwise. For that reason, we have the simplified expressions:
Once all rounds were completed, we selected the a and b values corresponding to the backtest with the highest observed average NDCG.
This model, while very simple, was shown to perform better than simple distance sorting.
Figure 2: Bivariate density plot showing distance against delivery time. A moderate correlation is observed.
Going further with LambdaMART
Despite the baseline model’s practicality, it has limitations.
The linear model doesn’t accurately represent reality. For example, as highlighted in Figure 2, while some correlation is observed, the correlation is not strong. Besides, model scalability to additional features is limited due to the exponential growth of the search space for model parameters.
To overcome these issues, we adopted LambdaMART, a more sophisticated learning-to-rank algorithm that combines LambdaRank and gradient-boosted trees (GBT). LambdaMART is effective with a large number of features and requires little to no feature transformation. We added several new features, such as short-term popularity, restaurant average preparation time, and restaurant location.
LambdaMART was A/B tested and demonstrated superior performance compared to the baseline model.
Conclusion
In this blog post, we presented our journey to improve restaurant recommendations for new customers, from feature exploration to a simple baseline model, and finally to LambdaMART, a more sophisticated learning-to-rank algorithm.
The significant performance improvements we achieved encourage us to continue our efforts with learning-to-rank models. We have since been working on incorporating personalization features to extend our LambdaMART model to returning customers, further refining the recommendation experience to ensure our users discover their favourite foods and restaurants with ease.
References
Would you like to become a Hero? We have good news for you, join our Talent Community to stay up to date with what’s going on at Delivery Hero and receive customised job alerts!
