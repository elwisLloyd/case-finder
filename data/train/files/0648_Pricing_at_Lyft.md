# Pricing at Lyft

Источник: https://eng.lyft.com/pricing-at-lyft-8a4022065f8b

By Yanqiao Wang
Introduction
Pricing forms the backbone of the Lyft’s marketplace system, which is core in the journey of improving people’s lives with the world’s best transportation. In general, the goal of price optimization is to find the price that balances supply and demand while covering the expenses necessary to provide an easy-to-use rideshare platform, where drivers have tremendous influence on the rider prices through their entry and exit on the platform. Specifically, we strive to find rideshare options and prices that are:
- Reliable: balance consistent prices and pickup times across repeated usage;
- Fair: any two riders see the same price for the same ride intent with a clear explanation otherwise (e.g. one rider has a Lyft Pink membership);
- Competitive: efficient pricing to remain competitive compared to other transportation options.
In this blog post, we discuss the rideshare pricing system architectural design, modeling approaches and potential future iterations of Lyft’s pricing engine to illustrate how we tackle price optimization to achieve Lyft’s long-term mission.
System Design
From the system design perspective, there are three layers of the stack:
- Pricing Orchestration: a configurable engineering platform with fast iterations for precise execution to support algorithms and operations;
- Pricing Operations: a process and supporting toolkit to ensure prices are competitive;
- Algorithmic Pricing: a plug-in-play model library designed for consistent backtesting, experimentation, and productionization of automated data-driven decisions pursuing fair and reliable prices.
All three layers work seamlessly together towards a unified goal for the long-term success:
We will introduce how each layer works in the following sections.
Pricing Orchestration
In pricing orchestration, we built a robust platform that ensures a rider’s price is stable as they consider their options and that ensures prices for similar rides are consistent between riders. The platform also encapsulates all of the business logic for determining the market price and generates a traceable history of each pricing decision.
In this platform, we leverage multiple technologies:
- Infra: Flink, Flyte, Spark, Redis, Dynamo, Hive;
- Modeling: Tensorflow, Reinforcement learning, Neural Network, Linear regression, Convex Optimization;
- Programming & Serving: Python, Flask.
The overall architecture design is as below:
Each component has a distinct responsibility:
- API Layer: a set of endpoints that provide access to market signals and session-level information;
- Cache Layer: provides price stability and consistency, as well as, reduce latency via user and route caching;
- Calculation Layer: acts as an ingredient manager that fetches information from the cache layer (e.g. estimated travel time and distance, estimated tolls and venue fees) and executes the price calculation according to a list of step-by-step procedures for each rideshare option;
- Storage: a GDPR/CCPA-compliant price quote store having highly reliable, efficient and low latency storage that records details of the price like: request, ingredients, line items and price quote ID.
Pricing Operations
Pricing operations include strategic and tactical operations, which work harmoniously with pricing algorithms to drive both financials and growth.
Get Yanqiao Wang’s stories in your inbox
Join Medium for free to get updates from this writer.
Algorithmic pricing needs two types of guidance from pricing operations:
- Strategic Guidance: how to optimally consider trade off among multiple business goals (financial, growth and service levels);
- Tactical Guidance: how to tackle special use cases (e.g. airport and venues) in the overall system.
Algorithmic Pricing
We have built a large-scale real-time pricing algorithm by leveraging causal inference, machine learning and operations research methodologies. This design enables faster experimentation and system evolution, which is particularly crucial given the market volatility and marketplace dynamicity.
In general, the unified algorithmic pricing includes structural pricing and dynamic pricing with a near real-time feedback loop:
The structural pricing component serves as the foundation of pricing optimization at Lyft, in order to maximize the passenger long-term value taking ride level characteristics (location: origin and destination, estimated travel time and distance, timestamp and ride type) as inputs. Dynamic pricing aims for optimizing the entire rideshare network by looking at both riders and drivers to improve the throughput of rides. As soon as drivers sign on or off and riders check the Lyft app, the dynamic pricing algorithm starts counting and gathering input signals, and then trying to find a reasonable balance between demand and supply. The process is that drivers’ entry and exit onto the platform influence the pickup times, affecting service quality, such as cancels, lapses and driver utilization, which in turn impacts dynamic pricing’s throughput of rides by influencing riders’ conversion rate (check out this blog post for more details).
To handle the dynamicity, we adopt an “offline training, online learning, and real-time evaluation” design principle, where we train the input signals generation model based on causal inference and machine learning in an offline setting, then simultaneously correct the potential bias of input signals, correct for market management inefficiencies, and optimize for the multi-objective goal using online reinforcement learning and off policy evaluation, in which one learns about a policy different from the policy that generates the data. Visually, the flow looks like this:
Online Pricing with Reinforcement Learning
As you can see, we handle the market volatility by building flexibility into algorithmic pricing and, specifically, online reinforcement learning enables the platform to support multi-objective, non-parametric decision making. Let’s dive in.
Pricing is a difficult problem because it is difficult to estimate how a price change today would impact the market, especially given the market volatility we have experienced over the last couple of years, and because even if one could estimate the demand response to price changes, the response is likely to be non-linear across the many different rideshare options which makes price optimization computationally challenging. Online pricing with reinforcement learning (RL) addresses these challenges by using continuous A/B tests on small price changes to identify the right price for the current marketplace dynamic conditions by processing a wide range of market and business inputs.
A general online reinforcement learning workflow would look like this:
We have successfully applied this technique to our algorithmic pricing component. As mentioned before, we use off-policy evaluation to warm-start prices and have for awhile, but what’s new with online reinforcement learning is that, in near real-time, we process transaction ride data as raw data to update the pricing policies (Selection & Action) based on the realized pricing goals (Reward) and can be more robust to market instability (State) changes in the marketplace.
What’s Next?
To summarize, we have discussed pricing’s mission, reviewed different engineering, operations and algorithmic components on the system level, then briefly illustrated how online RL contributes to pricing. The next step would be to apply the hierarchical RL design for the long-term value maximization and system unification across and beyond marketplace optimization.
Are You as Excited as We Are?
Interested in operations research, reinforcement learning, causal inference, experiment design, applying science at scale and helping push the boundaries of data-driven decision-making in rideshare, or working at Lyft in general? Check out our job posting or university program pages. If you find this blog interesting, don’t hesitate to reach out via email.
