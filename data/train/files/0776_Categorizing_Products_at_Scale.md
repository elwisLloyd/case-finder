# Categorizing Products at Scale

Источник: https://shopify.engineering/categorizing-products-at-scale

By: Jeet Mehta and Kathy Ge
With over 1M business owners now on Shopify, there are billions of products being created and sold across the platform. Just like those business owners, the products that they sell are extremely diverse! Even when selling similar products, they tend to describe products very differently. One may describe their sock product as a “woolen long sock,” whereas another may have a similar sock product described as a “blue striped long sock.”
How can we identify similar products, and why is that even useful?
Applications of Product Categorization
Business owners come to our platform for its multiple sales/marketing channels, app and partner ecosystem, brick and mortar support, and so much more. By understanding the types of products they sell, we provide personalized insights to help them capitalize on valuable business opportunities. For example, when business owners try to sell on other channels like Facebook Marketplace, we can leverage our product categorization engine to pre-fill category related information and save them time.
In this blog post, we’re going to step through how we implemented a model to categorize all our products at Shopify, and in doing so, enabled cross-platform teams to deliver personalized insights to business owners. The system is used by 20+ teams across Shopify to power features like marketing recommendations for business owners (imagine: “t-shirts are trending, you should run an ad for your apparel products”), identification of brick-and-mortar stores for Shopify POS, market segmentation, and much more! We’ll also walk through problems, challenges, and technical tradeoffs made along the way.
Why is Categorizing Products a Hard Problem?
To start off, how do we even come up with a set of categories that represents all the products in the commerce space? Business owners are constantly coming up with new, creative ideas for products to sell! Luckily, Google has defined their own hierarchical Google Product Taxonomy (GPT) which we leveraged in our problem.
The particular task of classifying over a large-scale hierarchical taxonomy presented two unique challenges:
- Scale: The GPT has over 5000 categories and is hierarchical. Binary classification or multi-class classification can be handled well with most simple classifiers. However, these approaches don’t scale well as the number of classes increases to the hundreds or thousands. We also have well over a billion products at Shopify and growing!
- Structure: Common classification tasks don’t share structure between classes (i.e. distinguishing between a dog and a cat is a flat classification problem). In this case, there’s an inherent tree-like hierarchy which adds a significant amount of complexity when classifying.
Sample visualization of the GPT
Representing our Products: Featurization 👕
With all machine learning problems, the first step is featurization, the process of transforming the available data into a machine-understandable format.
Before we begin, it’s worth answering the question: What attributes (or features) distinguish one product from another? Another way to think about this is if you, the human, were given the task of classifying products into a predefined set of categories: what would you want to look at?
Some attributes that likely come to mind are
- Product title
- Product image
- Product description
- Product tags.
These are the same attributes that a machine learning model would need access to in order to perform classification successfully. With most problems of this nature though, it’s best to follow Occam’s Razor when determining viable solutions.
Among competing hypotheses, the one with the fewest assumptions should be selected.
In simpler language, Occam’s razor essentially states that the simplest solution or explanation is preferable to ones that are more complex. Based on the computational complexities that come with processing and featurizing images, we decided to err on the simpler side and stick with text-based data. Thus, our classification task included features like
- Product title
- Product description
- Product collection
- Product tags
- Product vendor
- Merchant-provided product type.
There are a variety of ways to vectorize text features like the above, including TF-IDF, Word2Vec, GloVe, etc. Optimizing for simplicity, we chose a simple term-frequency hashing featurizer using PySpark that works as follows:
HashingTF toy example
Given the vast size of our data (and the resulting size of the vocabulary), advanced featurization methods like Word2Vec didn’t scale since they involved storing an in-memory vocabulary. In contrast, the HashingTF provided fixed-length numeric features which scaled to any vocabulary size. So although we’re potentially missing out on better semantic representations, the upside of being able to leverage all our training data significantly outweighed the downsides.
Before performing the numeric featurization via HashingTF, we also performed a series of standard text pre-processing steps, such as:
- Removing stop words (i.e. “the”, “a”, etc.), special characters, HTML, and URLs to reduce vocabulary size
- Performing tokenization: splitting a string into an array of individual words or “tokens”.
The Model 📖
With our data featurized, we can now move towards modelling. Ensuring that we maintain a simple, interpretable, solution while tackling the earlier mentioned challenges of scale and structure was difficult.
Learning Product Categories
Fortunately, during the process of solution discovery, we came across a method known as Kesler’s Construction [PDF]. This is a mathematical maneuver that enables the conversion of n one-vs-all classifiers into a single binary classifier. As shown in the figure below, this is achieved by exploding the training data with respect to the labels, and manipulating feature vectors with target labels to turn a multi-class training dataset into a binary training dataset.
Kesler’s Construction formulation
Applying this formulation to our problem implied pre-pending the target class to each token (word) in a given feature vector. This is repeated for each class in the output space, per feature vector. The pseudo-code below illustrates the process, and also showcases how the algorithm leads to a larger, binary-classification training dataset.
- Create a new empty dataset called modified_training_data
- For each feature_vector in the original_training_data:
- For each class in the taxonomy:
- Prepend the class to each token in the feature_vector, called modified_feature_vector
- If the feature_vector is an example of the class, append (modified_feature_vector, 1) to modified_training_data
- If the feature vector is not an example of the class, append (modified_feature_vector, 0) to modified_training_data
- Return modified_training_data
Note: In the algorithm above, a vector can be an example of a class if its ground truth category belongs to a class that’s a descendant of the category being compared to. For example, a feature vector that has the label Clothing would be an example of the Apparel & Accessories class, and as a result would be assigned a binary label of 1. Meanwhile, a feature vector that has the label Cell Phones would not be an example of the Apparel & Accessories class, and as a result would be assigned a binary label of 0.
Combining the above process with a simple Logistic Regression classifier allowed us to:
- Solve the problem of scale - Kesler’s construction allowed a single model to scale to n classes (in this case, n was into the thousands)
- Leverage taxonomy structure - By embedding target classes into feature vectors, we’re also able to leverage the structure of the taxonomy and allow information from parent categories to permeate into features for child categories.
- Reduce computational resource usage - Training a single model as opposed to n individual classifiers (albeit on a larger training data-set) ensured a lower computational load/cost.
- Maintain simplicity - Logistic Regression is one of the most simple classification methods available. It’s coefficients allow interpretability, and reduced friction with hyperparameter tuning.
Inference and Predictions 🔮
Great, we now have a trained model, how do we then make predictions to all products on Shopify? Here’s an example to illustrate. Say we have a sample product, a pair of socks, below:
Sample product entry for a pair of socks
We aggregate all of its text (title, description, tags, etc.) and clean it up using the Kesler’s Construction formulation resulting in the string:
“Check out these socks”
We take this sock product and compare it to all categories in the available taxonomy we trained on. To avoid computations on categories that will likely be low in relevance, we leverage the taxonomy structure and use a greedy approach in traversing the taxonomy.
Sample traversal of taxonomy at inference time
For each product, we prepend a target class to each token of the feature vector, and do so for every category in the taxonomy. We score the product against each root level category by multiplying this prepended feature vector against the trained model coefficients. We start at the root level and keep track of the category with the highest score. We then score the product against the children of the category with the highest score. We continue in this fashion until we’ve reached a leaf node. We output the full path from root to leaf node as a prediction for our sock product.
Evaluation Metrics & Performance ✅
The model is built. How do we know if it’s any good? Luckily, the machine learning community has an established set of standards around evaluation metrics for models, and there are good practices around which metrics make the most sense for a given type of task.
However, the uniqueness of hierarchical classification adds a twist to these best practices. For example, commonly used evaluation metrics for classification problems include accuracy, precision, recall, and F1 Score. These metrics work great for flat binary or multi-class problems, but there are several edge cases that show up when there’s a hierarchy of classes involved.
Let’s take a look at an illustrating example. Suppose for a given product, our model predicts the following categorization: Apparel & Accessories > Clothing > Shirts & Tops. There’s a few cases that can occur, based on what the product actually is:
1. Product is a Shirt: In this case, we’re correct! Everything is perfect.
Product is a dress - Model example
2. Product is a Dress: Clearly, our model is wrong here. But how wrong is it? It still correctly recognized that the item is a piece of apparel and is clothing
3. Product is a Watch: Again, the model is wrong here. It’s more wrong than the above answer, since it believes the product to be an accessory rather than apparel.
Product is a phone - Model example
4. Product is a Phone: In this instance, the model is the most incorrect, since the categorization is completely outside the realm of Apparel & Accessories.
The flat metrics discussed above would punish each of the above predictions equally, when it’s clear that this isn’t the case. To rectify this, we leveraged work done by Costa et al. on hierarchical evaluation measures [PDF] which use the structure of the taxonomy (output space) to punish incorrect predictions accordingly. This includes:
- Hierarchical accuracy
- Hierarchical precision
- Hierarchical recall
- Hierarchical F1
As shown below, the calculation of the metrics largely remains the same as their original flat form. The difference is that these metrics are regulated by the distance to the nearest common ancestor. In the examples provided, Dresses and Shirts & Tops are only a single level away from having a common ancestor (Clothing). In contrast, Phones and Shirts & Tops are in completely different sub-trees, and are four levels away from having a common ancestor
Example hierarchical metrics for “Dresses” vs. “Shirts & Tops”
This distance is used as a proxy to indicate the magnitude of incorrectness of our predictions, and allows us to present, and better assess the performance of our models. The lesson here is to always question conventional evaluation metrics, and ensure that they indeed fit your use-case, and measure what matters.
When Things Go Wrong: Incorrect Classifications ❌
Like all probabilistic models, our model is bound to be incorrect on occasions. While the goal of model development is to reduce these misclassifications, it’s important to note that 100% accuracy will never be the case (and it shouldn’t be the gold standard that teams drive towards).
Instead, given that the data product is delivering downstream impact to the business, it's best to determine feedback mechanisms for misclassification instances. This is exactly what we implemented through a unique setup of schematized Kafka events and an in-house annotation platform.
Feedback system design
This flexible human-in-the-loop setup ensures a plug-in system that any downstream consumer can leverage, leading to reliable, accurate data additions to the model. It also extends beyond misclassifications to entire new streams of data, such that new business owner-facing products/features that allow them to provide category information can directly feed this information back into our models.
Back to the Future: Potential Improvements 🚀
Having established a baseline product categorization model, we’ve identified a number of possible improvements that can significantly improve the model’s performance, and therefore its downstream impact on the business.
Data Imbalance ⚖️
Much like other e-commerce platforms, Shopify has large sets of merchants selling certain types of products. As a result, our training dataset is skewed towards those product categories.
At the same time, we don’t want that to preclude merchants in other industries from receiving strong, personalized insights. While we’ve taken some efforts to improve the data balance of each product category in our training data, there’s a lot of room for improvement. This includes experimenting with different re-balancing techniques, such as minority class oversampling (e.g. SMOTE [PDF]), majority class undersampling, or weighted re-balancing by class size.
Translations 🌎
As Shopify expands to international markets, it’s increasingly important to make sure we’re providing equal value to all business owners, regardless of their background. While our model currently only supports English language text (that being the primary source available in our training data), there’s a big opportunity here to capture products described and sold in other languages. One of the simplest ways we can tackle this is by leveraging multi-lingual pre-trained models such as Google’s Multilingual Sentence Embeddings.
Images 📸
Product images would be a great way to leverage a rich data source to provide a universal language in which products of all countries and types can be represented and categorized. This is something we’re looking to incorporate into our model in the future, however with images come increased engineering resources required. While very expensive to train images from scratch, one strategy we’ve experimented with is using pre-trained image embeddings like Inception v3 [PDF] and developing a CNN for this classification problem.
Our simple model design allowed us interpretability and reduced computational resource usage, enabling us to solve this problem at Shopify’s scale. Building out a shared language for products unlocked tons of opportunities for us to build out better experiences for business owners and buyers. This includes things like being able to identify trending products or identifying product industries prone to fraud, or even improving storefront search experiences.
If you’re passionate about building models at scale, and you’re eager to learn more - we’re always hiring! Reach out to us or apply on our careers page.
Additional Information
- Google Product Taxonomy
- Multi-Lingual Universal Sentence Encoder for Semantic Retrieval, 2019.
- SMOTE: Synthetic Minority Over-sampling Technique, 2002. Journal of Artificial Intelligence Research 16 (2002) 321–357.
- A Review of Performance Evaluation Measures For Hierarchical Classifiers, 2007 [PDF]. Association for the Advancement of Artificial Intelligence Research.
