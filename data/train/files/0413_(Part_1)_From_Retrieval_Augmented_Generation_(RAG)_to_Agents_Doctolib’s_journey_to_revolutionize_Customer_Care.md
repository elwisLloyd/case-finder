# (Part 1) From Retrieval Augmented Generation (RAG) to Agents : Doctolib’s journey to revolutionize Customer Care

Источник: https://medium.com/doctolib/part-1-from-retrieval-augmented-generation-rag-to-agents-doctolibs-journey-to-revolutionize-d34610eeb550

(Part 1) From Retrieval Augmented Generation (RAG) to Agents : Doctolib’s journey to revolutionize Customer Care
Abstract
Founded in 2013, Doctolib is a leading e-health company in Europe. We provide health professionals with services to improve the efficiency of their organization, transform their patients’ experience, and strengthen cooperation with other practitioners.
As part of our AI ambition, our team of 40 data scientists is working on developing groundbreaking AI products (such as a consultation assistant which we will release in Q4 2024). We also infused our internal processes and ways of working with top notch AI. This article talks about how we are trying to make our customer care services even better and more efficient with the use of Large Language Models (LLMs), how we started with well known solutions such as Retrieval-Augmented Generation (RAG) (part 1), how we are conducting R&D on more powerful solutions such as Agentic frameworks (multiples LLMs (agents) interacting together) and how it questions the way we develop products at large (part 2).
Introduction
Our story starts with providing top-notch customer care service to our users.
To make this happen, we continuously improve our product daily to make it simpler to use for practitioners. We are also using Data Science and AI to enhance our services.
While simplistic rules-based bots are common, they are highly limited. They can’t adapt to users or their context. These bots rely on pre-programmed scripts, which prevents them from adapting to users or their specific contexts, leading to suboptimal user experiences. Yet, the advent of Large Language Models (LLMs) has transformed how we interact with information. They were a big step forward in understanding user intent. However, they are trained and thus have knowledge solely on a large corpus of public data. This lack of access to recent and private data can limit the accuracy and depth of their answers. This is where Retrieval-Augmented Generation (RAG) steps in. It enables addressing this by providing LLMs context specific content. It leads to far better answers.
Standard RAG is good at simple queries across a few documents, like a FAQ database. But, it has pitfalls and can’t answer complex user questions.
After reaching the ceiling using RAG we started looking at agentic architecture. It adds a layer of intelligence by using LLM-based agents. They can improve the quality of complex answers by performing actions like fetching data, running functions or executing API calls. They can better understand and enrich user’s questions, but also interact with users.
Agentic frameworks promise a better user experience than bots. They should also be more reliable and scalable than rules-based systems, which need constant updates for new tasks. Also, by understanding unstructured data it is way more robust to the variation of natural language.
But first, let’s start by exploring how a RAG system can already transform your customer care services and understand what are its limitations.
As everyone we started with a Retrieval Augmented Generation (RAG)
RAG is simple yet powerful architecture
Retrieval augmented generation (RAG) combines the power of large language models with dynamic access to external knowledge. Instead of relying only on pre-existing training data, RAG pulls in up-to-date knowledge to provide more accurate and relevant answers. This blend of static and dynamic information enhances the AI’s ability to respond to specific and complex queries.
The basic RAG pipeline involves embedding a user query, retrieving relevant documents to the query, and passing the documents to an LLM for generation of an answer grounded in the retrieved context.
Get Anouk Barnoud’s stories in your inbox
Join Medium for free to get updates from this writer.
In our case, the RAG is based on the FAQ articles updated daily. We currently use GPT-4o as a LLM, hosted on the Azure OpenAI service by Microsoft for security and confidentiality issues, OpenSearch as the Vector Database containing the embeddings of the chunks of the FAQ articles. As this step alone does not provide good enough results, we improved it by implementing a re-ranking brick. It is essential to keep the Vector Database embeddings up to date. To do so, we implemented and deployed a data pipeline that retrieves the up-to-date FAQ and embeds it in the vector database everyday.
We built and deployed an evaluation tool based on a framework called Ragas. It gives us metrics to evaluate our RAG system, both component-wise and end-to-end, such as :
- Context precision which measures the signal-to-noise ratio of the retrieved context
- Context recall which measure if all the relevant information required to answer the question was retrieved
- Faithfulness which measures the factual accuracy of the generated answer
- Answer relevancy which measures how relevant the generated answer is to the question.
Those are RAG specific metrics. They differ from the classical Natural Language Processing (NLP) metrics such BLEU or ROUGE scores that do not recognize semantic similarity. Also, transformer-based metrics such as BERTScore do not check if answers are factually consistent with source documents. With this framework, we can run experiments to optimize our system.
One first key element was the need for annotation. We needed a dataset of “Groundtruth records”, which are perfect answers for our system. This evaluation brick lets us optimize our system’s parameters. We tested the performance of different methods: hybrid search, prompt engineering, LLM parameters, chunking methods, embedding models and fine-tuning, reranking methods…
This improved our vanilla RAG. It has had a significant impact on customer care cases deflection with a 20% reduction. Customer care agents can now focus on more complex cases.
Today, user experience (UX) is key to an AI product’s success and adoption. So, we worked with designers to improve our UX to meet users’ expectations. The UX iterations showed a need for a classifier to activate or not our system and the big challenges on latency.
A key to improving user experience is to reduce the number of times our system can’t answer the user. To achieve this, we developed a Machine Learning classifier model to predict if our system could answer the user query. It diminished the reach of our tool but made it more precise and impactful.
As we embarked on the journey of implementing a RAG, we faced a major challenge: the latency. It is the delay between a request being initiated and a response being received, that comes with using LLMs. We had a long journey to go from a latency of 1 min to less than 5s. To do so, we tested several strategies: optimizing the code, using Provisioned Throughput Units (PTUs) to guarantee consistent throughput, using smaller models and implementing streaming for the generation.
However RAG comes with limitations
The current RAG system, despite improvements, has limits. It struggles with complex user queries and resolving issues beyond FAQs. It only gives descriptive answers. Also, the system is not user-friendly. Its UX does not allow for seamless conversation.
To tackle those challenges, we explored agentic frameworks as a potential solution. They enable back office actions, enriching queries with more context or allow user interaction. We will deep dive into them in a second article. Stay tuned!
Contacts and thanks
Many thanks to the incredible team that worked on the project and developed the POC : Vincent Cornet Louis Melliorat Julien Richard Sinda SALEM
Don’t hesitate to contact us if you have any question :
- Anouk Barnoud : anouk.barnoud@doctolib.com
- Sinda SALEM : sinda.salem@doctolib.com
- Vincent Cornet : vincent.cornet@doctolib.com
- Julien Richard : julien.richard@doctolib.com
- Louis Melliorat: louis.melliorat.pro@gmail.com
