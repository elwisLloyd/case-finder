# Forecasting something that never happened: how we estimated past promotions profitability

Источник: https://medium.com/artefact-engineering-and-data-science/forecasting-something-that-never-happened-how-we-estimated-past-promotions-profitability-5f55cfa1d477

Forecasting something that never happened: how we estimated past promotions profitability
A guide on how to use counterfactual forecasting to estimate the cost-effectiveness of past in-store promotions in retail.
TL;DR
During a 3-month real-world project, we developed and industrialised a counterfactual forecasting model (first using Prophet, then XGBoost) in order to assess the performance of past in-store promotions of a store chain, to help demand planners in their choices of promotional campaigns.
This model is trained and then forecasts hypothetical sales (called baseline) in the past if there had not been any promotion. The difference between the actual promotion sales and this baseline gives the incremental sales, that we call uplift.
Thanks to hand-crafted temporal features, we reached a forecast accuracy of almost 90%.
Business context
When planning future promotional campaigns, demand planners need to decide which product assortments will be discounted, with a certain promotional mechanism (e.g “-15%”, “buy 2, get 1 free” etc…)
These are difficult decisions as:
- Opting for too many promotions would not be an effective strategy (customers will get accustomed to promotions and tend to wait for the next one).
- Choosing the wrong promotions would result in shortfalls and losses.
For most retail companies, the campaign choices are made based on their business knowledge and the performance of past promotions. However, the “performance of past promotions” is difficult to estimate. Indeed, promotional campaigns do increase sales (in most cases), but how to estimate the efficiency or Return On Investment (ROI) if we do not know what would have been the sales without a promotion? This hypothetical value of the sales with no promotion can be called a baseline. In other words, it is all about being able to estimate the incremental sales (or uplift) of a promotional campaign, corresponding to the actual sales, minus the baseline.
To answer this question, we built a tool which was able to estimate the promotional sales uplift of past campaigns, with an accuracy of almost 90%.
This task is quite challenging as the goal is to make forecasts of hypothetical sales in another situation (here, if the promotional campaign had not occurred for a given product). This can be called “counterfactual forecasting”. This article is mainly based on our experience on a project we did for a French store chain.
Its purpose is to describe the approach we used, give tips and caveats when implementing a counterfactual forecasting solution (data preparation, modelling), explain the evaluation process and finally discuss the limits and next steps to this approach.
What is counterfactual forecasting and why is it difficult to predict?
Counterfactual forecasting is the process of predicting something in the form: what would X be like had there been no Y. In our use case, X would be the sales and Y would be a promotional campaign.
There are actually multiple fields where this process can be applied: stock shortage (estimate the shortfall due to out of stock items), any special events which do not last too long (Covid: does not work!) in order to have enough data to estimate that counterfactual.
The promotion problem can be tackled on 3 angles (sorted by ascending difficulty):
- Understanding past promotions: estimating with a thorough approach the performance (sales uplift or ROI for instance) of previous promotion campaigns.
- Predicting the performance of future promotion campaigns given their characteristics (discounted products, start & end dates, mechanism…)
- Optimising the promotions plan: finding the best setup of future promotions to maximise a business metric.
In this article, we will focus on the first step as it was the objective of our project. However, we will give a few insights on how to tackle the next two ones, in the following sections.
There are two main reasons which make the task of counterfactual forecasting a challenging process:
- There is a paucity of literature or examples on the topic while it is very useful in retail and other industries.
- In counterfactual forecasting, there is no ground truth, as it is something which did not happen. Thus, the performance assessment seems quite difficult (fortunately enough, we came up with an approach which will be presented in the Evaluation section).
Proposed approach
The approach we used to build our tool is the following:
- Train a forecasting model on out-of-promotion dates, to learn a baseline of what sales should look like without any scheduled promotions.
- Predict on all the data points (actually, only the predictions during the promotion are used but it can be good to keep the predictions everywhere for the sake of interpretation).
- Compare that predicted baseline to actual sales during each promotion to infer its uplift.
Important note: The goal is to use the forecasts during the promotion periods, which are in the past. It is because this task is an a posteriori analysis that, contrary to classical forecasting, it is possible to train on dates which are after the inference period, corresponding to the promotional campaign. There is no notion of data leakage here as we try to explain a phenomenon that happened in the past. Thus, the training — inference workflow looks like this:
Implementation
Preparing the data
To tackle the promotion problem, one must use the proper data format. Usually, we have access to two types of data:
- Promotional data (descriptive information related to promotions)
- Sales data.
The preprocessed data is basically sales data, enriched by promotion information (left join, see figure above). Every row with a non-null “Promo type” corresponds to a day where the product is in promotion.
Before doing the first implementation, it is important to assess the data quality. Here are a few guidelines for the checks to perform:
- Look for major issues in the time series:
- Intermittent and/or very low sales (it will be hard to learn a baseline).
- Promotions last too long and/or are too frequent (thus, not enough data points to train on).
- Some products are in multiple promotions at the same time (which promotion is responsible for these incremental sales?)
2. Define a granularity for the use case:
- Time granularity: will the analysis be daily or weekly?
- Item granularity: one time series by article? By family of articles? Sometimes, you won’t be able to reduce the granularity if the number of units sold by time element is not high enough or if the time series is too intermittent. The aggregated sales will be smoother, with less volume issues but they will sometimes lack interpretability.
So, if the time series are clean enough, a good starting point is to take the most granular approach (e.g. product X day, especially if working with Prophet, as we did in this project).
3. Having a clear promotion scope: which products/families of products are part of a given promotion? Are the promotions planned at a national level? (if not, one may not for instance aggregate the sales of a product across all the stores of a country.)
Get Luca Serra’s stories in your inbox
Join Medium for free to get updates from this writer.
Once the data has been checked and prepared, it is time for modelling.
Modelling
First iterations and key takeaways
We started our first iterations with Prophet because it enabled us to have a baseline very quickly, easily add regressors, and interpret the results naturally (thanks to its additive decomposition).
Here is a summary of the main iteration improvements we had during the project:
Basically, the main improvements were coming from the regressors we added:
- The handling of special events (Black Friday was specifically important)
- Temporal lags (even if Prophet model is autoregressive, we added past sales and future sales lags which has proven to be quite useful for the accuracy of the model).
Finally, adapting the way we measured forecast accuracy (see Evaluation section below) also helped to have a more accurate way to assess the performance.
Why did we switch to XGBoost?
Despite Prophet good performance and interpretability, we realised that XGBoost was most suitable, for multiple reasons:
- We had more than 1000 time series thus meaning more than 1000 Prophet models to train.
- Prophet has trouble understanding non-linear relationships between features and their impact on the target. This feature cross issue is well described in this article.
- We reached the same performance while reducing by a factor of 10 the training time.
Evaluation and limits
Evaluation
As written above, there is no ground truth in counterfactual forecasting, which makes the performance assessment more complex than for classical forecasting.
However, we found a way to measure our performance, or rather estimate it as precisely as possible. Here is how:
In classical forecasting, we typically measure performance using a cross-validation strategy (here, expanding window) on a certain validation period (e.g. last year of available data). For this validation period, the actual window where we measure the performance is shifting in each fold (“evaluation window”), and the anterior data is used for the lag features (“Data used to make predictions”). In a promotion use case, we add some data after the evaluation window to reproduce the training — inference workflow described in the “Proposed approach” section.
We can thus apply this cross-validation strategy on the subset of data where there is no promotion, with the Forecast Accuracy (FA) as a metric.
With this approach, we were able to reach a forecast accuracy of almost 90% with a granularity at the level family X day, which is a decent performance, comparable to what we achieved on other projects on classical forecasting.
Even though this performance can be satisfying, our approach has some limitations.
Limits
- First, some external factors are not considered. For instance, media campaigns. These external factors may have a (positive) impact on sales and thus we might overestimate the uplift generated by the studied promotion.
- Secondly, the case of long-lasting promotions: Indeed, it removes an important number of dates from the training dataset.
- Last but not least, the overall promotion impact could be improved taking into account multiple effects such as cannibalisation, halo effect, anticipation/storage effects, which are detailed in the last section.
Going further & next steps
Improving the modelling
Several effects could be added to measure the net impact of a promotion :
- Cannibalisation: The fact that a product is in promotion and thus more attractive will impact negatively on the sales of a similar product.
- Halo: The fact that a product is in promotion and thus more attractive will impact positively on the sales of “frequently bought together” products.
- Anticipation: Customers buy less of the discounted products before a promotion, knowing prices will be more attractive.
- Storage: Customers buy less of the discounted products after a promotion, having bought more goods than usual during the promotion.
The first two effects were not included in our analysis because of the chosen granularity (family level) and the two last ones were hard to quantify thoroughly with the time we had for this project.
To summarise, the net additional sales of a promotion could be represented with this waterfall:
Going beyond the a posteriori analysis
As stated earlier, once the (posterior) analysis of past promotions has been done (stage A), it is then possible to go further by predicting the profitability of future promotions (stage B) and finally propose an optimisation of the promotions plan (stage C).
Of course, predicting (an estimation of) the future profitability of a promotion is harder than estimating the profitability of a previous promotion because we have no data available around the promotion. The idea is to reuse the model developed in stage A using data which is not historical data but forecasted data from a classical forecasting model, as follows:
First, train the classical forecasting model on the available data (until today):
Then, make the predictions with this model (the period to be forecasted must cover the range of temporal features which will be used by the “baseline model”):
Finally, use the trained baseline model using temporal features based on the forecasts of the first model and estimate the baseline, which will give the sales uplift:
Of course, this process has more uncertainty by construction, given that the errors from the two stacked models will be correlated.
Finally, to be able to optimise the promotions plan, the strategy consists in using what has been done for the previous stage to choose the best combination of promotion parameters in order to optimise a business metric such as the ROI.
Conclusion
Using counterfactual forecasting to solve business problems is not a common task that can be found in the literature.
However, we saw that it could be a powerful tool to tackle the problem of assessing thoroughly the performance of past promotions, by forecasting hypothetical sales (baseline) if there had not been any promotion. We also explored recommendations for feature engineering for an autoregressive (Prophet) or gradient boosting (XGBoost) model. Finally, we detailed some guidelines to refine the analysis even more and also go further than just doing an a posteriori analysis.
Thanks to the fellow data scientists who worked with me on this project: Kasra & Ombeline. Thanks also to the Artefactors who proofread this article.
