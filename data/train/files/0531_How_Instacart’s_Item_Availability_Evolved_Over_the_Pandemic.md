# How Instacart’s Item Availability Evolved Over the Pandemic

Источник: https://www.instacart.com/company/how-its-made/how-instacarts-item-availability-evolved-over-the-pandemic/

This is the part-1 of a three-part blog post series in which we outline how we addressed inventory challenges through product, machine learning, and engineering innovations.
A few years ago, we introduced the problem of predicting the availability of grocery items. In the last couple of years, fueled by the pandemic and supply chain issues, being able to get an accurate sense of availability has become table stakes for both Instacart’s customers and the company. In this three-part post, we detail the increased complexity of this problem, the machine-learning innovations that helped us address it, and the engineering infrastructure that powered it.
COVID: the pivotal point
The rise of COVID and customers’ reliance on essential services like Instacart presented a few key challenges.
Demand Surge
As more customers turned to Instacart for their grocery shopping needs, we faced a unique challenge in fulfilling orders. Unlike traditional online retailers, Instacart is a marketplace that allows users to shop from different retailers, while Instacart shoppers go to physical stores to pick up those items. However, this creates a logistical challenge for Instacart to determine the physical availability of millions of items across 80,000+ retail locations, each with their own distinct inventory management systems, to ensure that every item in a customer’s order is fulfilled.
Since Instacart relies on shoppers to pick and gather items for customer orders from the store, limitations in in-store inventory and fulfillment logistics make it difficult to meet the customer’s expectation of receiving every item in their order.
Fast-changing inventory
The pandemic also led to disruptions in supply chains and labor shortages. These changes resulted in rapidly fluctuating store inventory levels, making it more difficult for machine learning models to predict product availability accurately. The model architecture we were using at that time struggled to keep pace with these changes, resulting in a larger discrepancy between predicted availability and the actual outcome of the item being available in the store.
Shopper supply
During the initial stages of the pandemic, Instacart, like many other companies, faced challenges in meeting the surge in demand and needed to increase the number of shoppers on our platform as a result. While we onboarded hundreds of thousands of new shoppers during this time, it was important that shoppers could use their time efficiently to fulfill the high volume of customer orders coming in. The percentage of orders that were canceled because items were out-of-stock (OOS) specifically spiked during the onset of COVID, which in turn led to frustrating experiences for both customers and shoppers. To ensure that we were using shoppers’ efforts efficiently and providing faster delivery for customers, it was crucial to maintain high found rates.
Other crises
Although the grocery market has stabilized since the onset of COVID-19, similar challenges arising from other crises, such as floods in New York, and shortages of baby formula and tampons, among others, still occur on a smaller scale. These situations, though distinct, share a common pattern of problems where the selection-found rate balance is tipped, highlighting the need for scalable solutions to address them effectively. The chart below illustrates the systematic spikes in the percentage of orders canceled because the items are out-of-stock (OOS) during key moments.
Competing Trade-offs
Selection vs Found rate trade-off
Instacart uses a probabilistic approach to inform its customers about inventory availability. Given the difficulty of accurately determining real-time item availability in stores and the ever-changing inventory levels, Instacart relies on machine learning models to estimate the likelihood of shoppers finding specific items in-store. It’s important to note that, despite this estimation, purchased items are not reserved until our shoppers pick them up in the store, a crucial factor to consider when estimating the probability.
Consequently, Instacart faces the challenge of balancing selection, the number of items displayed to users, and the found rate of the ordered items.
If the approach leans towards the conservative side, we might show a smaller selection, which runs the risk of hiding items that are available in the store and potentially eroding the customer’s confidence in Instacart’s reliability. On the other hand, if the approach leans towards the liberal side, we show a larger inventory, which results in a lower found rate and once again undermines the customer’s confidence. Henceforth, Instacart must manage this delicate balance between “selection vs. Found rate” to ensure high customer confidence.
The above graph presents the hypothetical trade-off curve for the selection vs found rate problem. Finding the optimal threshold along this trade-off curve ensures an ideal balance between selection volume and found rate — thereby realizing business goals and fostering customer faith in Instacart. When there are abrupt shifts in item selection or user demand, ML models exhibit a sluggish response as they require ample observations to adapt. While this transpires, the trade-off curve change, rendering the previous threshold suboptimal. By appropriately adjusting the thresholds, we can re-balance the trade-off while allowing the ML models to recalibrate. This allows swift accommodating to changing circumstances while maintaining an optimal balance between selection volume and found rate.
Importance of found rate to long-term retention
Based on intuition and user research, we learned that order quality, specifically found rate, is critical for customer retention. However, we needed to find a way to validate that hypothesis and benchmark for a “good found rate.” The benchmark is important for us to find the optimal zone in the selection-found rate curve for the system to operate in that maximizes customer confidence measured through retention. We conducted multiple experiments and developed analytical models to measure the impact of changing found rate on customer retention. Through this research, we uncovered two key insights that form the core of our work:
- Customers with orders that have a perfect found rate are twice as likely to retain and re-order compared to those with a low found rate.
- This effect is more significant for new customers than for existing customers.
Key Learnings
Fueled by the importance of found rate in solving the above challenges, we learned a few key insights.
Setting customer expectations
Based on our research, we discovered that effectively communicating product availability to customers is crucial for making informed choices.
We achieved this by implementing badges on products that displayed “low stock” and “many in stock.” We also introduced a “Request” button, which informed customers that an item was running low in the store and gave them the option to request the item. As a result of these changes, we observed a significant decrease in baskets containing items with low availability and an increase in orders. We have now incorporated these modifications on the shopper side to streamline their experience and prioritize items that are in high demand.
Real-time availability
We found that we needed to react faster to match the volatility in the store’s inventory.
We found that the shopper’s found/not-found information is a great source of predictive power.
We will cover more about how our ML systems adapted to this as well as how our engineering systems made us use real-time availability in the follow-up posts of this series.
Dynamic Thresholds
Availability plays a critical role in the Instacart ecosystem, affecting customer orders, advertising revenue, shopper efficiency, and more. However, during crisis situations, it is challenging to re-train models to optimize among these metrics.
To overcome this, we developed a complex set of thresholds that operate in conjunction with our machine-learning availability model to determine which items are available for purchase and which items are not.
Thus by changing these thresholds, we can trade off between these metrics without having to train new ML models. Additionally, we implemented the ability to support different thresholds for various segments, such as retailers, locations, and categories. This enables us to perform additional optimizations tailored to specific business needs. We will delve further into the engineering system that supports the dynamic nature of these thresholds in the following engineering systems post.
Future Work
We are still at the onset of making significant strides in solving some of these challenges. These are some promising areas we believe will help us make those strides.
ML improvements
ML continues to be our most promising area of investment in improving our ability to predict in-store inventory. Part 2 of this blog series will talk about future improvements in that space.
More data signals
To improve the long tail and items with high volatility, we are investing in getting more data signals about items in the store and how they are sold and replenished.
Working with Retailers
As a retailer enablement company, the success of Instacart aligns with that of the retailers. We are working with companies like Publix to explore tighter technological integrations to help us with the data signals and other operational ways to improve found rate.
Postface
In today’s fast-paced world, customers expect seamless and reliable service. Because of rapidly fluctuating store inventory levels, achieving a near-perfect fulfillment rate is a crucial challenge for companies like Instacart. This is a unique problem that the industry is in its nascent state, and the complexity is further compounded by the wide variety of products and retailers on our platform. Solving this problem would require a combination of user experience, software, machine learning, data, and hardware innovation, as we closely collaborate with retailers and other partners.
If you are interested in tackling these cutting-edge challenges at Instacart, please check out our open roles.
Hope you enjoyed the part-1 of this series. We will be publishing the part-2, How Instacart Modernized the Prediction of Real Time Availability for Hundreds of Millions of Items While Saving Costs, in a week.
Acknowledgments
Improvements to Found rates by better availability predictions required collaboration across several functions and organizations at Instacart. We would like to thank the following key members that were instrumental in making progress across many areas.
- Product: Joey Loi, Matt Deiters, Nick Turley
- Data Science: Eugene Agronin, Benjamin Knight, Eric Rynerson
- Eng: Damon Ding, Michael Prescott, Yanhua Liu, Thomas Cheng, Frank Chung, Jason Shao, James Liew, Evan Grossman, Deonna Hodges
