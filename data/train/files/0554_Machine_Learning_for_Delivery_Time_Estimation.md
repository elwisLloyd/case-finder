# Machine Learning for Delivery Time Estimation

Источник: https://tech.olx.com/machine-learning-for-delivery-time-estimation-1-591c8df849a0

In today’s fast-paced digital marketplace, accurate delivery time estimation has become crucial in ensuring customer satisfaction and building trust in e-commerce platforms.
OLX, a leading online marketplace, understands the significance of providing reliable delivery estimates to its users. To achieve this, we embarked on a data science project aimed at optimizing the delivery time estimation process. In this article, we will take an in-depth look at the various stages of this project, providing insights into the steps involved, including:
- Define the problem and success criteria
- Exploratory Data Analysis
- Baseline solution
- A/B Testing
- Training and Modeling
- Productionizing the Solution
- Next Steps
So let’s start by delving into each of these points, beginning with defining and understanding the problem.
Delivery Time Estimation
The project started as a research project focused on using Machine Learning (ML) to improve the delivery time estimation and encourage buyers to use Pay&Ship. Pay&Ship is one of the options available to buyers in certain markets, where the seller sends the item through a delivery service, and OLX holds the money of the transaction and transfers it to the seller when the package is delivered to the buyer.
Through our research, we discovered that one of the factors buyers consider when purchasing an item with Pay&Ship is the delivery time. The main problem we identified is that users are currently not informed about the expected delivery date for the items they are considering, despite this being standard information in most e-commerce and classified businesses. Users have a natural inclination to seek this information and use it in their decision-making process. Since other players in the market have already implemented this solution, we have reason to believe that this is indeed a viable case that can be addressed using ML.
The objective of our project was to determine the factors that impact delivery time estimation and, by doing so, increase the conversion rate of users who choose to buy with Pay&Ship while decreasing churn for users who had a negative experience with delivery. However, before delving into finding a solution, we first needed to address two important questions.
Before Starting the Project
The first two questions that we made before diving deep into finding solutions were:
- What is the current solution that exists already in the company, if any?
- What does success look like?
What is the current solution that exists already in the company, if any?
This is very important to make sure that we don’t redo work that might already exist or start from scratch if we already have another solution implemented. We didn’t find any solution, so we checked the web page. Currently, the ad page only displays information about each delivery provider and their respective costs and nothing regarding delivery time, as shown in the picture below.
What does success look like?
How can we say in the end that our project was a successful project? What business metrics do we want to impact? What do we want to see after the implementation of our solution? In other words, what success looks like? 
We believe that the lack of this information on the page might be a factor in users’ decision-making process. Therefore, we expect to see an increase in the number of deliveries where this information is displayed.
Now, let us start by understanding how to solve the problem.
Exploratory Data Analysis
In most e-commerce, the delivery time would be the time that the company packages the item to the carrier plus the time that the delivery provider takes to deliver the package to the buyer. However, as a classified business, we don’t sell anything — we facilitate the life of sellers to find buyers. So the total delivery time would be as shown in the picture below:
It is worth mentioning that the seller can be anyone who posts an ad on the OLX website, while the carrier refers to the available delivery providers in each country that handle the deliveries. Now it becomes clear that the total time consists of two components: the time it takes for the seller to hand over the package to a carrier (after the buyer makes the purchase on the website) and the time it takes for the carrier to deliver the package to the buyer’s house.
So we must figure out what mostly impacts the seller and carry time. Which one is the fastest? Which one counts more for the total delivery time? Are the attributes that impact seller time the same as carrier time?
Those are the kind of questions we expect to answer during the analysis. So let us take a look into the data and see if we get some insights.
Difference between Seller and Carrier
- We can see from the table above that the average for the seller is approximately one day, and for the carrier is two days, meaning that the carrier is the longest step.
- Considering the seller is not a business, their one-day time to deliver the package is quite fast.
- The total delivery time is three days on average (Applying the formula above seller + carrier = delivery time).
Let's look at the delivery time distribution to see if it gives us a broader perspective.
Distribution on how many days it takes to be delivered
Below we can see the distribution of the delivery time collected from delivery data at OLX. Here, we can see quite some interesting things.
- The distributions of the time in days. We can see a normal distribution skewed to the right.
- Most of the packages are delivered within three days.
- Some packages are delivered on the same day.
Really interesting knowledge, but there may be a difference among each carrier. Some might be faster than others. Let’s check that:
Distribution among carriers
- The average varies among each carrier, meaning that the carrier (the company that makes the delivery) might be a good predictor feature for our model.
- Despite the fact that the average is three days, if we look at each delivery provider, we see that there is quite a difference between them.
Other factors that are important
The delivery provider, from our analysis, was the most important feature. However, some other attributes also have its contributions to the delivery time, namely:
- Day of the week (The order is made)
- Region (Of the seller)
- Distance from the seller to the buyer
We can use those features to see if we can improve performance. At this point, we still don’t know how much value our solution will bring, if any, so before jumping into finding a really complex solution with all the features all at once, let us think about this:
What is the simplest way we can test our assumptions and prove value from our solutions?
Initial Solution
From our analysis, we decided to use each delivery provider's mean and standard deviation to create a simple baseline, which will help us understand the impact of having this information on the web page. We will show the information next to each delivery provider as a predicted range, as shown in the picture below.
Using a baseline is very important. You can validate your solution and understand the impact of your change without the need to spend months working on a solution and, in the end, figuring out that your work didn’t produce any value.
Get Enderson Santos’s stories in your inbox
Join Medium for free to get updates from this writer.
But before going into production, let's evaluate how our model performs offline.
Baseline Offline Performance
In the picture above, we can see the percentage of the inside the range, before and after, that our baseline solution achieved.
We created ranges for the delivery time predictions, like three to six days. Then we analyzed to see how good those ranges were. There are three different possibilities:
- The true prediction fell within the range that we predicted. Let’s say we predict 3 to 6 days, and our prediction was 4 days. That’s is inside 3 to 6 days, then our prediction was right since the package was delivered within the expected time.
- If the true value was before the range we created, let’s say 2 days, then we compute before, meaning that the package was delivered before we predicted.
- In case the true value was after the range, let’s say 7 days, then we compute After, meaning that the package was delivered after we predicted.
One of our assumptions is that users would rather receive early than late on what we predicted.
Now that we are happy with our baseline performance, let’s start thinking about running an experiment.
Learning Through Experimentation
We want to understand how users are impacted when they see this information on the ad page, and we can test our assumptions and learn from our users. Some ideas include:
- Baseline: Testing, Baseline vs. Nothing
- UX Design: How the UX can impact users, UX1 vs. UX2
- Broad Ranges: How do users react to seeing two to three days vs. two to five days?
- Speed vs. Date: How users react seeing three days vs. by January 25
Those are some experimentation ideas that we can run, even before training a complex model, that can help us learn something from our users and even impact some choices when we are training and optimizing our machine-learning solution later on. But our overall objective is to have an ML-based solution predicting delivery time estimation, so let us jump into our ML model solution.
Machine Learning Model
With our initial solution in place, we now have a benchmark to gauge the extent of improvement our machine-learning model achieves. It is worth mentioning that machine learning models are powerful tools that enable computers to learn from data and make predictions or decisions without being explicitly programmed. That means that we are increasing the complexity of our initial solution. Hence the increased complexity of our solution should be justified by the improvement in performance compared to the initial solution. Otherwise, sticking with the baseline becomes preferable, highlighting the significance of having a baseline for evaluation.
Regarding machine learning predictions, the two common approaches are batch predictions and online predictions. Let’s talk about them.
Batch or online predictions?
In the context of an e-commerce platform, online prediction would be suitable when we require a feature from users to make delivery predictions. This approach enables real-time predictions based on individual user data, allowing for personalized and up-to-date delivery estimates.
On the other hand, batch prediction would be sufficient when we only need to utilize the features available on the ad page. By calling the model once when the ad page is created, we can process the batch of available data and generate predictions for a group of ads simultaneously. This approach saves computational resources and is suitable when immediate results are not necessary for the specific task at hand.
This choice will depend on many factors, but one is the features that we need when calling the model.
In our case, the distance between the seller and the buyer is an important factor when performing the delivery time estimation, but obtaining information about the buyer while they are on the web page for online predictions can be complex. Therefore, we decided to keep it simple and make a batch prediction, but we can add this feature and change it to an online prediction later.
We’ve trained several different models, and the one that got better performance was the Catboost Model, hence the one we’ll mention below.
Catboost Model
CatBoost is a powerful gradient-boosting framework specifically designed for handling categorical features in machine learning models. It automatically handles categorical variables without requiring explicit feature engineering, making it ideal for datasets with a mix of numerical and categorical features and can be used for a wide range of tasks, such as classification, regression, and ranking. Let’s see our specific use case.
Quantile Regression
We decided to follow the approach of quantile regression. To explain quickly, we will have two different models with the alpha parameter set to 0.05 and the other to 0.95. Instead of predicting the value of the regression, like three days, we are predicting the quantile, meaning that the first model will predict a value that 95% of the delivery time will be above, and the other model will predict a value that 95% is below. And with that, we create a predicted range, with one model predicting the upper bound and the other predicting the lower bound. In this way, we create a predicted range to display on the webpage.
Again, before going to production, let’s have a look at the model performance offline and see how much improvement we obtained compared to the baseline.
Model Performance
- We can see that we improved the performance compared with the initial solution
- We reached 81% in accuracy (+13,3% compared to baseline)
- 11,5% of the packages are delivered early (-11.5% compared to baseline)
- And 7.5% after what we predicted (-1.8% compared to baseline)
We achieved quite a good improvement in the performance of our model compared to our baseline. So now let’s start talking about putting our solution in production.
Productionizing
Productionizing our ML solution refers to the process of deploying and integrating our machine learning model into a production environment, making it ready for real-world use. It involves transforming the model from a development or experimental stage into a reliable, scalable, and efficient system that can handle real-time data and generate predictions or insights as expected.
To take our solution to production, we followed these steps:
- Create a script in Python to download and preprocess the data and train and deploy the model.
- MLFlow for Experimentation Tracking and model registry.
- Docker to containerize the project.
- CI/CD best practices on GitLab.
- Deploy the model using an internal tool called FrejaML.
- Automated preprocessing, training, and deployment using Airflow.
- Create a batch prediction in AWS.
Learnings
- Through Experimentation, we saw that the users use this information to decide to buy an item, and we validate that through our baseline. So we validate the value of our solution and that it is worth investing in training and evaluating a ml model.
- Enhancing our initial solution with the ML model has significantly improved its performance offline. This enhancement is expected to substantially increase the impact we achieve, particularly evident in a higher number of delivery clicks.
What are the next steps?
- Run a new experiment with a new ML model and see its performance in production with real users.
- Add Monitoring to check the model performance in production.
- Scale to other Markets.
Conclusion
In conclusion, this article discussed the use of machine learning for delivery time estimation at OLX.
It covered every step of a data science project, from defining the problem and success criteria to taking the solution to production and identifying the next steps.
The project aimed to improve the delivery time estimation to encourage buyers to buy with Pay&Ship. The lack of delivery time information was identified as a factor in users’ decision-making process, and the exploratory data analysis revealed that the carrier was the longest step in the delivery process. Other factors that were important included the day of the week, region, and distance from the seller to the buyer. We also emphasized the importance of using a baseline to validate the solution and understand its impact.
Overall, the use of machine learning in delivery time estimation improved the user experience and increased the conversion of users who buy with Pay&Ship while decreasing the churn for users who had a bad experience purchasing with delivery.
…
Thank you very much for reading this article, and if you want to know more about OLX, don’t forget to check our website 😃 -> https://www.olxgroup.com/
This article was written by Enderson Santos!
