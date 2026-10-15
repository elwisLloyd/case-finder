# Causal Inference — Estimating Long-term Engagement

Источник: https://medium.com/mercadolibre-tech/causal-inference-estimating-long-term-engagement-fac517929073

Causal Inference — Estimating Long-term Engagement
Measuring the impact our models generate in the business can be as complex as training and deploying them
User loyalty is an issue that concerns all e-commerce companies; just a tiny fraction of the best users generate most of the revenue. This is why taking care of these users is so important to the business; thus, the need to measure the impact of the efforts made to retain the sensitive segments.
In the Marketing Science Team at Mercado Libre, we have several issues such as budget allocation, channel attribution, life cycle, and cross selling. These issues call for a number of machine learning predictive models that help us take prescriptive actions to optimize KPI’s in the long term. By working intensely with the operations team we are able to bring these models to life persuading our users through different channels (push notifications, email, paid media) that we operate as effectively as possible. This is not the end, though, since we are also in charge of measuring success in terms of the impact and efficiency of the actions taken, and it is this point we will be focusing on through this post.
As part of the customer life cycle, we want those users who showed good behavior in the past to keep it over time. In order to foster this behavior, we have developed a predictive model that allows us to take early actions on valuable users who are close to drastically reducing their future life time value (LTV). The measurement of the increase we generate on the business in the long term, when compared to no action taken, becomes complex since the effects are diluted over time. This makes it necessary to apply techniques to infer the causal effect.
Understanding the Problem
Before discussing the technical details, it is necessary to understand why it is so difficult to speak about retention at Mercado Libre, the most important e-commerce in Latin America.
- Problem 1: There is no contract concept, so there is no certainty whether the user will buy again.
- Problem 2: We do not know how many times the user will buy again. Even worse, the nature of all e-commerce purchases is determined by a strong exponential distribution; that is to say, many users buy little and only a few buy a lot.
This being said, it is necessary to predict if a user is going to reduce their purchase frequency in order to take preventive action and avoid losing their engagement. For this purpose, we have developed the following strategy:
Our top users are injected into a prediction framework of “engagement loss” (loss of commitment or relationship with the brand), i.e., those with sufficient probability to take an action are stimulated by means of a notification with a smart discount coupon benefit in the app. Finally, we move on to the causal inference stage to measure the effect of the stimulus, where we seek to quantify the retention and the incremental growth in the users’ purchase frequency by measuring the accumulated impact over time. Due to the nature of the marketplace, we will have to wait some months until we can measure the effect of incremental growth.
The KPI’s to be followed will be the frequency and the incremental revenue in the long term. This will allow us to answer questions such as:
- What is the net worth of a buyer we manage to retain?
- How many more times will they incrementally buy?
- What is the net profit this action allows us to generate?
Measurement
The measurement of the causal effect we generate when we take an action can be thought of (from a simplistic point of view) as the difference between the effect generated in the users we stimulate versus the one in the users we do not stimulate. In technical terms, it would be:
- Users we stimulate: Test Group
- Users we do not stimulate: Control Group
- Stimulus: Treatment (to give a gift in a marketplace, a pill in medicine, etc.)
- Effect we generate: Outcome. Y(1): outcome when the user receives the treatment. Y(0): outcome when the user does not receive the treatment.
The road to causal inference requires a conceptual understanding of the issue we are tackling and the conditions in which we operate. It is only by way of a conceptual approach that we will outline the three problems we could be faced with if we had a control group at our disposal.
The dotted line indicates that when we do not have a control group at hand; there are other techniques potentially applicable that are beyond the scope of this article, such as difference in difference, causal impact (BSTS: Bayesian Structural Time Series) or synthetic control.
The Magic of Randomness — Randomized Controlled Trials (RCT)
It is always a good start to clarify the importance of being able to make a measurement with randomized groups and the advantages it implies. Not always do complex solutions lead to better results. In other words, whenever it is possible to solve a problem with an A/B testing, do not hesitate. Just go along!
Choosing the groups randomly ensures that all the covariates before the stimulus will be kept in the same proportions for both test and control groups. In our case, we will have the same proportion of Android/IOS users, visitors/non-visitors, checkout abandoners, etc… This means there is no covariate that determines which group our user belongs to.
As mentioned at the beginning, in the Marketing Science Team, we measure our success on the basis of the incremental we generate in the KPI’s with respect to what was being done. How is this defined? By Average Treatment Effect (ATE). ATE = E[Y(1)] - E[Y(0)] where Y(1) is the potential outcome each individual would have when stimulated and Y (0) when not stimulated. The problem of causal inference is that the same person cannot be stimulated and not stimulated at the same time (counterfactual), but fortunately, when we generate random groups, this issue is reduced to:
ATE = E[Y(1)] — E[Y(0)] = E[Y|T=1] — E[Y|T=0] which can be simply extracted from data such as the mean difference in the groups.
Instrumental Variables (IV)
This will be our turning point to justify what we will analyze in the following points. In the case of Mercado Libre, push notifications sent to the app have several stages since a person can receive the push, see it, open it and buy. That is to say, we would like to measure the effect on those who were really stimulated, for the stimulus should change behavior over time.
There is a method called Instrumental Variable (IV), which allows us to calculate the incremental effect with respect to the ones who received the stimulus. This effect is called Complier Average Causal Effect (CACE).
CACE = E[Y(Z=1) — Y(Z=0) | T(Z=1) = 1, T(Z=0) = 0]
Under certain criteria met in short-term measurements, CACE results in Intent To Treat (ITT) adjusted by the proportion the treatment took (Wald Estimator).
In other words, we want to calculate our ATE, but for compliers.
The causality graph above describes the causal relationships between the instrumental variable (the assignment to the test and control groups is random, so there is no relationship with exogenous variables) that determines those who can end up getting the stimulus (if Z = 0, then T = 0). Taking the treatment depends on external variables such as whether the user is opted out if there is poor Internet connection, etc..
One of the methods to measure CACE is by using the 2SLS technique, made up of two steps: first, we estimate T = f(Z) to break the link between U and T; then, we estimate Y = f(T) since T is not related to U.
When we put this into practice, we see the impact is diluted as days go by. We can see this in the sinusoidal behaviors and the sudden increase in the last 20 days that is explained when we look at the p-value of the regression of stage 1 of 2SLS. This means that our instrumental variable loses its persuasive power and its effect is diluted in time, thus invalidating this measurement methodology.
Why does this happen? The proportion of users that take the treatment is lower than 5% so the ITT is easily distorted with the remaining 95% of the test group.
Observational Study
Upon evidence that in the long term it is not viable to work with low proportions of persuaded users (those who receive the treatment) with randomized experiments, we decided to estimate the counterfactual of the persuaded users taking the control group as a reference, so as to answer the question “what would I have done if I hadn’t taken the stimulus?”. In this way, we turned the RCT (Randomized Controlled Trials) into an observational study.
CATE = E[Y(1) - Y(0) |X=x]
This methodology implies conditioning the test group we have randomly chosen and only keeping the ones that took the treatment versus the whole control group. In this way, we break the magic of randomness. As mentioned earlier in RCT, in order to make a fair comparison without bias, all the past covariates should be equal for both groups.
Let’s see what happens now when we look at the historical purchase frequency prior to the stimulus.
As with other issues, the users who take the treatment are better buyers than the average because the most experienced users are the ones who usually interact with the platform with more frequency than the rest. This means that the comparison is not fair and should be adjusted. We will use this real example throughout this section as a simplified version of the problem to be tackled.
Get Pedro Zenone’s stories in your inbox
Join Medium for free to get updates from this writer.
In this path, it is necessary to:
1- Identify the causal graph
As in the previous sections, it is important to identify the causal relationships that link the covariates with the treatment assignment and the outcome. This will allow us to understand where there are blockages and passages in the relationship.
In order to better understand this last point, let’s go back to the previous example, in which we showed that the users who took the treatment had been buying more. The causal graph is as follows:
The covariate Past Frequency is called confounder because it opens a relationship passage that does not allow us to make a direct relationship between the test group and the control group. If this were the only confounder, the solution would be very simple since we should compare the users of the test group with the ones of the control group that had the same past frequency and make up for the differences in proportion. In this way, we would be able to block the confounding association.
Taking the complete case, there are several possible covariates that could help us explain the causal relationships, and at the same time, they could be related to one another. This is why the causal discovery techniques make this easy; they allow us to obtain the relationship causal graph. This process starts with the search for the skeleton (Markov Equivalence Class) where we identify the associations but as this graph is not yet directed, we will orient the relationships using the GES algorithm.
2- Estimate incremental metrics and choose the best fitting estimator
This point aims to solve the problem of missing counterfactuals and confounder bias. In order to understand this, let’s try to answer two questions that arise from the previous example, where we only took the past purchase frequency as confounder.
Missing Counterfactuals. What would happen if there were frequency values in the test group but not in the control group? machine learning models come to solve this problem by estimating these missing values
Confounder Bias. What would happen if the test group had a higher proportion of users with 6 purchases more than the control group? We would be making an unfair comparison among users who were already better than average — this bias must be made up for. That is why there are different techniques to tackle this problem, which can be divided into:
- Re-weighting Methods: They consist in assigning a probability to the users of the control group to belong to the test group (propensity score). This will be used to make a weight comparison to overcome the selection bias, e.g.: IPW.
- Distance Methods: The propensity score is calculated on the basis of proximity algorithms, e.g.: Matching, Stratification.
- Meta-learner Methods: They perform estimation in two steps: (1) Estimate the conditional mean outcome E[Y |X = x] so the prediction model learned in the previous step will be the base learner. (2) Derive de CATE estimator based on the difference of results obtained with the model from step (1). E.g.: X-learner, T-learner, S-learner.
Unlike the classical machine learning problems where we have a clearly defined target in which we seek to make predictions as well as possible to then validate ourselves against a test group, in the causal inference we are not this lucky because we do not know the ground truth of what we are out to measure. It is crucial to understand what will be measured and what would be anomalous behaviors in order to decide on the best estimator for our needs. In this case, we will show several estimators. We will do away with some of them by mere inspection and then decide from among the candidates by applying the measurements on two experiments performed in parallel. We will decide on the one that shows the most stable results.
The graph shows different estimators:
Biased: It is the limit case where we compare the group that took the treatment with the whole control group. We can expect the rest of the estimators to correct the bias we are adding, since those users who took the treatment are better than average.
Matching: Propensity score matching.
Start: Propensity score stratification.
Lin: Linear regression.
LRS: X learner estimation using linear regression.
T,X,S: Meta learner using gradient boosting as the base model.
IPW: Inverse probability weighting.
Instrument: Estimation using IV explained above.
The first estimator discard is carried out from the previous line graph, where the top extreme case is represented by the dummy Biased estimator. We can expect the estimators to compensate for the differences in the covariates so that the estimate is less biased. On the other hand, the bottom extreme is represented by the case of IV which, as stated above, was losing inference power as days went by.
We can see that Matching, Lin and Start cannot remove the biases and show CATE values very close to Biased. If we continue with X,T,S, we notice that they fluctuate considerably over time, which suggests that they are not very stable. This leaves two estimators to define: IPW and LRS.
At first sight, we cannot make this decision. We need another point of view. A way of making this test is to take random groups, send them the same stimulus and proceed with the measurements. If the estimator is robust, the results should be the same in both groups.
In our case, we ran an experiment in which we had three groups randomly selected and a control group. We stimulated them with different amounts of discounts every 15 days:
- Group “1 DISC”. Receives 1 discount on day 0.
- Group “2 DISC”. Receives 2 discounts on days 0 and 15.
- Group “3 DISC”. Receives 3 discounts on days 0, 15 and 30.
It is to be expected that in the first 15 days, the three groups have the same CATE. Then, when the second discount is sent, the other two groups should also have the same CATE during the following 15 days. The LRS estimator captures this effect, while the IPW shows differences in identical groups given the same stimulus and therefore, we dismiss it.
3- Validation of estimator robustness
Once we choose the best estimator, we must validate its robustness. To do this, we stress the model by applying the following tests::
- Placebo Treatment: What happens to the estimated causal effect when we replace the true treatment variable with an independent random variable? (Hint: The effect should drop to zero.).
- Add Random Common Cause: Does the estimation method change its estimate after we add an independent random variable as a common cause to the dataset? (Hint: The results should not change.).
- Dummy Outcome: What happens to the estimated causal effect when we replace the true outcome variable with an independent random variable? (Hint: The effect should go to zero.).
Conclusions
Through this real case of use, we’ve managed to show the complexity of measuring the effect of our actions in the long term and demonstrate that without this technique, we could have fallen into two different scenarios:
- Analysts without any knowledge on measurement would have chosen biased metrics, which leads to higher results. This would imply an unrealistic profit report to the business.
- Analysts with domain knowledge would have chosen a measurement with instrumental variables, which leads to lower and not very repeatable results. This would imply to report that the initiative of valuable user retention is not very profitable, and this goes against the gold standard of marketing.
As stated earlier, measuring the impact our models generate in the business can be as complex as training and deploying them. To sort this out, from a technical point of view, we have shown the cases in which it is necessary to resort to causal inference and how to approach it, bearing in mind that we must always evaluate several estimators and validate the robustness of the one we choose.
Acknowledgements
- Cristian Calla for pushing to improve day by day.
- Operations team and Field marketing for making this happen.
- Barbara Michalla for general coordination assistance and Cecilia Sassone (editor).
