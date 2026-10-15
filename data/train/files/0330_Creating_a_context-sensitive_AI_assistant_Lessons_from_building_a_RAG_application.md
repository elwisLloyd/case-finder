# Creating a context-sensitive AI assistant: Lessons from building a RAG application

Источник: https://vectorize.io/creating-a-context-sensitive-ai-assistant-lessons-from-building-a-rag-application/

At Vectorize, we want to make it fast and easy for our users to create retrieval-augmented generation (RAG) pipelines to power their AI applications. We’ve tried to make it as intuitive as possible and continue to iterate on our user interface towards this goal. However, when you support dozens of integrations with third-party vector databases, AI platforms, and data sources, it’s inevitable that the user will need additional information. Because of that, we’ve invested a lot of time and energy in our documentation to help people along.
However, we still get questions about how to do things that are explained in our documentation. This is not really a big surprise. It’s human nature to try to figure things out before going to the documentation. And it doesn’t help that reading our docs–like with most applications–requires you to leave the user interface and go to a different site (https://docs.vectorize.io). You have to context switch from “getting something done” to “searching the docs.” Once you get your answer, you need to switch back to “getting something done” mode.
While we do provide an Intercom chat interface so our users can ask us directly for help, we aren’t always immediately available to help, and some people are reluctant to “bother” someone else with their problems. Given that one of the most common use cases for our RAG pipelines is some sort of customer support assistant, it made sense for us to set out to build something like this for our users.
AI assistant > chat-with-our-docs
So what shape should our AI-powered assistant take? Well, we could build a standalone chat-with-your-docs chatbot, but that still requires you to leave the user interface to go to the chat interface, which is similar to the friction of going to the docs site. It would be better to have an AI assistant built right into the user interface. The user gets the information they need when they need it without a major context switch.
An AI assistant with access to our documentation integrated right into the user interface seemed like the right solution to the problem, so that’s what I set out to build. While building it, I learned some valuable lessons about how to set up RAG pipelines, how to optimize RAG retrieval, how to prompt a large language model (LLM) for a RAG application, and how to measure the quality of what you are building.
I will take you through the process of building the AI assistant. After that, I will wrap up with a set of concrete tips you can use when building your own RAG application.
RAG pipeline
Since our AI assistant needs to be an expert on our documentation, this is an obvious use for retrieval augmented generation (RAG). LLMs are not trained on the details of our product so we need to provide them with additional information or they will just make stuff up (hallucinate). We could fine tune a foundational model, but we are constantly updating our docs so repeated fine tuning is not practical. What makes the most sense is a RAG pipeline that takes the unstructured content from our docs site, transforms it into embedding vectors, and pushes it into a vector database. Once it’s in a vector database we can use similarity search to provide relevant context for the LLM to use when generating a response to the user’s question.
So we needed to start with a RAG pipeline. How to build that pipeline was an easy choice–I used Vectorize itself. This is an eat-your-own-dogfood option and may feel like a shameless plug (since I am a co-founder and CTO of Vectorize), but I honestly believe that using Vectorize was the fastest and easiest way to build the retrieval pipeline for my AI assistant. I didn’t have to learn and wrangle with Python frameworks or think about where the code would run. I didn’t have to worry about how to update the vector embeddings when the documentation changed. I just had to configure a few things, and my Vectorize RAG pipeline was quickly up and running.
Using multiple sources
Originally, I was just going to scrape the docs site using the web crawler connector. But because Vectorize supports multiple source connectors in a pipeline and has integrations with Discord and Intercom, I was also able to easily pull data from two other sources of helpful information–the answers we had provided to questions asked by other users. When we tag approved answers in Discord or Intercom, they get automatically processed by the RAG pipeline and put into our vector index.
This ability to pull data from multiple sources in real-time is really powerful because it makes our RAG pipeline self improving. As we answer support questions and add or improve the documentation, that information automatically becomes available in the vector index. And if you remove incorrect documentation or support answers, the vectors are automatically removed. Our vector index gets better over time just through our normal day-to-day activities.
Retrieving from the vector database
For the retrieval from the vector index, I used Vectorize’s retrieval endpoint. Although a RAG pipeline writes to your vector database and you can query that directly if you want, you would still have to handle creating a vector embedding to use in the similarity search. The retrieval endpoint takes care of this for you using the same embedding model the pipeline uses when populating the vector database.
The retrieval part of the RAG equation boils down to this fetch code:
const payload = {
   question,
   numResults,
   rerank,
 };
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), timeout);
const response = await fetch(retrievalEndpoint, {
   method: "POST",
   headers: {
       "Content-Type": "text/plain",
       Authorization: `${dataplaneApiKey}`,
   },
   body: JSON.stringify(payload),
   signal: controller.signal,
});
clearTimeout(timeoutId);
That code will return the specified number of results of a similarity search against your vector database with the provided question text. It also will pass the results through a reranking model if you set rerank to true. More on why this is useful later.
Context-sensitivity is king
With the RAG pipeline and retrieval worked out, I could start working on the fun part–building the interface and the interactions with the LLM. Since our user interface is a React application, I built an AiAssistant React component that I could add to every page where I thought the user might need some assistance. For example, here is the component on the page where the user configures their integration to Google Drive:
When the user clicks on “Ask AI” a chat window appears at the top right of screen:
As I was building the component, I had an important insight. Because the AI assistant is integrated into the product, it has an idea of what the user is trying to do. My first thought was to seed the assistant with a question that the user is most likely to have on this page. If the user sees that question and it matches what they are wondering about, they are likely to try the AI assistant. It seems like an easy way to encourage users to give the AI assistant a try.
There is no magic with the seed question. I just pass it as a hard-coded contextualQuestion whenever I use the component. Here’s an example:
<AiAssistant
    contextualQuestion={"How to manage retrieval endpoint tokens?"}
    topic={"Retrieval endpoint token management"}
