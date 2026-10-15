# Building Lyft’s Marketing Automation Platform

Источник: https://eng.lyft.com/lyft-marketing-automation-b43b7b7537cc

We take pride in our mission to improve people’s lives with the world’s best transportation. More than 50 million carbon neutral Lyft rides happen every month across the US and Canada — and we’ve barely scratched the surface in the potential for rideshare.
Part of our growth is improvements in our acquisition process — like launching region-specific ad campaigns that increase awareness, and consideration of our multi-modal offerings. Coordinating these campaigns to acquire new users at scale has become time-consuming, leading us to take on the challenge of automation.
Growth Acquisition
Acquisition is typically led by a data-driven cross-functional team that focuses on scale, measurability, and predictability. You may have seen Lyft ads like these:
Acquisition operates at the top and largest part of the onboarding funnel, through the various channels listed on the left. No two channels are created equal: we work with different partners, technologies, and strategies to make sure that Lyft is the top choice for consumers. Other teams at Lyft focus on different parts of the user journey to provide a world-class experience. A high-level view is shown below.
Motivation
Acquiring users at scale means making thousands of decisions each day, for each region where Lyft operates: choosing bids, budgets, creatives, incentives, and audiences; running tests; and more. Just keeping up with these repeated tasks occupies a great deal of marketers’ mindshare and can lead to suboptimal decisions. It’s expensive to the business and does not scale.
By automating routine decisions, we can scale efficiently and create a data-driven learning system. This also lets marketers concentrate on innovation and experimentation instead of operational activities.
Path to Automation
Our goal: build a marketing automation platform to improve cost and volume efficiency while enabling our marketing team to run more complex, high-impact experiments.
Requirements:
- Ability to predict the likelihood of a new user to engage with our product.
- Measurement mechanisms to allocate our marketing budgets across different internal and external channels.
- Levers to deploy these budgets across thousands of ad campaigns.
Marketing performance data contributes to a feedback loop to constantly nourish the reinforcement-learning system.
Here are examples of problems we needed to automate:
- Updating bids across thousands of search keywords.
- Turning off poor-performing display creative.
- Changing referrals values by market.
- Identifying high-value user segments.
- Sharing learnings from different strategies across campaigns.
And so, we created Symphony — an orchestration system that takes a business objective, predicts future user value, allocates budget, and publishes that budget to drive new users to Lyft.
Architecture
The Symphony architecture consists of three main components: lifetime value (LTV) forecaster, budget allocator, and bidders.
Our tech stack comprises Apache Hive, Presto, an internal machine learning (ML) platform, Airflow, and third-party APIs. A light front-end feeds in business targets and launches creatives. The architecture has a lot of moving parts and dependencies and requires rigorous logging and monitoring. We dive deeper into each component below.
Lifetime Value (LTV) forecaster
Understanding the potential value of a user is critical to every business. The goal of this component is to measure the efficiency of various acquisition channels based on the value of the users coming from those channels. Budget can then be allocated based on the expected value for users coming from a given channel and the price we are willing to pay in a particular region for those types of users.
The above diagram portrays at a high level how we calculate a user’s expected LTV while accounting for supply and demand in our two-way marketplace. We try our best to predict LTV accurately, as it helps us set mid- to long-term strategic goals.
Early in the user’s lifecycle, it is hard to get a sense of their retention, rides, or transaction value, so instead of attempting to measure LTV directly, we predict it from historical data. The forecast improves as the user interacts with our services.
The benchmark here represents average expected LTV from a cohort of users. These forecasts feed into the budget allocator and help it decide the value of users that come from a specific set of campaigns.
Budget allocator
The budget allocator collects marketing performance data in conjunction with LTV forecasts. Budget allocations are done using Markov chain Monte Carlo (Thompson Sampling). A curve of the form LTV = a * (spend)^b is fit to the data assuming a & b come from distributions with their own parameters (e.g. a comes from a distribution with mean μa and standard deviation 𝜎a ). Here’s the trick — we don’t try to estimate a & b directly as you would in standard regression. Instead, we estimate the parameters of their distributions: (μa, 𝜎a) & (μb, 𝜎b). Consequently, instead of drawing a curve with fixed a & b, each day we sample a different estimate of a & b from these distributions — naturally injecting a degree of randomness into our cost-curve creation process.
This type of random searching may seem wasteful, but modest exploration is actually optimal in the long run. It helps us explore points in the curve we would have not normally considered to converge to a global optimum.
Get Ajay Sampat’s stories in your inbox
Join Medium for free to get updates from this writer.
The budget allocator sends each campaign’s allocation to the respective channel bidder for deployment.
Bidders
Bidders publish the final changes needed to serve an ad at the target price point. Bidders are made up of two parts — the tuners and actors. The tuners decide how to deploy the capital based on available levers (e.g keyword, title, value, bid type for Google Search), while also considering channel-specific context. The actors communicate the actual bid to the internal and external channels like Job Boards, Search, Display, Social, and Referrals through API integrations.
Over the years we have built relationships with our partners who help get our product in front of the right audience. Each channel, based on its level of sophistication, supports different bidding strategies. Some popular strategies are listed below.
We’re constantly experimenting to set each campaign’s bid with the right strategy and update cadence in an ever-changing digital media landscape.
Bidders contain a lot of channel-specific nuances that help them make the best possible decision. The bidders also have some level of recency weighting and seasonality baked in to account for market volatility.
Conclusion
The long-term success of marketing automation at Lyft depends on incorporating human feedback into our machine learning platforms. This is generally referred to as “human-in-the-loop” machine learning, and enables machines to work on automation-breadth problems while empowering human operators to focus on knowledge-dependent problems. Without good input from the humans driving the automation engine, the quality of the models will suffer (“garbage in, garbage out”).
Without the cognitive overhead of manually updating bids or allocating budgets, we expect our marketing teams to more nimbly apply audience and creative changes to campaigns. They have more time and energy to:
- Understand our users and their interests
- Ideate new ad formats, messaging & channels
- Form hypotheses for big shots on goals
We have many exciting ideas for the continued iterations to Symphony:
- Always-on experimentation
- Incorporating seasonal effects like weather & time of day
- Better marketplace context to inform our bidders
- Intelligent segmentation & personalization
With Symphony, we are achieving a higher return on our investments while saving marketer hours. The system powers a growing ecosystem of more than 30 million riders and close to 2 million drivers (based on 2018 data). Marketing automation is still in its nascency at Lyft, and while these methodologies have helped us scale so far, we will continue learning and improving as we grow. We are excited for our bright machine learning and experimentation driven future.
Acknowledgments
Many thanks to the team — Alex Armenta, Jared Bauman, William Borges, Anna Campanelli, Dongwei Cao, Carolyn Conway, Ismail Coskuner, Petros Dawit, Jared Gabor, Langfei He, Robert B. Kaspar, Antonio Luna, Patrick McGrath, Usman Muhammad, Jack van Ryswyck, Alejandro Veen, Vidya Vutukuru, Xing Xing, and our cross-functional teammates.
The Growth team is actively looking for talented and driven engineers, data engineers, scientists, product managers, and marketers to join our team. Learn about life at Lyft and visit the careers section for the latest openings.
