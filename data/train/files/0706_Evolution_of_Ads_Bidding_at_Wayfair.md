# Evolution of Ads Bidding at Wayfair

Источник: https://www.aboutwayfair.com/careers/tech-blog/evolution-of-ads-bidding-at-wayfair

Introduction
Wayfair, like most other e-commerce companies, leverages advertising to place relevant content in front of existing and prospective customers. Content is hosted and distributed over various advertising channels, such as search engine results, websites, videos and social media. Several of these advertising channels operate in auction mode - meaning each advertiser determines the amount of money they are willing to spend for an ad click, and the ad platform will use that as a key input in determining ad placement. This article discusses how the Ads Bidding Platform at Wayfair evolved, the key capabilities it provides, the platform’s architecture and building blocks, and plans for the future.
Overview
Let's look at a simplified example - a potential customer searching for “blue sofas” using the Google search engine. Wayfair may be willing to pay $1.00 for each click on their sofa ad by a potential customer, while another e-commerce site may be willing to pay $1.09, and a third only $0.90. Google uses these “bids,” in addition to other factors such as the quality of the landing page, to determine where on the search results page Wayfair’s ad will be displayed. Hence, determining the right amount for the bid is critical. If we pay too little, our ads may receive undesirable placement or may not even show up at all; but if we pay too much, we may not recover the cost of the ad spend.
Hence, to do this at scale and determine the appropriate amount to pay for each of the millions of keywords and items in our Catalog, we (Bidding & Optimization team at Wayfair) have built an automated, data-driven platform. The goal of this platform, simply put, is,“To determine Wayfair's willingness to pay for any marketing opportunity, taking into account specific business goals."
Early Days
During the early days of ads bidding at Wayfair, there was no central platform to handle bidding. This meant that each time someone wanted to develop a heuristics-based or Machine Learning (ML)-based new approach to bidding, they needed to reimplement several aspects of the end-to-end pipeline in an ad hoc manner (see Figure 1). Note that the purpose of these models is to allow us to analyze the metadata and historical performance of ads, use that data to predict future performance, and ultimately to determine how much we want to pay per click.
There were several challenges with this early approach, such as duplication of similar types of work, slow time to market, and a lack of observability and coordination across these approaches. It was clear that we needed a new central platform to help us scale.
New Platform
To address these challenges and deficiencies, the Wayfair Bidding and Optimization Platform team designed a new central platform for ads bidding. The key considerations, assumptions, and requirements for the new platform were as follows:
- Extensibility
  - We may not have a single best approach that will always work for all bidding units (e.g., stock-keeping units (SKUs) - which refer to each unique item in our catalog (which contains millions of items), keywords, URLs, and any other entity we want to produce a bid for). So, the platform should be able to support different approaches for different groups of SKUs or keywords.
  - The platform must make it easy to plug in new approaches.
- Observability
  - The platform should provide visibility into why decisions were made in a certain manner. This is crucial for marketing analysts and data scientists to gain insights into how our algorithms are working in the real world.
- Configurability
  - The platform should provide fine-grained control over parameters such as return on investment (ROI) and bid aggressiveness. For example, it may be acceptable to have a very low ROI on certain categories of items, but not on others.
- Experimentation
  - The platform should allow for easy trial-and-error experimentation, to quickly weed out any poorly-performing approaches.
- Scalability
  - The platform should make high quality data available, to allow rules-based and ML-based approaches to be developed by Data Science and/or Marketing groups.
  - In addition, it should allow algorithm builders to focus on the development of core logic, as opposed to the various aspects of running a scalable, robust production system.
