# Classifying restaurant cuisines with subjective labels

Источник: https://medium.com/foodpanda-data/classifying-restaurant-cuisines-with-subjective-labels-fa10012d18a9

“Is Chendol Singaporean or Malaysian?” (Ans: Singaporean in Singapore, Malaysian in Malaysia)
Many Singaporeans and Malaysians would remember the great food debate back in 2018 when CNN announced the world’s best 50 desserts — featuring “Cendol, Singapore”. In the same year, Singapore’s plan to bid for UNESCO recognition of its hawker culture drew resistance from Malaysians who felt that their hawker culture (which serves similar dishes) should be recognized instead.
This subjective nature of cuisine definitions poses a challenge when we build machine learning models to categorise the cuisines. In this article, we explore solutions that aim to standardise cuisine labels while taking into account local customer opinions. Ultimately, we want the cuisine labels to improve customer’s search experience on the platform, and help them find what they are looking for more quickly and accurately.
Problem Statement
Initially, the business problem did not seem as complex — we wanted to tag the restaurants on our platform with the correct cuisines. Having the right cuisine tags were important as they are to be used for various features on the platform to improve customers’ search and discovery experience. Examples of cuisines include Dish-based (Chicken, Pasta, Beverages) and Geographical/Cultural (Italian, Singaporean, French) categories.
Having tried manually-labelling a sample of restaurant cuisines, the exercise proved to be time-consuming. foodpanda has hundreds of thousands of restaurants across the 11 markets we operate in, and given the number of possible cuisines that a restaurant could be tagged with, there is no effective way to tag the restaurants with cuisines manually. To make things more complicated, some vendors even serve a multi-cultural mix of cuisines! This prompted them to approach the Data team for an automated solution.
Working out our solutions
As mentioned in the introduction, cuisine definitions can be subjective. From manually generated data labels, we noticed that two restaurants that sell very similar products may be labelled differently by different labellers. This suggests labellers are not aligned on the definitions and more iterations of discussions and re-labelling is required. We also noticed that given the large number of cuisine categories available, some labels may be missed out during the data labelling process. Inconsistent or missing data labels affect any models trained based on it, and also affects evaluation metrics.
We summarise in this table some of the models we tried building, weighing the pros and cons for each.
After several model iterations, we found that a combination of the last two methodologies allow us to develop a model with acceptable quality at scale. We elaborate more on how the two methods work together in the sections below.
Step 1: Using customer behaviours to determine correct labels
- We establish a list of keywords that gives us high confidence that a user is looking for a particular cuisine.
- We then analyse the restaurants that customers click on after searching for these keywords, and assume that these restaurants should be labelled with the cuisines associated with their search terms.
Step 2: Semi-supervised using embeddings
After identifying the correct cuisine labels for the restaurants, we compare the menu of these restaurants against all other restaurants and identify which pairs of restaurants have similar menus.
The steps are as follows:
- Generate fastText embeddings for each menu item in all restaurants
- Calculate average of the menu item embeddings for each restaurant
- Generate cosine similarity scores between the restaurants labelled using customer behaviour, and all other restaurants
4. Generate predictions for unlabelled restaurants for pairs with high cosine similarity scores
Visualising the Embeddings
The results of the steps above can be seen in the following gif, where the visualisation allows us to see how similar or different restaurants are. Distances between nodes are based on similarity of their embeddings.
Get Chin Wee Chok’s stories in your inbox
Join Medium for free to get updates from this writer.
Observations
- Some cuisines (Thai/Pizza) have very distinct clusters while other broader cuisines (Dessert/Cakes & Bakery) have multiple clusters that are scattered
- Nevertheless, the embeddings generated work well in helping to identify which restaurants are similar and which are not
Label Validation
In the last step, the cuisine labels generated are validated manually. This data validation step is different from our initial hand-labelling approach in the following ways:
- Instead of considering all cuisines, labelling specialists are provided a narrowed down list.
- Predictions from models may be obviously wrong, and we need labelling specialists to help us sieve out wrong cuisines since our approach may still predict false labels.
The following is an example of our labelling specialists fill in when they validate the results:
Evaluating the solution
Why is our approach a good solution?
Instead of just relying on an employee to tag the cuisines, the approach also takes into consideration customers’ feedback based on inference of user actions on the platform
- This helped us get buy-in from stakeholders for the predictions generated, as predictions are generated in a ‘white-box’ approach
- While labelling specialists still need to decide if a cuisine is correct/wrong, there is less room for subjectivity since they are not suggesting additional labels
Effort required to build a model from scratch is lower compared to a supervised model or rule-based model, making it more scalable.
- Less time is spent checking possible labels for each restaurant, and labelling specialists avoid missing out labels that should be applied since they have been generated by the model.
Results are reasonably accurate to roll out on production confidently
Model limitations
While the existing approach reduces many of the challenges we faced in our previous approaches, the model is still far from ideal. We observed the following limitations in the model results:
- We are limited to a pre-defined list of cuisines
- The similarity approach works great for identifying dominant cuisine types, but not so much for identifying a fusion of cuisines.
- Furthermore, the current approach either identifies missing cuisine tags or affirms existing cuisines, but we have yet to try using it to point out incorrect cuisine tags.
- Getting labels from Customer clicks might not always give the correct labels, especially since it is dependent on what customers click on.
- Some restaurants might appear to be similar in menu item names but are not the same cuisine, leading to false positives (E.g. “Carrot Cake” could refer to the Singaporean hawker dish or a Western Cake.)
Future improvements/expansions
With the limitations in mind, there is great potential for the future of our cuisine tagging project. There are several parts in the model that can be tweaked and iterated upon to determine the best approach and configuration.
- We can further develop the model to find the best threshold to set for the cosine similarity score.
- We could identify new cuisine categories based on observations of the embedding space. For example, the Beverages category could be split into smaller categories like (Coffee, Bubble Tea, Coconut Shake, etc.).
- We could also experiment with using the similarity scores to identify incorrect cuisine tags if any of the restaurants tagged with a cuisine have a too small cosine similarity score from the rest of the cuisine restaurants.
- Finally, given the diverse markets that foodpanda operates in, we could expand the model to other languages while accounting for character-based languages like Chinese and Thai.
So, is Chendol Singaporean or Malaysian? At foodpanda, the answer depends on the local context of the country ;) Ultimately, for the problem we are trying to solve, the answer to this is what improves the experience for our customers.
Credits
Special thanks to the Content team for their support for the project, Wen Qing and Jerome for their contributions to the project as well.
