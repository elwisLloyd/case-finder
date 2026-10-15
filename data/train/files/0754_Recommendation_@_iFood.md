# Recommendation @ iFood

Источник: https://medium.com/ifood-engineering/recommendation-ifood-88d60fa8bc6a

It’s impossible to talk about recommendation at iFood without giving you a context of what is the team like and what is iFood like (spoiler alert: it’s the biggest foodtech in Latin America!). So let’s get into it!
iFood Brain
iFood Brain is the the team of innovation and data. At Brain, we have people with different skills in roles such as data analysts, data engineers and data scientists.
We built iFood Brain to provide the best user, restaurants and riders experience so as to maximize the number of orders. At Brain, we built several machine learning models to provide accurate answers for questions such as:
- How long it will take for an order to be completed (estimated time arrival)
- What are the best restaurants and dishes to recommend to a customer;
- Whether the payment being used is fraudulent or not.
To generate the training datasets for those models — and serve features in real-time so the models’ predictions can be made correctly — it is necessary to create efficient, distributed data processing pipelines.
We have a very diverse team with people from different parts of the world. If you have questions about how we work or want to work with us, you should check our career page.
iFood in numbers
iFood is the largest food-tech in Latin America. We have a few dozen of millions of users who place more than 44 million orders per month, within more than 200 thousand establishments active on the platform, and, to make this reach you, we have more than 150 thousand drivers. We are the 4th largest food delivery app in download numbers worldwide.
We believe that a personalized experience is fundamental to help the user’s life. We have the challenge of making a whole new iFood experience for each user.
Unique moment
Food is associated with memorable moments in our lives, and all we want to do is make this moment of opening the app and ordering easier. Several happy moments of our life were around a dinner table with the family or a good chat with our friends’ over snacks and beers.
To make these moments happen, we are here to optimize your decision-making process using recommendation techniques. Finding what you want within millions of options is quite a challenge. We have an additional complication that is: food is perishable. It is made for you, and your logistics need to be very precise so that soon after the product is ready, it needs to arrive fresh at your home.
Personal choice
Each of us here has a favorite food. We may even have favorite cuisines, but each restaurant might present the same food in different ways. It could be more spicy than you’re used to, or use the restaurant’s special seasoning. More than that, everyone who has ever used a food delivery marketplace has gone through the frustrating experience of scrolling forever while your stomach is making weird noises, and you’re unable to attend to it because of the overwhelming amount of possibilities. We don’t want you to go through that. We want to make the experience of finding food as seamless and as quick as possible.
Apart from that, we also have a challenge looking directly into the restaurant’s kitchen, aiming for the perfect match between the user and the food.
Users and restaurants have unique characteristics, and they change all the time. Who never started to eat healthier on Monday, and, by Sunday, went back to eating pizza? The best restaurant must go beyond the best food. It must also have the right price for you, does that restaurant you always wanted to buy have a special offer?
Looking from the restaurant’s point of view, how do I make new users buy at my establishment? How do I find users who will like my menu? For that, we need to look at the recommendation beyond the needs of the customer.
Challenges
As a food tech, we have an additional challenge compared to regular eCommerces because our items and restaurants have a small delivery area and limited opening hours. Today at iFood, we have polygons with thousands of restaurants capable of serving you and this list changes depending on where and when you open the app, so finding the best pizzeria for you is much harder than you’d expect.
The essential point is that the customer hardly plans her order, so she is already hungry when she comes online to order. No one that’s hungry is in a good mood.
There is no point in recommending her the best restaurant fitted for her if the restaurant has dozens of orders in line at its kitchen and is about to delay orders. This might affect the customer’s experience negatively, causing frustration and maybe even hatred for our product.
The app emits several signs, so knowing how to create a useful engagement function for our models is a challenge, how to interpret someone’s review as a one-off failure or a consequence of a failed process?
Every day thousands of new users and restaurants come into the platform; how do we serve them the best experience?
Everywhere can be personalized
We have worked hard in the last year to plug the recommendation anywhere in the user experience, making it personalized.
We can actively notify the user via a push notification saying that his restaurant has a discount. Another way is to passively wait for the user to select categories, search, or enter the session with all the restaurants. Within them, our goals are to please you right away, facilitating your journey.
Get Julia Tessler’s stories in your inbox
Join Medium for free to get updates from this writer.
Our next frontier will be to have components designed for you, more inclusive, understand your way of navigating and enable new elements, and create new ways to display the same content, always thinking about simplifying your journey.
Main pillars
Our recommendation are based on four main pillars we need to learn to provide the best options:
- Customer profile: How much can she pay? How active is this user? Which cuisine does she like most?
- Context: How would the offer change on weekends? On special dates? Location?
- Customer journey: How does the user journey affect recommendation? If a user ordered pizza yesterday, what are the best cuisines/restaurants/dishes to offer today? How to balance exploration/exploitation in time?
- Dish profiles: To better understand the user context, we need to crack down dishes. What tags can we associate with dishes? Pleasure Treat? Healthy? Low-calorie? Trendy? Quick fill? How about allergy-risk?
The problem we want to solve is clear: what is the best offer to this customer now?
Candunga
Candunga is a little chubby fish. This is the north-eastern Brazilian nickname for — apparently — the “Amboré” or Frillfin Goby or Bathygobius soporator fish.
Candunga is also the name of our main algorithm for orderings lists of restaurants and dishes.
ALS Main
Alternating Least Squares is a pretty usual recommendation algorithm to reinforce tastes by suggesting new things similar to what we know you like through implict feedback (such as ordering some kind of food or looking into specific restaurants frequently). But ALS fails to identify new tastes or changes in diet. We used ALS due to its high degree of suggestions for similar users.
Looking at conversion metrics by frequency of purchase, we saw that users who bought this approach the most were working very well, but users at the beginning of their life within iFood were not performing as well best. Another issue with our first approaches was that our data is more sparse than usual due to geographical constraints (restaurants don’t usually deliver to all the users in the world, for example).
Also, new restaurants had a slower growth ramp than the previous solution.
ALS Cluster
We decided to use an approach to have more models taking advantage of the matrix factoring solution. Instead of excluding the user as axis — which caused loss of precious information, these new models have features regarding users.
We can use anything from the user’s context: their location, temperature of that location, shift, and any available features.
The main thing behind this solution is the less sparse matrix that indicates the popularity of restaurants with an affinity with you.
Solution
Our final solution is the union of several matrices and external features for the boost. The Candunga project adapts to different scenarios of the app, such as lists of restaurants and dishes.
We have the power to create this set of matrices and features for each list and user group. Each matrix receives a different weight. These weights are defined using Bayesian optimization focused on improving the Normalized Discounted Cumulative Gain score (NDCG).
Our features sections are defined as weights for restaurants and dishes by external models. These models can be things like best-selling restaurants; restaurants with a full kitchen to not send new orders; They are great for minimizing cold start and allowing Candunga to adapt to a multi-objective scenario.
Example
See how the lists with the adapted model look versus the previous sorting solution.
This is the example of Luiz Felipe Mendes list of lunch dishes. In the first option, we see desserts and fatty foods. After calling Candunga, the model learned correctly that Luiz likes Japanese food and healthy food.
Deploy
To do this, we have a considerable challenge to serve this giant volume of users. We have a very particular feature that orders are concentrated at shifts that people usually eat.
Today our solution is based on the AWS Sagemaker for both training and serving the model. We are making constant improvements to evolve this architecture; our current bet is the inclusion of ScyllaDB to store predictions.
Results
Using Candunga, we achieved incredible results after dozen iterations in the model.
The chart on the left shows the conversion gain per session, and the one on the right shows the increase in coverage. With this charts, we concluded that Candunga is better for users for converting more and for the health of the marketplace (restaurants) due to the better distribution of sales among the restaurants.
Our main challenge was to improve the conversion in the cold start scenario. It is much better now, but it’s an ongoing process.
Our journey to build the perfect personalized experience with food delivery, tailored to attend you and your needs is still in the oven, but it has been quite a journey so far. If agree with me and would like to work with us, plese check out our carreer page (:
This blog post wouldn’t be possible without the incredible work of Renan Oliveira and the unbelievable wizarding skills of Felipe Poncion.