As shown in Figure 2 below, the first major change was to ensure that the core capabilities are provided natively by the platform. This means that the only incremental work required to get new approaches launched is work specific to each new model.
The second major change was to clearly define the contract between the core platform and the specific bidding approaches. In order to satisfy all the requirements listed above for the new platform, we designed a new architecture, as described below.
New Platform Architecture
The architecture for the new Ads Bidding Platform consists of the following major components, shown below in Figure 3. These components provide the core capabilities for the platform.
The major components in the Ads Bidding Platform are described below.
Data Engineering (internal name: FORGE)
Both ML-based and rules-based approaches require a variety of signals, including both first-party signals (those collected from Wayfair’s internal data) and third-party signals (those collected by an outside source). The data engineering component of the system ensures that data from a variety of sources is processed and normalized into a usable form, for consumption by various systems, as well as Data Science and Marketing groups. These transformations range from aggregations and identity mappings, to more complex operations such as detecting anomalous data and excluding/imputing for them.
Older versions of data engineering involved large, complex SQL scripts that were difficult to reuse, test and maintain. We built a new platform called FORGE that performs data engineering in a modular, configuration-driven manner. Conceptually, it involves building reusable transformations that are connected together in a sequential pipeline. These transformations include logical and mathematical operations, as well as domain-specific transformations.
Bidding Console
The Bidding Console provides analysts with fine-grained control over objectives using various “levers,” letting them set both high-level and more precise objectives. These levers range from high-level ROI targets, to granular control over the rate of bid adjustments (which can be set at a class level, or even on an arbitrary group of SKUs). The system also allows for customizable levers for specific use cases.
Bidding Approaches - Single Bid Calculators (SBCs)
In order to support a variety of bidding approaches, and to provide maximum flexibility, we use the concept of a “Single Bid Calculator” as the core building block of our Wayfair bidding approach. Single Bid Calculators provide the core logic that determines the actual bids/adjustments.
Simply put, a Single Bid Calculator takes in a single bidding unit (e.g., SKU) as input. The SBC then produces a bid or bid adjustment by leveraging all relevant data/signals that are available for that bidding unit from the data engineering pipeline (or other services). The actual logic for the adjustment could be ML-driven or rules-based or a combination of both.
Some of the major benefits of using the SBC approach are:
- Allows easier isolation of the logic for each new bidding approach
- Supports the addition of new approaches in a simple structured manner
- Provides the flexibility to support approaches that have very different data needs, without mandating a specific data pipeline. For example, we may need to support algorithms that use dynamic lookback windows (to determine how many days of data we need to look at to ensure a minimum number of clicks, which varies for each SKU), or for simpler approaches where the data needs can be fully precalculated.
- Offers flexibility with respect to deployment. We can take the SBCs and run them out of process as a service, or use them as a library running in process to maximize performance.
- Speeds up development and makes it easier to test SBC-specific logic
Arbitration
As explained earlier, one SBC produces a single bid for a given bidding unit. At Wayfair, we often want to generate multiple bids for a given bidding unit, using different approaches. Doing so gives us the flexibility to:
- Use some combination of these bids as the final bid.
- Employ a simple fallback mechanism (where we may not know ahead of time which algorithm will be able to produce a bid for a given bidding unit).
- Evaluate multiple versions and approaches at the same time.
- Allow for exploration of “counterfactuals” (e.g., “Would model X have generated better bids for a specific scenario?”).
So how do we produce multiple bids for a given bidding unit? We simply use multiple SBCs, each using a separate approach. For example, we may write SBC-A to produce a bid using a rules-based approach, and SBC-B to produce a bid using an ML-based approach.
We now have two bids for this bidding unit. So how do we determine which bid to select? Arbitration is the step that determines a single best bid from the many bids produced for a single bidding unit, using one or more mechanisms such as optimal bid selection or A/B tests. We could use a simple fallback approach (i.e., if SBC-B is able to generate a bid, use that; otherwise, use SBC-A’s bid), or a combination (average of the two bids), or some other variation. Figure 5 below illustrates Bid Arbitration.
To understand how these SBC constructs make it easy to incorporate new bidding approaches, let’s review an example. Assume we find a new approach that works well for a certain set of bidding units that have specific site visit and purchase characteristics (e.g., high traffic). We would write a new SBC (SBC-New) that would produce a bid using this new approach, but only when those specific characteristics are present in the bidding unit. We would also create an arbitration rule that would first use the bid from SBC-New if it exists; otherwise, it would fall back to the standard SBC using the previous business logic.
Observability
In addition to allowing us to understand why each approach/model made decisions in a certain way over time, the platform also provides overall channel and model-level observability as another key benefit. For example, when any new model is added to the system, visibility around performance characteristics of the model (e.g., projected spend (see Figure 6), or the average bid amount by each model (see Figure 7), or the number of units that we are using the new model for) is available out of the box.
Vendor Mapping
Finally, the final bids that are produced are translated into vendor-specific terms and identifiers before they are sent to different advertising platforms such as Google Ads, Bing Ads, etcetera. All the ad features are expressed in generic (but Wayfair-specific) terms to ensure that we don’t lose performance history if the campaign structure changes, or ad units are moved from one campaign to another. We produce bids for bidding units expressed in generic terms (e.g., Wayfair identifier as opposed to vendor identifier). Hence, we need this final vendor-mapping step to translate our bid into terms that the vendor can understand.
Key Technologies
Wayfair’s Ads Bidding Platform leverages the following key technologies to maximize our platform performance and throughput, as well as engineering productivity.
Google Cloud Dataproc - Using the Single Bid Calculator approach with our platform architecture lets us convert the problem into one that is fully parallelizable. This allows us to use Google Cloud Dataproc as the main execution engine, taking advantage of its automated, fully managed and highly available workflow services.
Aerospike - Using Aerospike as the data store for the data/features used by bidding approaches allows us to fetch this data with extremely low latency. This enables us to maximize the throughput of bid calculations.
Python - After much deliberation, we settled on the use of Python for two main reasons. First, it offers the option of executing ML model predictions in process, to maximize performance. Secondly, for our data engineering pipeline (FORGE), Python allows us to express transformations more succinctly, without significantly impacting performance.
Google Cloud BigQuery - The scalability, performance, rich set of integrations, and ease-of-use by non-engineers made BigQuery an easy choice for our data storage and analytics needs.
Java/K8s web services - Several supporting services for our platform are built using Java-based web services running on Kubernetes (K8s), following a typical pattern for these types of services.
What’s Next
We have big plans for how to evolve the Wayfair Ads Bidding Platform over the next few years, and here is a sample of the types of changes we are considering.
- Transition to a more automated channel performance management
- Incorporate the addition of simulation and impact analysis capabilities
- Use approaches such as the “M ulti-armed bandit” to rapidly tune and improve algorithm performance
Conclusion
In this blog post, we walked through the journey of the evolution of Wayfair’s Ads Bidding Platform. However, we are nowhere close to being done! We have ambitious plans to make this platform much more intelligent, expand its scope to include additional marketing channels, as well as use this conceptual framework to produce other scores/targets. Last but not least, we place a lot of emphasis on collaboration at Wayfair, and none of this would have been possible without the strong partnerships we built with the Data Science and Marketing teams.
Come Join Us!
If you find our work interesting, please connect with us! We are always looking for talented engineers and managers to help build the next generation of scalable, well-architected platforms at Wayfair! Head over to our Careers page to see our open roles. Be sure to follow us on Twitter, Instagram, Facebook and LinkedIn to catch a glimpse of life at Wayfair and see what it’s like to be part of our growing team.
