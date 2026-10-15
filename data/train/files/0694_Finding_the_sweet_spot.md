# Finding the sweet spot

Источник: https://careers.ocadogroup.com/blogs/careers-blogs/our-technologies/finding-the-sweet-spot

Being able to forecast demand accurately has been the lifeblood of retailers for years. In the world of grocery ecommerce, where the freshness of goods and nuances in customer behaviour add complexity, it's even more critical.
Retailers face a constant challenge. If they don't order enough stock, customers won't receive the items they ordered, leading to lower customer satisfaction. But if they order too much, they have to contend with the lower profitability and stock wastage.
When it comes to striking a balance, preferences vary. One retailer may value availability and fulfilment accuracy for customers, whilst another may want to drive down purge. The challenge is finding the sweet spot.
Neural networks can help
For our Supply Chain and Data Science team, forecasting demand for retailers on the Ocado Smart Platform (OSP) is no small feat. Our team faces the challenge of driving down purge whilst maximising availability for our partners. We need to create accurate demand forecasts and find the best balance for each retailer, and we need to consider differing demand patterns across markets and geographies, along with different retailer business models.
What’s more, the factors driving the demand can change every day. So we need to recalculate all these forecasts regularly. Each automated customer fulfilment centre requires millions of forecasts every day!
To generate forecasts at this scale and frequency, whilst still maintaining the accuracy of human-generated forecasts, we developed a suite of machine learning models built on top of some of the latest research in neural networks.
These models, built in Python and Tensorflow, continuously learn from the most recent data in the Ocado Smart Platform (OSP) and adapt their behaviour over time to account for external factors - such as the coronavirus pandemic, which led to lasting changes in customer behaviour.
We use algorithms of varying complexity, ranging from simple heuristics to advanced sequence-to-sequence deep learning models.
1) Heuristic algorithms
For retail partners new to OSP, we don’t yet have any data we can use to train machine learning models. However, with our experience of forecasting demand for existing retailers, we know there are simple heuristic algorithms we can use that generate reasonable forecasts.
Rolling averages of recent sales help us forecast medium and long term trends in demand. By analysing what customers have already pre-ordered and checked out, we can forecast short term demand very accurately. Using combinations of heuristics such as these, we can provide retailers with meaningful forecasts from the moment they launch on OSP.
2) Simple feed-forward neural networks
Once our retail partners have begun to sell products on OSP, we no longer have to rely on our intuition to decide what combination of heuristic algorithms will provide the best forecast.
Instead, we can look at the retailer’s recent sales to determine this. And because the best combination of heuristics will be a little different for every product and every day we forecast, we use machine learning to automate and optimise this process.
Our simple, feed-forward neural networks take all possible heuristics we could use for our forecasts, such as daily demand, rolling averages and checked out orders. Our neural networks work out the best possible combination for every forecast we make, based upon the recent demand history of the product.
3) Deep sequence-to-sequence neural networks
Our simpler machine learning models do well at identifying and continuing recent trends seen in each product’s demand. However, many external factors can cause these trends to change.
Some of these factors retailers control, such as selling a new product or placing it on promotion. Other factors, such as seasonal events and global pandemics, are outside of their control.
To order the right amount of stock, retailer’s (human) demand planners need to consider all these external factors. And, so to achieve the same level of accuracy, our (AI) forecasting models need to do the same.
Based on some of the latest research in deep learning, our deep sequence-to-sequence neural networks learn to forecast similarly to humans. We can define this under memorisation and generalisation:
i) Memorisation: Models learn to identify and remember information that drives demand and forget information that does not. This means they can look at long sequences of data - months and months of sales, for example - and quickly identify the patterns and features that will determine future demand.
ii) Generalisation: Models learn behaviour across all products. This means they can forecast accurately for new products and promotions based upon the demand they’ve seen for similar products and promotions in the past.
Our deep neural network models for retail partners established in OSP mean we can forecast at CFC-level scale with human-level performance.
Looking to the future
As retailers continue to sign up to OSP, we want to make sure their demand forecasts are as accurate as possible, as quickly as possible. And although our simpler models have performed well for the retailers we have launched so far, we know the sooner we can use our deep neural network models, the better the forecasts will be.
To this end, we are developing ‘general’ neural networks that can learn trends and factors that are common to all OSP retailers. We can use these models to predict demand for any retailer as soon as they launch in OSP, and as we start to collect retailer-specific data, we can fine-tune these models to learn retailer-specific trends.
Looking ahead, although our demand forecasting models are continuously improving, we know their forecasts will never be perfect. To account for this, we are developing models that can estimate their uncertainty. With a better understanding of where future sales are less certain, retailers can adjust their stock levels to strike the right balance between purge and availability.
Change your world with us
Across Ocado Technology, we have a growing, diverse mix of data science teams helping us solve complex problems. Learn more about our full range of opportunities here.