/>            
For this instance of the component, I pass the question “How to manage retrieval endpoint tokens?” as a prop. As you can see in the example, in addition to passing the contextualQuestion, I am also passing a topic, which generally describes what the user is doing on the page. Why did I add this? Because I discovered that it helps a lot with retrieval.
Retrieval is better with context
Although I seed the AI assistant with a good question, users are allowed to delete it and ask a different question (or ask follow-up questions). And users don’t always formulate good questions for retrieval. Imagine in the scenario above where the AI assistant component is on the Retrieval Endpoint Token page, but instead of the seed question, the user asked this question: “When does it expire?” By “it” they most likely mean retrieval endpoint token, but if we just use that question for the similarity search, we won’t necessarily get any information about the retrieval endpoint tokens since that semantic information (“retrieval endpoint token) is not in the question.
One way to deal with this in a RAG application is query rewriting. With query rewriting, you send the question plus some context to an LLM and ask it to rewrite the question so that it would be effective for retrieval. The context is important here, since without it the LLM can’t really write a better question (except for maybe fixing up the spelling and grammar). With query rewriting the context is typically the chat history. However, with the AI assistant I don’t want the user to have a long conversation to get the answer they want. I want them to get the answer on the first shot.
Because of where the AI assistant is located I can infer the topic that they are interested in. That is what the topic prop on the component is for–giving the context for the question the user is going to ask. I could send this topic plus the question to an LLM for query rewriting and I may do this in the future, but for the first release of the AI Assistant I was getting good results by just appending the topic to the question when calling the retrieval endpoint, like this:
// Prefix the question with the topic to improve retrieval
const contextualizedQuestion = `(${topic}) ${question}`;
Now whenever the user asks a question, the topic is part of the question, which means that we get results that are semantically similar to both the question and the topic. When I added this to the retrieval, it really improved the quality of the responses. The AI assistant was no longer giving unrelated answers.
Irrelevant results
Using the contextual information I was able to make sure the retrieval contained some information about the topic the user was most interested in. However, this didn’t guarantee that it would only contain information about that topic. When doing similarity search using a vector database, if you ask for 5 results, it gives you the 5 most similar results. Some of them may be highly similar and some may only be marginally similar, but you asked for 5 results so the database will give you that many.
Keep in mind that you are ultimately going to send the retrieved data to the LLM to generate a response to the user. Although current LLMs all have large context windows so you can send them a lot of data, sending them poor quality data will do exactly what you would expect: confuse them.
I’ll give you a concrete example. Many of the integrations in Vectorize require the user to specify an API key to authenticate with the service. If the user is trying to configure the Elasticsearch integration and asks the AI assistant a question about the API key, the retrieval will come back with results from Elasticsearch but also from other integrations that use API keys.
Vectorize has a handy feature called the RAG Sandbox so you can simulate the questions your users are asking and see exactly what is retrieved and how an LLM (from Groq and OpenAI) will use that data.
If I go to the RAG sandbox and send the question to my pipeline like it would be done in the AI assistant in this scenario, I get these results:
| Source | Similarity | Relevance | 
| https://docs.vectorize.io/tutorials/elastic-quickstart | 0.72417 | 0.97080 | 
| https://docs.vectorize.io/integrations/vector-databases/elastic | 0.73912 | 0.95498 | 
| https://docs.vectorize.io/integrations/vector-databases/elastic | 0.71257 | 0.91086 | 
| https://docs.vectorize.io/tutorials-and-how-to-guides/how-to-guides/setup-an-s3-bucket | 0.71880 | 0.00986 | 
| https://docs.vectorize.io/tutorials-and-how-to-guides/tutorials/couchbase-quickstart | 0.71165 | 0.00007 | 
As you can see, the first 3 results are from pages related to Elasticsearch, but the last two are about S3 buckets and Couchbase (a different vector database). We could send all 5 of these results to the LLM to use when generating the answer, but the last 2 are not about Elasticsearch at all and could lead to poor results. When I was testing this, sometimes the model would respond with information about S3 API keys (likely because S3 is a common topic in its training data), or it would ramble on about S3 and Couchbase keys when the user was only interested in Elasticsearch keys. 
The obvious solution is to filter out the information about S3 and Couchbase. But how do we do that? If you look at the similarity scores returned by the vector database, there is really little difference between them, ranging from 0.71 to 0.74. We can’t just filter out the bottom 2 results because it won’t work in all cases. And based on similarity scores, we can’t really be sure where to draw the line.
Relevance scoring with a reranking model
But look at those relevance scores. There is a huge difference between those. The Elasticsearch results have a relevance score of 0.91 to 0.97. But the results about S3 and Couchbase have relevance scores below 0.01. It’s obvious from those metrics that the S3 and Couchbase results should be tossed out.
How are these relevance scores calculated? This is done using a specialized model called a reranking model. The name “rerank” suggests how these models have been traditionally used: to rerank results from a search engine so that the best results appear at the top of this list. What they are actually doing is calculating how relevant a result is to a question and assigning it a relevance score. Both the question and the answer are passed to a specially trained model to calculate the scores. Then the model returns the answers, reranked from most to least relevant according to those scores.
Our Vectorize retrieval endpoint (and RAG sandbox) has built-in support for reranking and relevance scoring if you set rerank to true when calling the endpoint. This makes it easy to filter out responses that have low relevance to the question. For the AI assistant, I found by experimenting that a relevance threshold of 0.5 works well. Any data retrieved below that threshold is not sent to the LLM.
Anti-hallucination prompting
So that’s the full retrieval part of the equation. The next part is the generation of the response to the question. I am using standard prompting techniques here, inserting the question and the retrieved data into the prompt and then instructing the LLM to answer the question in Markdown format (for better presentation).
I want to call out a couple things on the prompting. I am including the same topic I used for the retrieval in the prompt to help keep the LLM on track:
"""
Unless the question specifies otherwise, assume the question is related to 
this general topic: {topic}.
"""
This is combined with the most important part of the RAG prompt: the instruction to only use the retrieved content in the answer:
`
This is very important: if there is no relevant information in the texts or
there are no available texts, respond with "I'm sorry, I couldn't find an 
answer to your question."
`
This instruction prevents the LLM from hallucinating an answer to the question. Without this and the additional emphasis (“This is very important”), in testing the LLM would make up answers about topics that we hadn’t written any documentation for. We noticed this happening in our development environment for features that were in development but had not been released and therefore did not have any documentation on our docs site.
`
These knowledge bases texts come from various sources, including documentation, 
support tickets, and discussions on platforms such as Discord. Some of the 
texts may contain the names of the authors of the resource or a person asking a question.
Never include these names in your answer.
`
This prompt prevents the LLM from quoting any users and also filters out any names that may have leaked into the conversation (ex. “Thanks for your help, Chris”).
As for the LLM itself, we have been using the Llama 3.1 70B model hosted on Groq. We have gotten good results from this model, which is lightning fast due to the Groq service and its relatively small size. A larger model might have been able to deal better with low relevance data, but with our relevance filtering we have a more deterministic system with better performance (low latency, lower cost).
Monitoring and feedback
Any time you build a system like this, you should gather user feedback to see how it is performing. For our AI assistant, we used standard thumbs-up and thumbs-down icons for the users to click on after an answer.
Clicking on these buttons sends messages to our analytics system so we can track how users are responding to our AI assistant.
Another type of monitoring that we are keen to add is tracking of the relevance of the responses from the retrieval. This is a feature that is on the Vectorize roadmap. It will allow you to see how well the system is doing at retrieving relevant information based on users’ actual questions. Not only can it point to a need for query rewriting, a low score could also mean there are blind spots in your data. For example, you may have released a new, popular feature but the documentation on it is thin, so when people ask questions about it the retrieval doesn’t come up with much. This should be visible in your relevance scores over time and will alert you that you have a problem somewhere in your RAG pipeline.
Since this is on the Vectorize roadmap, we didn’t build it into the AI assistant, but having a metric to track the quality of the RAG pipeline retrievals over time is highly recommended and something we will have in the future.
Lessons learned
That’s a quick overview on how we build our AI assistant for Vectorize. It was a good exercise in eating-our-own dogfood, but it also led to some valuable learnings along the way:
- Use multiple, real-time sources. Your docs aren’t the only source of information. Make sure to pull data from as many sources as you can and update the pipeline regularly to build an automatic, self-improving system.
- Use context to improve the quality of your application. Because LLMs just figure things out from little context, we tend to forget that context helps them do a better job and keep them on track.
- Use context in your retrievals. If you want to make sure your semantic search yields the best results make sure to include the context clues in the retrieval, whether that be using query rewriting or, as we did, include the context information in the text for the similarity search.
- Use a reranking model to filter out low relevance information. Semantic search is great, but you should pass your data to a reranking model to score the relevance of each response and filter out the low ones. This makes the LLM’s job much easier.
- Don’t forget the prompt engineering. Even though we are retrieving highly relevant information, you still need to be clear in your instructions to the LLM, especially to not hallucinate. If done well, you can use smaller, cheaper models to get good results.
- Monitoring the results. Don’t forget to monitor the quality of the user responses and the RAG pipeline retrievals. This can alert you to blind spots in your information.
I had fun building our AI assistant and learned a few things along the way. I hope you find this useful, and if you do try out Vectorize, please also give the AI assistant a try and let me know how it worked for you.
