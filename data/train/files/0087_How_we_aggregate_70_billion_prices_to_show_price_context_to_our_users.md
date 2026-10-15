# How we aggregate 70 billion prices to show price context to our users

Источник: https://tech.trivago.com/post/2025-02-13-how-we-aggregate-70-billion-prices-to-show-price-context-to-our-users

Price comparison is one of the key value propositions of trivago, and in doing so, we handle billions of prices everyday to provide our users with the most accurate and up to date price as possible. We can leverage this enormous amount of historic price data to provide price context for our users in a scalable and fast way.
Why do we need aggregated price data?
As we handle billions of prices everyday, aggregating them in real time to provide, for example, the average price for Berlin for next month, would add an extra load into our application and it would not be beneficial for the user experience.
However, given that we store all the prices we request from our advertisers, we can use this historic data to build aggregated price metrics for a travel destination or an accommodation. This solution is particularly more efficient and scalable as the aggregated price data can be streamed to our applications and served to our users even faster than a regular hotel or city search at trivago.
In 2023, providing price context to our users became one of our key objectives in terms of product development. This meant a strong demand for aggregated price datasets that we could quickly leverage to test price context features. Before diving into the creation of something entirely new, we chose to tap into existing datasets. This strategy allowed for quick testing and helped us gain valuable insights.
However, this proved to be challenging, as our price data was scattered around different datasets with complex dependencies and debatable aggregation approaches. Over the years, we had built numerous aggregated tables on top of other aggregated tables as quick, temporary solutions that ended up becoming permanent. A typical example of technical debt growing with time.
Our Solution: Price Stream
With the previous context in mind, we set our goal of building a data product that could fulfil the growing demand of aggregated price data, while taking a few design constraints into consideration:
The delivered data must be an accurate representation of the prices we show in our product
As we aimed to provide aggregated price trends, we needed to be sure these were an actual representation of the price trends on destination or accommodation level.
We had a lot of historic data available to build these aggregations as we ingested all the prices advertisers sent us into our data through a kafka stream. However, this data was raw and unfiltered, meaning that it contained many prices that will not be exposed to our users, so we decided that an outlier rejection condition was necessary to ensure our price aggregated metrics were reasonable.
Flexible and scalable to cover the most common use cases
We were looking for a solution that would give our product teams the flexibility they need in regards to filtering capabilities and aggregated metrics they might require. After carefully studying the challenge we were facing, we knew that this required an aggregated price data set on accommodation and city level, but also on arrival month and locale level (the trivago platform from which the user executes a search).
We knew from previous feature tests that this was not enough and that we needed to aggregate the data using various other fields. This can be achieved in BigQuery and many other SQL interpreters by using Grouping Sets. This is useful for generating aggregated results for different combinations of columns without writing multiple GROUP BY queries.
We selected columns or attributes which we knew might be useful for our product teams, based on previous tests and domain knowledge from our product teams:
- If the price for an accommodation has breakfast or cancellation included
- The star rating and review rating for a given accommodation
- The weekday of the arrival date for the requested price
We also generated metrics such as percentiles, average prices, minimum or maximum prices, etc. since we knew from previous tests that these were often the most used metrics for product features.
With this, one could answer questions such as “What is the average price for a one night double room stay in Amsterdam for January 2024, with breakfast included?”
The resulting dataset was very big. One day of accommodation data generated in early September 2024 had a row count of 521,857,384 records.
Must be integrated with our web application in a fast and practical way
Finally, the missing piece was, how do we make this large dataset available to our frontend engineers so that they can show the price aggregates through insightful features in our product?
As we do with other similar use cases, the answer was through a Kafka stream. Kafka streams are very useful for streaming data as a key-value pair format in a scalable and fault tolerant way.
With this and thanks to our GraphQL gateway services, we could make this data available to our application, similar to how we also deliver many other datasets to make trivago work as expected.
Challenges
As expected, projects that deal with not only large datasets, but also with various stakeholders usually create interesting challenges. Here are some of the main ones we faced during its implementation and even while the pipeline was already in production.
A big data problem
To have a rough idea of how much data we are talking about, one of the base tables we were trying to populate for this project had around 14 billion rows on a daily level. We wanted to use at least 7 days of historic data (hence the 70 billion prices mentioned in the title), to capture the weekly seasonality of prices. But this was an enormous amount of data to handle and we realised this project was not feasible to do under our on-premise cluster resources as we had initially designed.
Fortunately for us, in 2023 the company was migrating from our on-premise Hadoop cluster to a cloud computing environment in Google Cloud Platform (GCP), and even though we had to migrate the codebase to the new framework, this gave us a significant increase in computational power which enabled us to continue iterating on the project.
Even in GCP, due to memory constraints, we had to compromise a few of our initial requirements to make the pipeline work and reduce the historic data used from 7 to 1 days. This meant we reduced the coverage of the data in terms of arrival months in the future, specially for countries where we don’t have that much traffic, which takes us to the next challenge.
Solving coverage issues
As mentioned, for particularly smaller locales or platforms, we noticed that the coverage of destinations and accommodations with prices could be better, causing the price context to be missing in some scenarios. This was partially caused by our inability to calculate price aggregates from destinations or accommodations without sufficient search volume. If a destination is not particularly popular in a certain country, it will always be hard to get enough price data to build our metrics.
We also realised that there were a lot of duplicated prices in the data source (around 88% of duplicated records) and by removing these duplicates, we could start using 7 days of historic price data instead of 1 and significantly increase the coverage in almost all locales.
Switching to a deduplicated approach revealed another issue: without adjusting the outlier rejection step, we experienced a significant increase in rejected prices at the accommodation level. Fortunately, this was rather easy and quick to fix.
Outlier rejection issues
During the data validation stages, we noticed that our outlier rejection approach was not working as expected as we saw extreme prices while doing spot checks.
To reject outlier prices we initially decided to implement one of the most popular approaches: reject all prices outside 3 standard deviations from the mean. This practical rule usually works pretty well for datasets with a normal distribution. The problem was that our data was not normally distributed:
Since the previous distribution resembles an exponential distribution, where the majority of the prices are concentrated in the lower end of the data, here a logarithmic transformation can ideally transform this distribution into a normal distribution. After applying this transformation we plotted again our prices and obtained better results:
After deploying a fix, thanks to all the investigations we did, we decided to add additional percentile metrics to better capture the lower and upper tails of our data and we also started recommending our stakeholders to ideally use percentiles instead of minimum, average, or maximum for price trends.
Current features using Price Streams
Price advice calendar on the homepage of trivago
This feature shows a price context using percentile 5th and 95th for the price range, for the top destinations for the particular country (Germany in this case).
Dateless search
Users doing a search on trivago without providing dates will see a list that doesn’t fetch live prices but relies instead on our Price Streams to show the minimum price of each accommodation.
Learnings
Start simple and doing smaller iterations pays off faster than trying to go all in from the start.
One key takeaway from this project is that reducing the requirements and trying to deliver the most simple yet functional solution as possible will save a lot of time and effort. Looking back now, we initially tried to deliver the most complete and solution which took us a good amount of time to develop, debug and optimise. Considering that as of now we haven’t used even half of the features and aggregation capabilities of our solution, we could have simplified a lot our requirements and deliver the bare minimum that was needed to kick start the project and unblock the product teams, while continuing iterating and adding more features as needed.
Investing time in exploratory analysis is worth it.
This sounds obvious, but this is something that we often skip in due to the fast paced environment we face. While you probably should simplify your solution as much as possible, skipping the basic exploratory analysis phase is something you should never do. In our case, we learned the hard way that the distribution of our price data was not what we assumed and this caused more rework and time invested in solving outlier issues, than the time you would had spent doing a basic histogram chart and realising the data is not normally distributed.
Be careful with assumptions
We often need to make many assumptions during analyses, projects and so on, but different assumptions come with different risks. One should think beforehand very carefully, what kind of risks are we facing by assuming certain things. In our case, different wrong assumptions led to issues that we had to tackle and meant additional effort. For example, assuming that after a change an increase in coverage on destination level would also mean the same on accommodation level.
Document as much as possible
Something that I personally learned while working on this project, is that documenting every problem I faced, every decision I took and every approach I evaluated helped me a lot later on. Either to prepare a presentation for our yearly Tech Get Together conference, to write this tech blog, or to explain to stakeholders why we took the design decisions we took, documenting has allowed me to learn and also share my knowledge with others. In a more general sense, documenting this project has also been the documentation of a very interesting and enlightening journey.
Next steps
The work does not end here for us as this project has turned into a data product that we now maintain and improve constantly. Some of the ideas we have in our pipeline to further improve and deliver more useful datasets to our stakeholders are:
- New price stream datasets: for example, until now our lowest aggregation level is on arrival month, but many product features will eventually require aggregated price data on specific arrival dates, to provide our users with more detailed price context.
- Further optimising the outlier rejection conditions, specially for accommodations, with the focus on relaxing the constraints and hopefully increasing the coverage.
- Implementing data quality checks and alerts to early detect data incidents and be able to react quickly to issues.
