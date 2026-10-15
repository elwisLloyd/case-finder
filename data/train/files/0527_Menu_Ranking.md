# Menu Ranking

Источник: https://medium.com/foodpanda-data/menu-ranking-422ad21f381e

Maximising the conversion rates, among other metrics, of users on the Foodpanda platform requires that we have a competitive edge in understanding what an ideal menu looks like. To find the best order in which a user is presented choices, for each particular vendor, we run A/B experiments for a set of countries. What we call menu ranking refers to the sorting order of categories and products, as illustrated below.
In this article, we will explain the initial implementation of scheduled updates of the B versions, the scaling challenges we faced along the way, our optimisation efforts and results.
To run the experiment(s), we needed
- The business logic to decide which is a suitable B version for testing against in the form of BigQuery tables.
- An internal API to declare what the B versions look like (using an ordered data structure such as a list)
- Scheduled task that takes the result of (1), and sends data through (2)
- Ability to track and compare metrics such as click-through rates to determine the success of the B version, relative to its baseline.
We will explain our design of (3), the challenges that arose, the current solution, and some future improvements planned.
First, we use the de-facto Apache Airflow to describe a DAG (Directed Acyclic Graph), which describes a workflow, basically chaining together various tasks (run by Operators).
The high level concept for this task would be:
- Query the tables containing B version data
- Create the payload(s) to send to API
- For each vendor and its corresponding payload(s), call the API
However, even for the initial 5 countries, we were limited to sending synchronous requests for either one set of categories or products, for one vendor per API call. Executing 200,000 calls sequentially took our production server 9 hours. This cost us in two ways:
- Hogging of compute resources (Kubernetes slots) which deprive other DAGs in our data pipeline
- Higher failure rates
While compute resources can be increased, the real problem was a high failure rate. We found that the failures were largely due to vendors actually modifying their menu during the window of time in which we ingest the source data, augmented it with B versions, and sending it to the API. The total time taken by the entire workflow totalled around 13 hours.
Get Tommy Lim’s stories in your inbox
Join Medium for free to get updates from this writer.
The transaction logs which showed the reasons for failure confirmed our suspicion; around 4% of the time, by the time the payload was sent to the API, the menu either no longer existed, or did not have the same set of categories or products that the payload contained. In addition, we were not prepared to scale up to run the A/B experiment with more countries. For the most effective experiment, we should have the capability to update the B versions fast enough to fit into a daily schedule. If it took 9 hours for 5 countries, that means that once we exceeded approximately 14 countries, the DAG would spill over to the next cycle and start a snowball effect. We would then have to reduce the frequency of sending the data, and deal with an even higher failure rate.
Thus began our optimisation efforts. We restructured the DAG to increase concurrency by doing the following:
- Paginating the B version data using OFFSET and LIMIT in BigQuery
- Generate multiple concurrent DAG tasks for each page
- Breaking down the B version data into countries, prioritising by country
- Using a dedicated DAG pool
- Allocate more CPUs to deal with more concurrent tasks
And the DAG evolved to look like this:
Each element of optimisation was integral to the overall- without (4) and (5), the DAG would still struggle to run fast, because having a small number of CPUs context switching between tasks was not going to work. (1) and (2) worked together because each task would only have to send data based on its own page. (3) is less obvious, but it also contributed to reducing the error rate. Assuming equal chances of a vendor changing their menu for each country over time, prioritising the country with the most vendors meant that a greater proportion of vendors were less “at risk” of changing their menus before we could declare the B version.
The final result of our optimisation? Over 2x faster run times (3 hrs 45 mins) and a failure rate of 2.2% or lower. Generally, this should be low enough to preserve the quality of our A/B experiments.
As we scale up to include more experiments across more countries, some potential future improvements include:
- Dynamic configuration of pagination, to reduce the need for updating the page size and max pages when there are huge shifts in markets
- Batch sending of payloads (based on internal API upgrades)
- Decouple the B version formulae for different countries, separate DAGs to allow toggling of the A/B experiment individually
- Ability to swap B versions with A versions in response to positive experiment results
