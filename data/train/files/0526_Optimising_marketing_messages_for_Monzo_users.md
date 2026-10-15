# Optimising marketing messages for Monzo users

Источник: https://medium.com/data-monzo/optimising-marketing-messages-for-monzo-users-3fe805f24572

We’ve been launching several new products at Monzo that serve different financial needs for our customers. We have internal principles that guide teams on the frequency and limit the number of messages that users receive. This ensures we stay focused on maintaining a great experience and avoid overwhelming customers with communications. Different teams, promoting different products and features across the company, will want to reach the most relevant users and maximise the effectiveness of their marketing campaigns.
For that reason, we wanted to select the most relevant marketing message for each customer whilst avoiding overloading customers with communications and learning from the behaviours they exhibit. To achieve this, we built an optimisation algorithm using uplift model’s predictions to decide the most optimal campaign targeting. This approach helped us improve campaign effectiveness, as much as 200%, compared to traditional broad targeting.
📚What are uplift models
Uplift models help us predict the additional response we get from an intervention, like a marketing campaign, compared to no intervention. We can measure the additional response as a binary (e.g. opening a savings pot) or as a continuous value (e.g.: total amount saved).
Uplift models also helps us identify four different types of users:
- Treatment only: users who responded only after being contacted
- Adverse effect: users who don’t respond, if they are contacted
- Sure things: users who “always” respond, independently of being contacted or not
- Never: users “never” respond, independently of being contacted or not
Before building an uplift model, we should run a randomised A/B test. This test needs a group of users who receive the message (treatment) and another group of users who don’t (control). We will later use the results of the A/B test as the data to train the uplift model.
There are different ways to build uplift models and we’ll explain the common ones we’ve used:
- T meta-model: builds two models, one trained using the treatment group and the other using the control group.
- S meta-model: builds a single model, in which one of the variables indicates if the user was in treatment or control group.
Once the models are trained in any of these two methods, we take the difference between the prediction assuming the user is in the treatment group (prediction_1) and the prediction assuming the user is in control (prediction_0) as the “uplift”. We’ve used the library CausalML that abstracts a lot of this process.
Both models predict the same metric, but there are some limitations to be aware of. The T meta-model is prone to over-fitting in the under-laying models. The risk for the S meta-model is that it may disregard the treatment variable if its effect is weak.
In the image below, we can see examples of what we would expect across our different segments for both predictions from the meta models. Users in the treatment only segment would have a higher score and those in the adverse effect would have a negative one. Users in the always or never group would have a score around zero since both predictions are expected to be the same.
🔮Predicting campaigns’ value using uplift models
Before optimisation, we had to train product specific uplift models. To create the training datasets, we included all users and their response from past campaigns of the corresponding product that ran with A/B testing. We used internal data that we considered predictive to train the models and applied some feature selection to avoid overfitting.
We were looking to optimise product values that depended on the metric that each team wanted to improve. For that reason, each uplift model’s target had a different product value that could be either continuous (e.g. amount saved in a pot), or binary to represent a take up rate (e.g. user subscribed to Monzo Plus).
Get Valeria Cortez’s stories in your inbox
Join Medium for free to get updates from this writer.
The uplift model then predicted how much additional product value a user would take after receiving a marketing campaign compared to not receiving any (e.g. what additional amount a user would save in a pot, if campaign sent).
🖥️ Simulating campaign results with optimised assignment
A common optimisation problem looks at maximising or minimising a single function while following certain constraints, e.g.: maximising revenue while keeping costs under certain levels. In our case, we were looking to improve multiple objective functions, since each product had a different type of metric. We call this multi-objective optimisation. For this, we reviewed all eligible results and agreed on outcomes based on business needs using the process we describe below.
We first had to define how to prioritise campaign messages for each user. We decided to assign a user for one product over the other, if the first uplift prediction was t times greater than for the other product.
The parameter t can range from 0 to a very large number. Its purpose is to regulate how many messages for one product are sent over another, e.g. if t is very large, more users would receive the first product message and vice versa. We’d need to include additional parameters if we were to add more products into this exercise (for simplicity, we’ve used two products in the example in the graph below).
We would then simulate the campaign results using different t values as seen in the graph below. The dots show us the campaign results for each different value of t. We’d eventually select a t value that:
- increases additional product value for each campaign
- meets campaign goals from each product team, including user reach
🧪Running a controlled experiment to measure impact
To measure the effectiveness of our optimised approach with uplift models, we ran A/B tests to compare it with the existing approach. To do this, we randomly allocated users into three different samples based on campaign assignment strategy:
- Treatment (Random): users in this sample were later assigned randomly to a product’s campaign
- Treatment (Optimised): users in this sample were later assigned to a product campaign using the optimised approach
- Control: users in this sample didn’t receive any product message
We kept the control group to calculate the uplift between sending a campaign (treatment) and doing nothing (control). As time passes, the accuracy of the uplift models may degrade, so we can use the new treatment and control datasets to refresh the uplift models.
From the experiments, we saw that larger campaigns had a higher absolute increase in uplift since we were reaching more users. However, smaller campaigns had a higher relative increase in uplift, since fewer customers received a message from a much larger pool of eligible users.
🌰 In a nutshell
Overall, we were aiming to boost the effectiveness of our marketing campaigns to promote the products that would better meet our customers’ financial needs. We built uplift models to capture user preferences towards our products and used them in a multi-objective optimisation problem to enhance campaign targeting. This helped us improve campaign performance, by as much as 200%, compared to traditional targeting.
👩💻 Come and join us
If you love working on these types of data challenges, you should come and join us! We’re hiring for several roles in our data team, including:
