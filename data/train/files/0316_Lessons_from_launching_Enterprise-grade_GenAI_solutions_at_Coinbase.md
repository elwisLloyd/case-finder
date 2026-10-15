# Lessons from launching Enterprise-grade GenAI solutions at Coinbase

Источник: https://www.coinbase.com/blog/lessons-from-launching-enterprise-grade-genAI-solutions-at-Coinbase

Lessons from launching Enterprise-grade GenAI solutions at Coinbase
Operationalizing GenAI requires optimizing for latency and availability, beyond accuracy and cost
Operational Challenges of GenAI
GenAI can revolutionize industries by enhancing their efficiency and productivity. We initially began our GenAI journey at Coinbase thinking that we would need to optimize between cost and accuracy i.e. choose the best LLM given our cost constraints. But very soon, we realized that developing enterprise-grade LLM solutions involves several further challenges like trust and safety, cost and scalability, and an evolving landscape of LLMs.
Finally, the lack of availability of models with appropriate QoS was an unexpected surprise. Let’s elaborate further on the decisions which a company needs to make, in order to build and launch an enterprise grade product using LLMs. 
Note: Coinbase’s customer-facing conversational LLM chatbot, serving all our US consumers, was launched in June, 2024 - we’ll follow up with more details of that architecture, in a subsequent blog post.
- Accuracy: Each new iteration of LLMs improves in accuracy and the LLM leaderboard changes quite frequently. This implies that the fundamental decision (which LLM to use) needs to be revisited frequently. And we need to maintain the flexibility to change our selection of LLMs for various use cases.
- Trust and Safety: Without clear benchmarks for the trust and safety of LLMs, companies need to build their own guardrails to protect against hallucinations or jailbreaking. Different LLMs require different amounts of efforts of tuning and prompting - to achieve the adequate level of protection. 
- Cost: LLMs differ in their capabilities and corresponding prices. These variations are influenced by factors such as training hours, the volume of training data, and specific model architecture. For example, OpenAI's GPT-4 is 10x more expensive than GPT-3.5, and Anthropic's Claude 3 Opus is 60x the price of Claude 3 Haiku. Similarly, costs associated with open-source models are determined by model size and required GPU capacity to deploy them. Therefore, it is crucial to select a model that aligns with available budget and accuracy needs of the task (e.g. use a cheaper LLM to check for profanity, and a better and more expensive LLM to summarize).
- Latency: The latency of different models can vary from a few seconds to tens of seconds, with larger models offering better capabilities but higher latency. This becomes a key factor for consideration in any conversational use cases (e.g. chatbot), but less so in batch processing cases (e.g. web page translations). 
- Availability: Due to high demand of LLM models and the industry-wide GPU chip shortage, providers are often oversubscribed, leading to rationed quotas for tenants. Securing sufficient capacity for Coinbase’s larger use cases often requires negotiating with AWS/GCP for the appropriate quotas. For customer-facing use cases, careful consideration of latency, user experience, and quality of service in handling high load and burstiness is essential.
CB-GPT, our GenAI platform at Coinbase
We recognized the power of this technology and have built a platform (CB-GPT) that serves as a unified interface for all GenAI-powered applications at Coinbase. The key characteristics of CB-GPT that allow us to solve for the challenges above include:
1. Multi-Cloud, Multi-LLM Architecture
The LLM Leaderboard of best performing LLMs changes frequently, as each of the big players (OpenAI, Google, Anthropic, Meta and others) release new versions of their models every few months. This dynamic state of affairs necessitated our decision to build a multi-cloud multi-LLM architecture, and not get tied in to any one cloud vendor. The current CB-GPT architecture is truly multi-cloud (across AWS Bedrock, GCP VertexAI, Azure GPT and open-source LLMs) with different use cases routed to the appropriate destination.
Additionally, the CB-GPT team is developing / has developed:
- An internal LLM Evaluation Framework to monitor the performance of LLMs across various use cases bespoke to Coinbase and crypto.
- Rate Limiting, Usage Tracking, and Billing Dashboards to closely track costs.
- Semantic Caching to minimize expenses by storing previously asked questions and providing answers without invoking the LLMs.
- Load and Latency Benchmarks for all the LLMs available on the platform.
- A Decision Framework to select the most cost-effective LLMs based on the aforementioned factors.
2. Built-in Retrieval-Augmented Generation
For our enterprise LLM use cases, we extensively use a technique called RAG (Retrieval Augmented Generation) to ensure our responses are anchored in reliable sources of truth. For instance, the Coinbase Chatbot responses are based on our Help Center articles and the same source of truth used by Human Agents to assist customers.
We recognize RAG as a highly effective “grounding” technique and have chosen to integrate multiple data sources to enhance its utility.
- By integrating with an enterprise search and retrieval solution, we have enabled CB-GPT use cases to access a wide range of enterprise data.
- We’ve also enabled Web Search to support use cases that require world knowledge.
- We have also enabled easy use of vector embedding storage and semantic retrieval for other bespoke data sources.
3. Guardrails
One significant challenge of LLM-based applications, particularly in customer-facing scenarios, is ensuring the models' trustworthiness and safety. Due to the ease of interacting with LLMs in English, a vibrant community has emerged, dedicated to testing these models and identifying their flaws. These flaws include:
- Hallucinations, where LLMs generate fictional information.
- Jailbreaking, where LLMs are manipulated into disclosing harmful or inappropriate information.
Publicly available LLMs like ChatGPT and Google Gemini have been known to make mistakes, which often receive media attention.
Therefore, when deploying LLMs for enterprise applications, it is crucial to design a solution architecture with appropriate guardrails. These guardrails should evaluate both input and output information to ensure that the LLM's responses adhere to the 'Three H Principle' (Helpful, Harmless, and Honest).
4. CB-GPT API & Studio
CB-GPT supports a diverse set of technical and non-technical users. By making its features accessible both via an API and a no-code CB-GPT Studio, we allow staff from diverse job functions at Coinbase to build out relevant solutions rapidly. Till date, several dozen use cases have been built by non-ML teams, using CB-GPT.
- CB-GPT Studio is a self-serve no-code tool enabling Coinbase employees to create and maintain AI assistants for bespoke tasks.
- CB-GPT APIs enable engineers across Coinbase to incorporate the power of LLMs in applications that they build.
5. Self-hosting open-source LLMs
Currently, many of our solutions leverage a 3P LLM hosted by one of the major cloud providers (AWS, GCP, or Azure), for which we incur costs with each API call. This approach has been advantageous as it enabled us to quickly adopt the best LLM available in the market.
We are also working with open-source LLMs hosted within the Coinbase infrastructure. Although technically more challenging, it offers several benefits:
- Cost management, as hosting our own LLMs is less expensive than making API calls.
- Ability to fine-tune the LLMs for Coinbase or crypto-specific use cases for higher accuracy.
6. Agentified LLM Solutions
Agentification enhances LLMs to function as autonomous agents by enabling reasoning, planning, and acting independently to perform complex tasks.
- Reasoning: LLMs process information, draw inferences, and make decisions based on data. They understand context, identify relevant information, and apply logic to solve problems or answer questions.
- Planning: LLMs set goals and devise strategies to achieve them by breaking down tasks into manageable steps and determining the best sequence of actions.
- Acting: LLMs execute planned actions, such as writing blog posts, responding to emails, or interacting with other software tools.
Enterprise-grade applications often require LLMs to handle tasks that are too complex for a single model to manage alone. By creating a chain of LLM agents, each specialized in different aspects of the task, enterprises can achieve more efficient and accurate outcomes. For example, one agent might handle data extraction, another might focus on data analysis, and a third might generate reports based on the analyzed data.
Agentified LLMs operate with minimal human intervention, and are ideal for automating repetitive but reasonably complex tasks such as email responses, scheduling, and data entry, freeing up human workers to focus on more strategic activities. Our aim is to simplify the creation of such Agentified solutions for CB-GPT use cases, both through API and Studio.
Conclusion
We are keeping pace with the rapidly evolving field of LLMs, making significant strides in adopting the best solutions for Coinbase employees and customers. At the same time, we've implemented robust safeguards to protect them. We are thrilled by the opportunities ahead and the value CB-GPT brings to Coinbase.
- About Varsha MahadevanSenior Engineering Manager, Machine Learning Varsha Mahadevan is the Senior Engineering Manager leading the CB-GPT team at Coinbase, where she drives the integration of Generative AI into the everyday workflows of employees and customers. Before joining Coinbase, Varsha served as the Associate Vice President of Engineering at BankBazaar.com, a leading fintech company in India. She brings a wealth of experience from her tenure at Microsoft, where she played a pivotal role in developing the .Net Framework and creating AI-driven personalization features for Cortana, Microsoft’s AI assistant.
- About Rajarshi GuptaSenior Director of Engineering, ML Rajarshi Gupta is the Head of Machine Learning at Coinbase, bringing smart automation and protection to crypto users around the world. Prior to this, Rajarshi was GM, ML Services at AWS. He also worked for many years at Qualcomm Research, where he created ‘Smart Protect’, the first ever product to achieve On-Device Machine Learning for Security and shipped in over 1 billion Snapdragon chipsets. Rajarshi has a PhD in EECS from UC Berkeley and has built a unique expertise at the intersection of Artificial Intelligence and Blockchains. Rajarshi is a prolific inventor and has authored 225+ issued U.S. Patents.
