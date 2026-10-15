# Solving the weekly menu puzzle: recommendations at Picnic

Источник: https://blog.picnic.nl/solving-the-weekly-menu-puzzle-recommendations-at-picnic-42da16b281ad

Figuring out what’s for dinner is that daily question we can all relate to. Not only does it require effort, it can also be hard to get creative, so we often end up sticking to the same few dishes we’re familiar with.
At Picnic, we’re on a mission to alleviate the dinner dilemma for our customers. We’ve discovered that in-app recipes serve as a powerful tool to achieve this goal.
Recipes can give inspiration, or simply be the greatest version of your all-time favourite dish. Either way, through the Picnic app you can add them with a click, swiftly shaping your weekly menu.
Yet, discovering that specific inspiration or something that suits your taste can sometimes still take a bit of extra effort. Especially when the service you’re using overlooks your preferences. Imagine opening the app only to be greeted by that one veggie you’d really rather avoid. Well, that’s not exactly the culinary inspiration you were hoping for.
Picnic is working on improving this experience with our recommendation systems. We believe that, if your supermarket already does a good job in suggesting recipes, you can choose your meals with minimal effort and a plenty of inspiration.
With that goal in mind, we have recently introduced a brand new recommender algorithm, and in this blog post, we’ll take you behind the scenes: revealing how we do it, what factors we consider, our plans for future enhancements and, most importantly, which lessons we learned.
Recommendation systems 101
For those unacquainted, a recommendation system is a technology that suggests personalised and relevant items or content to users of a platform, based on their preferences and behaviour. Consider the recommended connections on LinkedIn or the “related items” section on Amazon product pages — both prime examples of recommendation systems at work.
If you ever put your hands on machine learning systems, you’re likely aware that recommenders stand in a category of their own. In this space, problems are often framed quite differently compared to, for example, traditional supervised learning: the typical, which digit does this image represent?
In supervised tasks, there tends to be a target, a set of features, a model representation (a tree, a network, etc.) and parameters to learn by minimising a certain loss function. But in the world of recommendation systems the goal is to find similarities between customers, items, and their context. Usually, the higher the similarity the better. Whilst there is no definition of target in the traditional sense, we do need an indication or some sort of proxy to determine how relevant an item is to a customer.
Two concepts strike out at first when it comes to recommendation systems: content based filtering and collaborative filtering. Content-based filtering is like asking: “I like pasta, what other pasta recipes are out there that I’d enjoy?”. Collaborative filtering, on the other hand, answers the question: “I like pasta, and another customer does too. Will I like the other dishes they’ve ordered?”.
Getting started with recommending recipes
With that said, how did we go about implementing a recommendation system from scratch and incorporate this new feature in the Picnic store?
As per good engineering practice, with new use cases the goal isn’t to kick off with the flashiest solution. So off we went with one of the most straightforward, yet effective, techniques: collaborative filtering based on implicit feedback.
Implicit feedback is any indication of personal relevance that is not a rating or review explicitly given by a user to an item. In our case, we looked at how many times customers would order a certain recipe, and use that as implicit feedback (the more a customer orders a recipe, the more likely they are to feel positive about it).
From an implementation perspective, we used a Python package called implicit. The first ingredient is to create an interaction matrix. You want a matrix with a row for each customer and column for each recipe, and the value of the cells should reflect how confidently we believe that the customer likes (or dislikes) that recipe.
Each row and each column in this matrix can be considered as an interaction vector. The rows represent customers in terms of how they interacted with recipes, and the columns represent recipes, in terms of how customers have interacted with them. In other words, you can think of interaction vectors as embeddings, a way to numerically represent recipes and customers through purchase behaviour.
Out of all the set of algorithms offered by the package, the nearest neighbour models are the ones that performed the best on our data. Specifically the CosineRecommender one.
Imagine each recipe as a point in a space where recipes that are more similar are closer together. Given a customer, the recommender looks at the recipes customers have interacted with and calculates a relevancy score for all other recipes. Put simply: for each customer and recipe, the recommender sums past purchases, weighted by similarity with the recipes being evaluated. Finally, the recipes that get a higher score are recommended.
The package includes a convenient implementation of this recommendation algorithm. Take a sneak peek at the code snippet provided below.
"">"2" data-code-block-lang="python">from implicit.nearest_neighbours import CosineRecommender
model = CosineRecommender()
model.fit(customer_recipe_matrix)
model.recommend(
userid=customers_indexes,
user_items=customer_recipe_matrix[
customers_indexes],
N=number_of_recommendations,
filter_already_liked_items=True)
Next to generating recommendations for a set of customers, through the same model you can also retrieve the similarities between recipes upon which recommendations are generated. For instance, the top 5 similar recipes to ‘Spaanse stoof met gnocchi en merguez’ (‘Spanish stew with gnocchi and merguez’) are the following:
- ‘Gnocchi in romige paprikasaus’ (‘Gnocchi in creamy pepper sauce’)
- ‘Gebakken gnocchi met chorizo en spruitjes’ (‘Fried gnocchi with chorizo and Brussels sprouts’)
- ‘Gnocchi met merguez en spinazie’ (‘Gnocchi with merguez and spinach’)
- ‘Romige gnocchi met erwtjes en gerookte zalm’ (‘Creamy gnocchi with peas and smoked salmon’)
- ‘Makkelijke gnocchi bolognese’ (‘Easy gnocchi bolognese’)
Qualitatively speaking, that’s quite accurate right?
But things can get challenging at times. When noise lurks around similarities can get, arguably, quite unexpected.
Noise and popularity bias
Cosine distance is used a lot in the space of recommendation systems, as it works well despite sparsity and varying magnitude of embeddings. However, it isn’t completely immune to outliers.
There has been an instance where an Indian curry, strangely enough, seemed to be particularly similar to a gnocchi recipe. Believe it or not, it turned out a single customer had purchased gnocchi a staggering 58 times and only a couple times Indian curry, hence why the similarity.
These types of data points can generate noise in the results, and cosine distance won’t be able to deal with such outliers out of the box. Luckily, the package also offers handy functions that can be used to weight or normalise the interaction matrix.
By means of experimentation, we opted to adopt BM25 weighting. This is a technique used to assign importance or relevance scores to the interactions between customers and recipes in a sparse matrix. In simpler terms, it helps to highlight significant interactions and downplay less important ones.
You can check below the exact formula to calculate such weights, as per implementation given in the implicit package.
"1" data-code-block-lang="python">def bm25_weight(X, K1=100, B=0.8):
"""Weighs each row of a sparse matrix X by BM25 weighting"""
# calculate idf per term (user)
X = coo_matrix(X)
N = float(X.shape[0])
idf = log(N) - log1p(bincount(X.col))
# calculate length_norm per document (artist)
row_sums = np.ravel(X.sum(axis=1))
average_length = row_sums.mean()
length_norm = (1.0 - B) + B * row_sums / average_length
# weight matrix rows by bm25
X.data = X.data * (K1 + 1.0) / (K1 * length_norm[X.row] + X.data) * idf[X.col]
This technique also helps in tackling general popularity bias. For example, in our platform all our customers used to see a manually curated list of recipes. Since these recipes were more visible to our customers they were bought more often. Without BM25 weighting the recommender would disproportionately recommend these recipes over less exposed recipes that might be more relevant to this customer.
By weighting the interaction matrix, we tackle outliers and make sure that very popular recipes that have got more exposure compared to others, don’t overpower recipes that get recommended.
Evaluation
Even though offline precision metrics, such as Precision@K or AUC@K, can give an indication of the predictive power of a recommendation algorithm, many would agree that only exposing the recommendations to real customers can ultimately tell something about their quality.
This algorithm has been rolled out to Picnic customers in an A/B testing fashion. Out of all the customers that have bought recipes at least once, we would pick a group to show them recommended content and a group that would be shown content that was manually curated.
Over the course of 8 weeks, we monitored the performance over these groups carefully, trying to tweak and adjust the algorithm week by week and find out what worked best.
According to our estimations, automatically recommended content was just as preferred to our customers as manually curated one. While this may not sound impressive at first, considering the simplicity of this initial iteration, it has been a massive feat! We were able to show that with a simple implementation, we could alleviate the workload of manually curating content. Resulting in saved hours of work, and a much more personalised, scalable solution.
Looking ahead
Due to its simplicity, collaborative filtering alone does come with its limitations. For example, the framework does not allow to explicitly model content-based features. That is, the characteristics of each recipe such as their ingredients, cooking time, or main kitchen. It also does not allow to model explicit preferences of customers. For example, whether they’re vegan, vegetarian, lactose-intolerant, or other preferences.
In the recommendation systems literature, hybrid recommender models seem to be able to take these factors into consideration. The reason for that is, because they combine the collaborative effect of how users interact with items and their specific characteristics at the same time.
An implementation of a hybrid recommender can, for instance, come in the form of the two-tower architecture. This is gaining popularity in many retrieval and ranking workflows across a variety of industries.
Conclusion
Collaborative filtering based on implicit feedback and its implementation of the implicit package has made us learn a great deal about recommendation systems and kick start this new and exciting project. By adopting a methodical approach — starting with simplicity, iterating fast, and ensuring robust A/B testing and meticulous monitoring — we’ve laid a strong foundation in this new domain.
Yet, our ambition does not stop here. We want to keep improving the accuracy and sophistication of our recommendations, with increasingly complex solutions. Stay tuned for updates on our journey in recipe recommendations 🚀.
Join us!
If you share our passion and curiosity about how we plan to tackle this evolving challenge, we invite you to be a part of our team as a Machine Learning Engineer in Search and Ranking. Join us on this venture, contributing to the advancement of Picnic’s recommendation systems and taking them to unprecedented heights!
