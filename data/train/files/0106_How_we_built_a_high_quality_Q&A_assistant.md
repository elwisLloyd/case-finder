# How we built a high quality Q&A assistant

Источник: https://medium.com/airtable-eng/how-we-built-a-high-quality-q-a-assistant-738ae9efeb7a

In June 2025, Airtable launched Omni, an AI assistant that can build custom apps and extract insights from the vast amount of information stored in an Airtable base, such as customer feedback, marketing campaign data, and product details. Developing an agent that adapts to a dynamic real-world environment and consistently provides high-quality answers required numerous iterations and trial and error. This blog post details methods for building an agent capable of researching complex databases.
Problem Description
Let’s start by imagining you are the owner of a product operations database below:
Building a reliable Q&A agent with a large language model (LLM) is no easy task. While LLMs excel at quickly processing and summarizing large volumes of information, far faster than any human, they also come with significant limitations. One of the biggest challenges is their tendency towards unpredictable reasoning: they often jump to conclusions prematurely, compound initial mistakes, or hallucinate entirely inaccurate responses. These issues are further amplified when dealing with large, complex table schemas or vague user questions. In practice, a system that gets answers right only half the time isn’t just unhelpful—it’s unusable. At Airtable, we’ve developed and applied a range of techniques to overcome these challenges and deliver a production-ready assistant that users can trust.
High-Level Architecture
We’ve shared the agentic framework in a previous blog post, which discusses how an LLM can call tools and make dynamic decisions in sequence to solve a problem. Below is a diagram with inputs (purple) and outputs showcasing how it works in the Q&A agent:
This system is particularly effective at solving problems that require multiple steps of reasoning. At its core, it mimics a human when trying to find answers from a database—explores the structure of each table, applies relevant filters, re-evaluates upon new information and performs quantitative or qualitative analysis. The primary components are detailed below.
Contextual schema exploration
The first and foremost challenge is: given hundreds and thousands of records that far exceeds LLM’s context window, how can we find an answer in a token-efficient manner? We started by providing the schema for all tables in the base, but even that could be too much for the LLM to process. For a larger base, the schema alone would consume most of the context window. Hence we break down data exploration into 2 steps:
- A tool to understand schema
- A tool to query data
Real world schemas are often noisy, with deprecated or empty columns and fields that are highly similar or ambiguous. We’ve found that the LLM is more successful when we pare down the initial context to the most useful and salient information:
- High level schema (e.g. table names, descriptions, primary column, relationships between tables)
- A more detailed schema for the information the user is actively viewing
- Example records for the table the user is actively viewing
This information helps clarify user intents and even predicts what they are likely doing next. We’ve found it not only useful for question answering, but also in offering proactive suggestions.
Planning and replanning
Chain of thought is proven to be an effective mechanism to improve the reasoning capability of LLMs. Instead of directly providing an answer, the model is guided to articulate its reasoning process step-by-step, mimicking how humans might solve a problem. This approach helps LLMs tackle complex tasks that require multi-step thinking by breaking them down into smaller, manageable parts. Anthropic’s Sonnet 4 has built-in ‘thinking tokens’ and lately ‘interleaved thinking’ to facilitate this process.
Get Ruoni Wang’s stories in your inbox
Join Medium for free to get updates from this writer.
In the system, we incorporate a planning step, as well as steps to replan upon discovery of new data. We built an evaluation system that captures complex scenarios where data schema is confusing and multiple explorations or backtracking may be required in the process. An example below illustrates replanning:
Hybrid search
Retrieval augmented generation (RAG) is a common technique employed by LLM tools for efficient data retrieval. The system’s efficacy depends on 2 factors:
1. Narrow down the data sources to search
2. Efficient search results ranking
We provide the LLM with tools to filter and search for base data. The filtering step narrows the search scope, while keyword and semantic search help identify results that are relevant for the user’s question. By combining both search methods, we can prioritize exact matches for named entities while still finding relevant results even when search queries are vague or worded differently. As LLM is subject to random errors, it could overlook tables or columns in the filtering step. We introduce a correction mechanism where, if no meaningful data was found, we perform the search again on a wider scope from the initial attempt. This provides a fallback for additional fault tolerance. Here is an overview of the system:
Citations
Citation of sources is important for LLM generated answers because citations allow users to verify information and reduce the risk of relying on potentially inaccurate responses. It is also an effective mechanism to minimize hallucination. We leverage inline citation tags for any derived information—whether it be from internet sources or database sources. This allows us to achieve compact and flexible citations that can later be turned into rich content.
The LLM cites the sources alongside each piece of information with inline citation tags. In the above example, the generation ends with “… a question before Justin <datasource id=recIdxxxxx/>”. This style of citation follows the natural flow of conversation and has additional benefits of being compact, model agnostic and flexible.
A common challenge here is that unique IDs are not token efficient. They don’t follow natural language patterns and a 17-character ID can consume up to 15 tokens. This resulted in increased cost and latency, especially when thousands are included in a single invocation. To address this, we encode database IDs into contextually relevant, token-efficient representations that can be as short as 3 tokens. We also apply a checksum algorithm to minimize collisions. This approach has yielded over 30% improvements in latency and 15% cost savings.
Evaluations
Lastly, it’d be hard to measure the impact of any approach without a robust evaluation system. We have two primary sources of evaluation:
1). An eval suite with curated lists of questions
2). Live feedback from production data
The eval suite is a collection of questions curated from customer research and production usage. We use deterministic or LLM-as-a-judge scorers to output result scores for various metrics we are interested in. These examples are selected to represent Omni’s most common use cases and failure points. We augment the list as more representative examples come in from usage. The evals are very helpful for us to iterate on any aspect of the system quickly and confidently. Since Omni is model agnostic, they also enable us to compare performance across models and track regressions.
Conclusion and looking forward
Building Omni was an exciting challenge. The techniques detailed in this post have been crucial in delivering high-quality and reliable answers. As we look to the future, our next challenge is scaling these capabilities to even larger, more heterogeneous bases with low latency, and enhancing LLM reliability during extended iterative operations.
Acknowledgements
Many thanks to Yifei Pack, Lee Weisberger, Jason Bradshaw, Justin Lu, Ameya Khare, Nabeel Farooqui and Trijeet Mukhopadhyay for their work on this project and to Lee Weisberger, Justin Lu and Kenzo Fong for editorial input for this blog post.
