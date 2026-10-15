# Real-time Fraud Detection with Yoda and ClickHouse

Источник: https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4

Authors: Nick Shieh, Shen Zhu, Xiaobing Xia
Background
Instacart is the leading online grocery company in North America with millions of active customers and shoppers. Combating fraud and abuse on our platform is essential not only for maintaining a trustworthy and safe environment but also for preserving Instacart’s financial health. In this article, we introduce our Fraud Platform, Yoda, explain why we chose ClickHouse as our real-time datastore, and provide insights on how this system helps us combat various types of fraudulent activities.
Fraudulent patterns are varied and broad by nature, ranging from fake accounts to payment fraud and collusion between customers and shoppers. Our Fraud Platform team developed Yoda, a decision platform service, to detect such fraudulent activities quickly and take appropriate measures. With Yoda, we implement rules that distinguish legitimate activities from fraudulent ones, and define the actions that we should take as a result. Actions can range from flagging the activity for review, blocking the transaction, or even disabling accounts.
Key Characteristics of a Fraud Platform
Overall the platform needs to be:
- Self-serve and Flexible: Fraud can take many forms, and the system should be self-serve and flexible enough for fraud analysts and operations teams to create rules that can respond to a wide range of fraud patterns.
- Low Latency: The system needs to evaluate data and make decisions quickly.
- Real-time: The system should have access to real-time data so it’s viable for making real-time decisions based on the freshest data.
To enable fraud decisions in fractions of a second, Yoda uses ClickHouse as its primary real-time datastore. ClickHouse is a fast and highly performant analytical database, widely used across Instacart to power other use-cases such as critical retailer and ads dashboards, calculating results for A/B testing, and machine learning signals.
Yoda Overview
At a high level, a typical lifecycle for a Yoda real-time rule is:
- Analysts create, read, update, and delete rules through a UI.
- A request comes in for decisioning into the real-time system.
- Feature system fetches and aggregates features based on the request information and the relevant rules configurations. Features can come from machine learning inference services, Instacart’s in-house Feature Store, and ClickHouse.
- Evaluation service evaluates the rules, comparing retrieved features against the rule logic for decisioning and actioning. Examples of actions include shopper warnings, suspensions, and issuing selfie identification checks.
- Action dispatch consolidates evaluated actions and calls appropriate action services.
Why ClickHouse?
Here, Yoda’s feature system integration with ClickHouse as a real-time datastore (3) is especially important in enabling fast fraud detection for the following reasons:
- ClickHouse is a columnar database, which means it stores data of each column independently. When performing aggregations on specified columns, it will only fetch data from those columns instead of the entire row, which makes these operations more efficient.
- ClickHouse supports LSM-tree based MergeTree family engines. These are optimized for writing which is suitable for ingesting large amounts of data in real-time.
- ClickHouse is designed and optimized explicitly for analytical queries. This fits perfectly with the needs of applications where data is continuously analyzed for patterns that might indicate fraud.
Data Ingestion Pipeline
The first step to being able to access features in ClickHouse is ingesting their data sources. Real-time data primarily comes from 2 sources: PostgreSQL and Instacart event data.
At Instacart, Postgres is used as the primary relational database, storing business critical information such as order deliveries, card transactions, and customer and shopper information. Therefore, we leveraged Change Data Capture (CDC) technology to read these records from PostgreSQL. Debezium’s Postgres connector is used to publish logical replication records to Kafka; this connector runs within the Kafka Connect framework.
Get Nick Shieh’s stories in your inbox
Join Medium for free to get updates from this writer.
For event data, Instacart built an in-house event ingester that processes events. Users can send events with JSON Schema from backend services (Ruby, Go, Python), Android, or iOS clients. The ingester collects those events, performs schema validation, and publishes them to Kafka.
Self-serve, Config-driven Flink Ingestion Job
In order to allow users to ingest data into ClickHouse easily, the team developed a config-driven ingestion job with Flink. It takes YAML configuration from users, reads data from Kafka topics, processes the data, and writes to ClickHouse, here’s an example config file:
cdcSource:
- name: OrderDeliveryBatches
topic: dispatch.order_delivery_batches
sourceGroupId: order_delivery_batches
parallelism: 1
fieldsList:
- fieldName: order_delivery_id
destinationFieldName: order_delivery_id
fieldType: Long
- fieldName: batch_id
destinationFieldName: batch_id
fieldType: Long
- fieldName: created_at
destinationFieldName: created_at
fieldType: DateTime64(6)
- fieldName: shopper_started_at
destinationFieldName: shopper_started_at
fieldType: DateTime64(6)
- fieldName: shopper_completed_at
destinationFieldName: shopper_completed_at
fieldType: DateTime64(6)
clickhouseDestinations:
- name: order_delivery_batches
source: OrderDeliveryBatches
config:
parallelism: 1
flushIntervalSeconds: 10
maxBufferSize: 104857600
destinationList:
- hostname: yoda.fraud.clickhouse.prod
port: 8123
database: FRAUD
table: order_delivery_batches
With this YAML config, the Flink job will consume data from topic dispatch.order_delivery_batches, perform some mappings and extractions, and insert data into FRAUD.order_delivery_batches table by sending requests to yoda.fraud.clickhouse.prod, the target ClickHouse cluster. The Flink jobs are deployed in our Flink deployment platform and as of today, we have ~30 ingestion pipelines running.
Real-time Feature Engineering Workflow
With data ingested into ClickHouse tables, real-time features can be served at runtime dynamically through SQL queries. Users of Yoda write YAML-based feature definitions which define dynamic SQL that queries the tables. These feature definitions are consumed in rulesets for evaluation and decisioning in the service. Following are the steps to onboard a new rule:
Step 1: ClickHouse Table Ingestion
Define the ClickHouse table schema for the respective Postgres or Instacart event data. Create the configuration for the Flink job to ingest data into tables as described in the previous section. This is a one-time step — the tables are now ready to be queried.
Step 2: Define Feature Definition
Analysts can define their own real-time features in a YAML configuration as show below for illustrative purposes:
Name: order_checkout_transactions_features
Description:
"[Illustrative Purposes] This feature definition returns features for the qualifying order if
- pos_amt > instore_checkout_amt
Then, the Yoda rule logic will be:
Suspend shopper if swipe amount >= X * in-store checkout amount."
Version: 1
Database: FRAUD
# Query-defined real-time features
Features:
- Name: shopper_id
Type: BIGINT
- Name: order_delivery_id
Type: BIGINT
- Name: pos_amt_usd
Type: FLOAT
- Name: instore_checkout_amt_usd
Type: FLOAT
QueryParams:
- order_delivery_id # %{order_delivery_id}
Query: |
WITH 
transactions_summary AS (
SELECT
order_delivery_id,
driver_id,
MAX(user_transaction_time) AS last_user_transaction_time,
SUM(amount_cents * (CASE WHEN type IN ('type_1', 'type_2') THEN -1 ELSE 1 END)) / 100 AS pos_amt_usd
FROM 
FRAUD.transactions
WHERE 
state IN ('STATE_1', 'STATE_2')
AND type IN ('type_1', 'type_2', 'type_3', 'type_4')
AND created_at >= NOW() - INTERVAL 24 hour
AND order_delivery_id = %{order_delivery_id}
GROUP BY 
1,2
),
checkouts_summary AS (
SELECT
order_delivery_id,
JSONExtractFloat(...) AS checkout_usd,
MAX(created_at) AS last_instore_checkout_ts
FROM 
FRAUD.checkouts
WHERE 
created_at >= NOW() - INTERVAL 24 hour
AND order_delivery_id = %{order_delivery_id}
GROUP BY 
1,2
)
SELECT
ts.order_delivery_id AS order_delivery_id,
ts.driver_id AS shopper_id,
ts.pos_amt_usd AS pos_amt_usd,
cs.checkout_usd AS instore_checkout_amt_usd
FROM 
checkouts_summary cs
INNER JOIN 
transactions_summary ts
ON cs.order_delivery_id = ts.order_delivery_id
WHERE 
...
AND ts.pos_amt_usd > cs.checkout_usd
The real-time features are explicitly defined for the definition, and the dynamic query extracts, transforms, and aggregates the appropriate features from multiple tables. Most queries fall under an analytical pattern of fetching information for a certain entity, shopper ID, customer ID, or order delivery ID, over a short look-back period.
Step 3: Consume the Feature Definition in Yoda Rules
Users create or update rules in the UI to reference these feature definitions for real time evaluation and decision making. These feature definitions are reusable across rules.
Outcomes and Lessons Learned
Having a self-serve, real-time platform has been a huge step forward for our ability to fight fraud. We’ve observed the following benefits:
- Improved fraud detection: Decreasing the time to develop features also lessens the time to address and respond to fraudulent activities. Catching fraudulent behavior in real time has already resulted in millions of dollars a year in savings.
- Flexible development workflow: Enabling self-service end-to-end development enhances usability, from feature engineering to rule creation to decision-making and taking action.
- Improved engineering productivity: By shifting from engineering-led to ops and analyst-led workflows, the time engineers spend on heuristic development has decreased from 80% to 20%.
ClickHouse Insights
We also learned some important lessons along the way in how to best use ClickHouse:
- Insert data in batches: ClickHouse is most performant when the ingestion pipeline inserts data in batches.
- Sorting key matters: Most real-time analytical queries follow a query pattern of selecting data for a certain identifier, such as shopper_id or batch_id, over a short look-back period of time. Specifying a sort key (e.g. <identifier>, created_at_ts) for ClickHouse table schemas significantly reduces the amount of data scanned and improves query performance.
- Security: Sensitive data such as order details, shopper, and user activities are streamed into ClickHouse. Therefore, two-step access controls are enforced so that data cannot be accessed by unauthorized clients. Clients from unauthorized groups first need access to the ClickHouse cluster hostname, and then clients need dedicated ClickHouse accounts upon connection.
- Data lag consequences: Data lag is the time delay between event occurrence and when it’s ingested into the system, which is unavoidable in an asynchronous streaming environment. Certain tradeoffs need to be accounted for, such as balancing system performance with rule accuracy and real-time data freshness by configuring ClickHouse batch writing intervals, table TTLs, and configuring the processing time delay of Yoda’s decision request per use-case.
Future plans
Going forward, we continue to invest in Yoda and ClickHouse at Instacart, expanding its scope for adoptability. The team aims to onboard and integrate more generalized business use-cases besides fraud onto Yoda and its feature system. In addition, feature engineering will be streamlined with further UI support and tooling.
On the ClickHouse side, the team is simplifying the process of setting up ingestion pipelines by investigating tools like Flink SQL, while further maturing the ClickHouse deployment infrastructure on Kubernetes to improve its scalability, availability and maintainability.
Acknowledgements
We would like to thank the following stakeholders and partners of this initiative: Xiaobing Xia, Praveen Burgu, Sylvia Lin, Wasi Ahmed, Ana Lemus, Nate Kupp, Like Liu, Regina Lin, Ryan Routh.
