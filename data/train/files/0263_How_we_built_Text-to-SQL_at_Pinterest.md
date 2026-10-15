# How we built Text-to-SQL at Pinterest

Источник: https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff

Adam Obeng | Data Scientist, Data Platform Science; J.C. Zhong | Tech Lead, Analytics Platform; Charlie Gu | Sr. Manager, Engineering
Writing queries to solve analytical problems is the core task for Pinterest’s data users. However, finding the right data and translating an analytical problem into correct and efficient SQL code can be challenging tasks in a fast-paced environment with significant amounts of data spread across different domains.
We took the rise in availability of Large Language Models (LLMs) as an opportunity to explore whether we could assist our data users with this task by developing a Text-to-SQL feature which transforms these analytical questions directly into code.
How Text-to-SQL works at Pinterest
Most data analysis at Pinterest happens through Querybook, our in–house open source big data SQL query tool. This tool is the natural place for us to develop and deploy new features to assist our data users, including Text-to-SQL.
Implementing Text-to-SQL
The Initial Version: A Text-to-SQL Solution Using an LLM
The first version incorporated a straightforward Text-to-SQL solution utilizing an LLM. Let’s take a closer look at its architecture:
The user asks an analytical question, choosing the tables to be used.
- The relevant table schemas are retrieved from the table metadata store.
- The question, selected SQL dialect, and table schemas are compiled into a Text-to-SQL prompt.
- The prompt is fed into the LLM.
- A streaming response is generated and displayed to the user.
Table Schema
The table schema acquired from the metadata store includes:
- Table name
- Table description
- Columns
- Column name
- Column type
- Column description
Low-Cardinality Columns
Certain analytical queries, such as “how many active users are on the ‘web’ platform”, may generate SQL queries that do not conform to the database’s actual values if generated naively. For example, the where clause in the response might bewhere platform=’web’ as opposed to the correct where platform=’WEB’. To address such issues, unique values of low-cardinality columns which would frequently be used for this kind of filtering are processed and incorporated into the table schema, so that the LLM can make use of this information to generate precise SQL queries.
Context Window Limit
Extremely large table schemas might exceed the typical context window limit. To address this problem, we employed a few techniques:
- Reduced version of the table schema: This includes only crucial elements such as the table name, column name, and type.
- Column pruning: Columns are tagged in the metadata store, and we exclude certain ones from the table schema based on their tags.
Response Streaming
A full response from an LLM can take tens of seconds, so to avoid users having to wait, we employed WebSocket to stream the response. Given the requirement to return varied information besides the generated SQL, a properly structured response format is crucial. Although plain text is straightforward to stream, streaming JSON can be more complex. We adopted Langchain’s partial JSON parsing for the streaming on our server, and then the parsed JSON will be sent back to the client through WebSocket.
Prompt
Here is the current prompt we’re using for Text2SQL:
Evaluation & Learnings
Our initial evaluations of Text-to-SQL performance were mostly conducted to ensure that our implementation had comparable performance with results reported in the literature, given that the implementation mostly used off-the-shelf approaches. We found comparable results to those reported elsewhere on the Spider dataset, although we noted that the tasks in this benchmark were substantially easier than the problems our users face, in particular that it considers a small number of pre-specified tables with few and well-labeled columns.
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
Once our Text-to-SQL solution was in production, we were also able to observe how users interacted with the system. As our implementation improved and as users became more familiar with the feature, our first-shot acceptance rate for the generated SQL increased from 20% to above 40%. In practice, most queries that are generated require multiple iterations of human or AI generation before being finalized. In order to determine how Text-to-SQL affected data user productivity, the most reliable method would have been to experiment. Using such a method, previous research has found that AI assistance improved task completion speed by over 50%. In our real world data (which importantly does not control for differences in tasks), we find a 35% improvement in task completion speed for writing SQL queries using AI assistance.
Second Iteration: Incorporating RAG for Table Selection
While the first version performed decently — assuming the user is aware of the tables to be employed — identifying the correct tables amongst the hundreds of thousands in our data warehouse is actually a significant challenge for users. To mitigate this, we integrated Retrieval Augmented Generation (RAG) to guide users in selecting the right tables for their tasks. Here’s a review of the refined infrastructure incorporating RAG:
- An offline job is employed to generate a vector index of tables’ summaries and historical queries against them.
- If the user does not specify any tables, their question is transformed into embeddings, and a similarity search is conducted against the vector index to infer the top N suitable tables.
- The top N tables, along with the table schema and analytical question, are compiled into a prompt for LLM to select the top K most relevant tables.
- The top K tables are returned to the user for validation or alteration.
- The standard Text-to-SQL process is resumed with the user-confirmed tables.
Offline Vector Index Creation
There are two types of document embeddings in the vector index:
- Table summarization
- Query summarization
Table Summarization
There is an ongoing table standardization effort at Pinterest to add tiering for the tables. We index only top-tier tables, promoting the use of these higher-quality datasets. The table summarization generation process involves the following steps:
- Retrieve the table schema from the table metadata store.
- Gather the most recent sample queries utilizing the table.
- Based on the context window, incorporate as many sample queries as possible into the table summarization prompt, along with the table schema.
- Forward the prompt to the LLM to create the summary.
- Generate and store embeddings in the vector store.
The table summary includes description of the table, the data it contains, as well as potential use scenarios. Here is the current prompt we are using for table summarization:
Query Summarization
Besides their role in table summarization, sample queries associated with each table are also summarized individually, including details such as the query’s purpose and utilized tables. Here is the prompt we are using:
NLP Table Search
When a user asks an analytical question, we convert it into embeddings using the same embedding model. Then we conduct a search against both table and query vector indices. We’re using OpenSearch as the vector store and using its built in similarity search ability.
Considering that multiple tables can be associated with a query, a single table could appear multiple times in the similarity search results. Currently, we utilize a simplified strategy to aggregate and score them. Table summaries carry more weight than query summaries, a scoring strategy that could be adjusted in the future.
Other than being used in the Text-to-SQL, this NLP-based table search is also used in the general table search in Querybook.
Table Re-selection
Upon retrieving the top N tables from the vector index, we engage an LLM to choose the most relevant K tables by evaluating the question alongside the table summaries. Depending on the context window, we include as many tables as possible in the prompt. Here is the prompt we’re using for the table re-selection:
Once the tables are re-selected, they are returned to the user for validation before transitioning to the actual SQL generation stage.
Evaluation & Learnings
We evaluated the table retrieval component of our Text-to-SQL feature using offline data from previous table searches. This data was insufficient in one important respect: it captured user behavior before they knew that NLP-based search was available. Therefore, this data was used mostly to ensure that the embedding-based table search did not perform worse than the existing text-based search, rather than attempting to measure improvement. We used this evaluation to select a method and set weights for the embeddings used in table retrieval. This approach revealed to us that the table metadata generated through our data governance efforts was of significant importance to overall performance: the search hit rate without table documentation in the embeddings was 40%, but performance increased linearly with the weight placed on table documentation up to 90%.
Next Steps
While our currently-implemented Text-to-SQL has significantly enhanced our data analysts’ productivity, there is room for improvements. Here are some potential areas of further development:
NLP Table Search
- Metadata Enhancement
Currently, our vector index only associates with the table summary. One potential improvement could be the inclusion of further metadata such as tiering, tags, domains, etc., for more refined filtering during the retrieval of similar tables.
- Scheduled or Real-Time Index Update
Currently the vector index is generated manually. Implementing scheduled or even real-time updates whenever new tables are created or queries executed would enhance system efficiency.
- Similarity Search and Scoring Strategy Revision
Our current scoring strategy to aggregate the similarity search results is rather basic. Fine-tuning this aspect could improve the relevance of retrieved results.
Query validation
At present, the SQL query generated by the LLM is directly returned to the user without validation, leaving a potential risk that the query may not run as expected. Implementing query validation, perhaps using a constrained beam search, could provide an extra layer of assurance.
User feedback
Introducing a user interface to efficiently collect user feedback on the table search and query generation results could offer valuable insights for improvements. Such feedback could be processed and incorporated into the vector index or table metadata store, ultimately boosting system performance.
Evaluation
While working on this project, we realized that the performance of text-to-SQL in a real world setting is significantly different to that in existing benchmarks, which tend to use a small number of well-normalized tables (which are also prespecified). It would be helpful for applied researchers to produce more realistic benchmarks which include a larger amount of denormalized tables and treat table search as a core part of the problem.
To learn more about engineering at Pinterest, check out the rest of our Engineering Blog and visit our Pinterest Labs site. To explore and apply to open roles, visit our Careers page.
