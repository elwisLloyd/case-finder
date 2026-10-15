# Enhancing Search Using Large Language Models

Источник: https://medium.com/whatnot-engineering/enhancing-search-using-large-language-models-f9dcb988bdb9

Enhancing Search Using Large Language Models
How we leveraged GPT to improve the Whatnot user experience
Yumeng Tao | Search Engineer & Grace Li | Machine Learning Scientist
Search functionality plays a pivotal role in the user experience of e-commerce apps, serving users’ high-intent discovery needs. Within the complex search process, one critical element is text input processing. Failing to accurately comprehend users’ input and provide relevant content can easily lead to misconceptions about the app.
Recent advancements in Large Language Models (LLMs) have significantly improved the capacity to detect and rectify misspelled words and to enhance overall text input expansion. Here, we’ll share how we adopted the Generative Pre-trained Transformer (GPT) — a well-established LLM — to enhance the search experience on Whatnot.
Problem Statement — Misspellings and Missed Opportunities
A common misspelling in the Whatnot search experience is “jewlery” instead of”jewelry.” Instead of recognizing the misspelling, most users naturally assume that Whatnot lacks jewelry-related content when they encounter a nearly empty “jewlery” search results page. Conversely, users can successfully discover, engage with, and purchase the jewelry they desire when we present an extensive “jewelry” search results page with relevant categories, live shows, and products.
We also observed that acronym/abbreviation queries, such as “lv” for “louis vuitton” or “nyfw” for “new york fashion week” tended to result in a low count of results/lower downstream engagement rates.
Figure I Query Expansion Generation and Serving
Query Expansion Generation and Serving
As illustrated in the flowchart above, our offline query expansion generation process follows these steps.
Data Collection
We begin by collecting search queries from logging, such as “funko pop,” “fine jewelry,” and “nyfw.”
Get Whatnot Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
On the backend, we log every search that is performed, including the query, any filters applied, as well as the SERP tab (Products, Shows, Users, etc.) that the user lands on after executing the search. Additionally, we have fields that allow us to join these event logs together in the data warehouse so that we can consider user behavior on three levels:
- SERP tab session: Actions the user takes on a specific SERP tab, without changing either the tab or the query (and filters).
- Query session: Actions the user takes for a specific query (and filters) across multiple SERP tabs.
- Search session: Actions the user takes while continuously engaging with Search, including SERP tag navigation and re-querying.
Tokenization
Next, we process these search queries into normalized tokens or unigrams for further analysis. This step includes some simple text processes:
- Normalization: Convert all queries into a lowercase format, ensuring that variations such as “Ipad Air,” “iPad air,” and “ipad Air” are transformed into the uniform format “ipad air.” Punctuation and emojis are also standardized or removed.
- Tokenization: Break down queries into individual units, known as tokens, by splitting them by white spaces (“ ”). For example, the original query “ipad air” would be processed into 2 tokens: “ipad” and “air”.
We gather frequently occurring tokens by summarizing their usage over the past 14 days. Specifically, if a token has been utilized in search queries more than 3 times during this period, we consider it as a token to be included in the subsequent GPT process.
GPT Rectification
For frequently occurring tokens described above, we send them to the GPT model along with a prompt designed to identify potential misspellings and to suggest expansion text from acronyms/abbreviations. This GPT call is made on an ad hoc/scheduled basis outside of the production code path since the user value of Search is heavily predicated on low latency (ideally sub-250ms).
The GPT model then generates corresponding spelling corrections and abbreviation expansions. Since the model is trained on such a wide, large collection of data, it has knowledge of brands such as “Xero” (shoes) or “MSCHF”, which would otherwise appear to be misspellings. This ability to handle real-world entities well means that we can do reasonable, basic handling of these cases in Search without having to do any knowledge graph construction/maintenance.
Post-processing
After receiving outputs from the GPT model, we put them into our query expansion cache. This is a tier in a production-level key-value store that maps from original query tokens to the lists of potential corrections/expansions, along with their associated confidence levels.
Query Expansion Serving
At request time, when a user executes a query during search time, our process follows these steps:
- Query Tokenization: We begin by processing the user’s query into tokens or unigrams.
- Query Expansion Lookup: Next, we refer to the query expansion cache to identify potential spelling corrections and abbreviation expansions related to the tokens of the user’s query. This is used to augment the query S-expression so that a user searching for “sdcc” will also get results matching “san diego comic con”.
- Search Result Generation: Finally, we generate a search result page from the combination of the original user query and the expanded queries retrieved and processed from our cache based on their confidence levels.
Compared to our previous query expansion method, this new GPT rectification-based approach has yielded substantial improvements in query expansion accuracy while also streamlining the generation and serving process significantly. For queries containing misspellings or abbreviations, we reduced irrelevant content by more than 50% compared to our previous method.
But we are not finished! This method means that the user can search “sdcc” and get results matching “san diego comic con”, but our current token-specific approach means that a user searching for “san diego comic con” will not get results matching “sdcc”. To support this, we will need to either 1) apply the equivalent query expansion process at indexing time 2) perform GPT rectification upon ngrams.
Next Steps
The query expansion process outlined above represents our initial attempts to leverage state-of-the-art machine learning techniques to enhance the search experience. We have a few exciting ongoing or upcoming initiatives:
- Semantic query expansion: This is approximately the same idea as semantic search (being able to search “star wars little green alien” to get Yoda results), but without requiring the real-time model inference and production-latency aNN index infrastructure.
- Shows and Product Description Keywords Extraction: Entity and attribute extraction from both search documents and queries to improve relevance and recall. Searching for “nike men’s sneakers size 11” should get the same set of results as searching “sneakers” with the “brand:nike gender:men size:11” filters applied. This can be combined with further LLM-powered knowledge graph-esque functionality to power related query/query refinement features.
- Image and Video Content Understanding: Content understanding of our entities allows us to do auto-population and quality validation of attributes tagging to improve the precision and recall of filtering/filters automatically extracted from queries. This is another precursor to full semantic search.
We are just getting started on leveraging state-of-the-art LLMs to enhance user experience across Whatnot. If you are interested in practical applications of machine learning in real-world products, join us!
