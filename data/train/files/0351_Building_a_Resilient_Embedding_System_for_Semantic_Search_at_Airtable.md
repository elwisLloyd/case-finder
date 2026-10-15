# Building a Resilient Embedding System for Semantic Search at Airtable

Источник: https://medium.com/airtable-eng/building-a-resilient-embedding-system-for-semantic-search-at-airtable-d5fdf27807e2

Building a Resilient Embedding System for Semantic Search at Airtable
When ChatGPT burst into the public eye in 2022, a small team of engineers at Airtable started ideating on the different ways our platform could leverage this new set of capabilities. One idea kept popping up: rich, semantic search over customer data.
Imagine a marketing team asking, “Can you find past campaigns similar to this one?”, a product management team asking “can you find engineers whose expertise matches this project?”, or in my case “can you find past issues (called “escalations” internally) similar to this one?”. Embedding powered systems can allow teams to quickly identify insights that would normally take hours of manual labor.
Thinking About Building An Embedding Powered System:
Embeddings are at the heart of semantic search. Embeddings are vectors, an array of numbers, numerical representations of data, that capture meaning in a way that machines can understand. Concretely, an embedding can tell you that “cat” is similar to “tabby”, but not similar to “car”.
Building a system around embeddings isn’t trivial. There are multiple dimensions to consider:
- (Focus of this post) Embedding Lifecycle Management
- Triggering — As data changes embeddings need to be (re)generated. We need to durably track the state of generation.
- Generation — Generating the embeddings via API calls (over the network, or in-process)
- Persistence — Where and how are the embedding stored
- Deletion — Deleting old data when it’s no longer needed
- Consistency — How do we maintain consistency between our vector data and primary database?
- Migrations — This has several flavors e.g. Changes to the DB schema, changes to the DB engine (e.g. LanceDB vs Opensearch), Changes to the AI embedding model, or changes to the underlying storage layer’s encryption
- Disaster Recovery — What happens if we experience data loss?-
- Data Preparation
- Corpus Choice — What data will we embed?
- Configuration — Embedding model choice, chunking strategy, other knobs
- Query And Access
- Querying — Via semantic search or direct access
- Indexing — Data structures for efficient semantic similarity queries
- Permissions — Making semantic search respect our permissions model
- Operational Concerns
- Security — Embeddings are sensitive customer data and must be treated accordingly
- Cost — How do we keep the cost of generation, persistence, and querying manageable?
- Partition Management — If you have many collections, how do you handle scaling the number of partitions?
Given all that, we needed a system that was not just functional but robust and adaptable.
A High-Level Overview of Airtable’s Architecture
Airtable offers an app building platform built on top of a custom, in-memory database backed by MySql.
Let’s introduce two useful terms we’ll be using
- MemApp — Our in memory database, manages all reads and writes for a base.
- The data is ultimately persisted in MySql
- Base — A particular instance of MemApp
A critical detail: MemApp is a single-writer database. All writes occur serially, which becomes important when we talk about maintaining consistency.
Building A Data Model
Fully Or Eventually Consistent?
Our first fundamental design question was this: Should embeddings be stored within MemApp to ensure full consistency with the data? While appealing in theory, this approach had two major drawbacks:
1. Cost: Memory usage is a significant factor in Airtable’s expenses. Storing embeddings in MemApp would be prohibitively expensive because embeddings are often 10x the size of the underlying data.
2. Performance: Achieving strong consistency would require generating embeddings within transactions. This process would be too slow for bulk updates and would limit us to less capable, in-house models rather than leveraging top-tier providers like OpenAI.
The solution? Embrace eventual consistency, and store and process embeddings outside of MemApp. This decision led us to design a data flow where embeddings are generated asynchronously and stored in a separate vector database — with their state tracked within MemApp.
Data Modeling
We anticipated that AI models, embedding providers, and storage engines would evolve. To future-proof our system, we introduced an abstraction within MemApp called an embedding config. This allows developers to map data from MemApp to a table in a vector database, without worrying about the underlying complexities.
An embedding config has the following primary components:
- data subscription — A declarative description of the data a user has told us they want to embed.
- embedding strategy — How the data is to be embedded
- storage configuration — Where the data will be stored.
- triggering configuration — Once data is out of date, when do we re-generate it?
We’ll be using the terms data subscription and embedding config repeatedly in this post.
Because the system is eventually consistent, we knew we needed to track the state of embedding for every piece of data that a data subscription needs to embed, which leads us to…
Tracking Consistency:
Given that we would be eventually consistent, the latest version of data persisted to our vector database will always lag behind the data in MemApp. We need to be able to determine which data has been embedded and what may be out of date (for filtering stale results or fixing up the vector database). To accomplish this it helps have an ordering of data versions. Ordered data versions also lets us handle out-of-order write operations.
Since MemApp is a serializable database, its transaction number is perfect for this — a BigInt that increments with each write. For each piece of data we embed we create an embedding state:
type EmbeddingState = {
// last recorded transaction that caused a write to the vector database
// this may be lower than the actual number in between when a write to
// the vector database occurs and when the update to MemApp occurs
// (those writes to MemApp may also be lost due to system failures)
lastPersistedTransaction: number | null,
// always correct and up to date, we update this transactionally when
// data in the data subscription is updated
lastUpdatedTransaction: number
}
Being more concrete, we expect updates over the lifetime of an embedding state to look like this:
// new data to be embedded enters the data subscription
{
lastPersistedTransaction: null,
lastUpdatedTransaction: 2,
}
// once the data is embedded, we mark it as up to date
{
lastPersistedTransaction: 2,
lastUpdatedTransaction: 2,
}
// data is edited, we mark it as stale so it can be re-embedded
{
lastPersistedTransaction: 2,
lastUpdatedTransaction: 5,
}
The Simple Life Of An Embedding
Here’s a rough sketch of our system when data changes and needs to be re-embedded
Let’s walk through the flow in practice
Initialization
Upon creating a new embedding config, MemApp automatically provisions a new vector database table and generates embedding states for each relevant data chunk.
Get Will Powelson’s stories in your inbox
Join Medium for free to get updates from this writer.
Detection
When data changes, we update the embedding state’s lastUpdatedTransaction to reflect the current transaction.
Triggering
Tasks are created to generate the embeddings for each config that saw data in its data subscription updated. Currently we do this within the transaction that the detection occurs.
Generation
Our embedding service processes the task(s), and generates the embeddings. We have ample retry logic in case this fails, there’s also a separate blog post here on how to prevent poorly behaving bases from consuming our global rate limits from AI providers or otherwise tanking quality of service.
Persistence
Once embeddings are generated we store them in our vector database. We prevent out-of-order writes by making the insertion conditional on the transaction number for the write being greater than the transaction number stored in the vector DB.
If the update has been outpaced we silently exit the flow since no more work is necessary.
We then confirm with MemApp that the write has happened, updating the lastPersistedTransaction. Once again we handle potential out of order writes by only ever increasing the value.
Deletion
Deleting individual embedding states will delete the data in the embedding store. Again we use conditional deletions to handle out of order writes.
Deleting an entire embedding config triggers automatic cleanup of all data: we delete the associated embedding states and the vector database table. This reduces storage costs and lets us meet various data retention guarantees. This actually creates a very nice property to the system — the real meat of this post…
Operations In Practice — Migrations And Failures
Systems fail and requirements change. We needed a strategy that handled:
- Vector database Failures
- Database Corruption — the database exists, but is in a bad state
- Catastrophic Data Loss — the database is deleted or unavailable
- Vector Database Migrations
- Schema Migrations — storing new metadata
- Database Engine Migration — e.g. LanceDB to Milvus or vice versa
- Data Residency Migration — e.g. US to EU
- KMS migration — when a customer using our KMS feature rotates their encryption key
- Permission Changes
- AI Provider Changes — Airtable supports multiple AI providers. What if a user forbids use of OpenAI and only allows models served via Bedrock
Note: Embeddings can/should not be compared across models. So updates require re-embedding everything.
- MemApp Migrations
- Deprecating AI Models — We need to update the AI model to one that is still supported
- Updating the Embedding Strategy — If we change how we embed data, we re-embed everything to keep comparisons apples-to-apples
- MemApp Operations
- Updating Data Subscriptions — This changes the data we’re embedding, and so usually requires completely re-embedding the data
- Cloning a base — Airtable allows you to clone a database. We need separate vector stores to keep the data model sensible over time.
- Base Snapshot Restoration — Airtable has multi-year old snapshots that can serialized in a database
- MemApp Vector Database Synchronization
- MemApp corruption — If we don’t create embedding states for some of our data
- Detection Change Bugs — what if we don’t propagate changes to the vector store because we fail to detect them?
- Task Queue Failures — What happens if our task queue violates its “at least once delivery” of updates?
You can imagine many ways to handle these cases. One pattern I found myself coming up with over and over again was:
- Deleting the old embedding config (cleaning up old data if it exists)
- Creating a new new embedding config in the old ones place (possibly with new settings)
We call this process resetting the embedding config.
I realized we could handle all of these cases if any time the system detects that embeddings are, or about to become, invalid, we reset the embedding config.
Moving a base from the US to the EU is illustrative.
When a base moves from the US to the EU sensitive data related to the base must move to the EU, with nothing in the US remaining. Since embeddings are sensitive they must be moved as well. To handle this we delete every embedding config in the base, our system then automatically deletes all existing embedding data as part of the normal cleanup process. We then re-create the embedding configs with a configuration to store the data in the EU. Voila! All the embedding data for the base has now been migrated.
You can repeat this exercise for every single case listed above. This approach had a few tradeoffs we had to consider:
Cost
Regenerating embeddings incurs expenses, but these are manageable compared to storage and indexing costs from incremental updates.
Downtime
Resetting embeddings causes temporary unavailability of semantic search features. Given the rarity of resets and the speed of re-embedding (p99.9 under 2 minutes), this was acceptable.
Handling this kind of downtime is already necessary at the product level since users can trigger large scale generations in the product very easily (e.g. cloning a base).
Potential Runaway Resets
We had to implement safeguards to prevent continuous reset loops, which could lead to spiraling costs and prolonged downtime. We used a combination of metrics, alerts, rate limiting, and idempotent requests.
Conclusion:
Our embedding system isn’t perfect, but it’s resilient and adaptable. By accepting eventual consistency and designing for graceful handling of failures and migrations, we’ve built a foundation that supports powerful semantic search capabilities and are continuing to iterate on this system as we find new ways to leverage AI to increase the power of the Airtable platform.
Some other interesting topics we totally glossed over but may touch on in the future:
- Failures in the embedding generation
- Downtime for MemApp
- Managing global AI rate limits
- Choice of vector indices
- How we apply filters and permissions
