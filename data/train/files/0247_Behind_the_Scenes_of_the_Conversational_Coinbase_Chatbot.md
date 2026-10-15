# Behind the Scenes of the Conversational Coinbase Chatbot

Источник: https://www.coinbase.com/en-ar/blog/behind-the-scenes-of-the-conversational-coinbase-chatbot

Behind the Scenes of the Conversational Coinbase Chatbot
TL;DR: Coinbase is using GenAI to handle tens of thousands of customer support queries every month. The Conversational Coinbase Chatbot (CBCB) delivers context-aware responses by integrating knowledge bases, real-time account information, and domain-specific rules.
The Challenge: Scaling Customer Support with LLMs
As Coinbase continues to expand, the volume of customer queries has surged to tens of thousands each month. The traffic patterns tend to scale in spurts, especially during events like crypto bull runs.
These customer queries often cover a variety of topics like account restrictions, platform policies, recent transactions, and unique Coinbase product features. Addressing these issues effectively in an automated manner demands a system that not only understands the intricacies of Coinbase's ecosystem but also generates personalized responses based on user data while adhering to our privacy and compliance requirements.
To meet these challenges and reduce the reliance on human intervention, we developed the LLM-powered Conversational Coinbase Chatbot (CBCB).
Several key factors motivated this initiative, offering significant benefits to both our customers and Coinbase.
- Our goal was to expand the range of queries the bot could handle while enhancing the quality of responses, enabling customers to get faster answers without needing to wait for a live agent.
- By refining the bot's conversational capabilities, we aimed to minimize the "back-and-forth" interactions, delivering a smoother and more efficient user experience.
- Finally, automating routine inquiries allows our customer experience (CX) agents to focus on more complex and impactful issues, where their expertise can have the greatest effect.
Building CBCB
Standard LLMs, whether commercial or open-source, lack the necessary context for Coinbase-specific needs. That is why the CBCB employs a multi-stage architecture that processes each query through prioritized stages, enabling dynamic access to the right data and logic required for the query. This architecture leverages knowledge bases, such as Help Center articles, and various real-time APIs that reflect actual account status and transactions history of the customer. For example, CBCB might first analyze account-specific restrictions before deciding whether to fetch product-specific guidance, or resolve the user's query through domain-specific logic tailored to particular issues. By processing user queries sequentially through each relevant stage, the system delivers personalized, accurate, and compliant responses.
From Query to Response: CBCB’s Intelligent Pipeline
CBCB is more than just an LLM — it is an orchestrated system involving multiple LLM tasks and knowledge retrieval operations and other decision-making steps.
- Rephraser: Refines customer queries to better match our knowledge base, ensuring accurate interpretation by the chatbot.
- Article Retriever: Bases responses on relevant help content by dynamically retrieving information from knowledge bases using multiple semantic indices for improved accuracy. Ranks the retrieved articles for optimal relevance to the user's query using an additional ML model.
- Response Styler: Guarantees that responses meet conversational standards, including appropriate tone, clarity, and style.
- Guardrails: Ensures compliance with legal, security, and privacy standards by enforcing strict input and output protocols.
Challenges of Building User-Facing LLM Applications
Developing CBCB required addressing a set of unique challenges:
- Accuracy & Hallucinations: Ensuring that responses are based on accurate, Coinbase-specific information, while trying to avoid any misleading or fabricated answers.
- Guardrails & Compliance: Stringent controls are in place to filter and shape both input and output, ensuring they are safe, relevant, and compliant.
- Scaling & Quotas: CBCB must handle a high volume of concurrent queries, making scalability a priority. To manage demand effectively, CBCB employs a multi-cloud and multi-LLM strategy to distribute the load and reduce the risk of throttling.
- Controllability & Explainability: Maintaining predictable and explainable chatbot behavior is crucial. CBCB’s layered architecture and modular design facilitate transparent, traceable decision-making, simplifying debugging and iterative improvements.
- Evaluation: We use a variety of evaluation methods, including curated test sets for different pipeline stages, live A/B testing to assess real-world user impact, automated LLM-based evaluations, manual reviews, and continuous performance monitoring across key metrics.
Conclusion
Coinbase’s CBCB chatbot was built to handle the growing scale and complexity of customer support. Using advanced LLMs, real-time account data, product-specific knowledge, and a comprehensive evaluation process, CBCB provides precise and compliant responses to incoming user queries. As CBCB evolves, it will further enhance its ability to manage more nuanced user queries, improving the support experience and addressing all stages of the user journey within the Coinbase ecosystem.
Stay tuned for more technical insights on how we're leveraging AI and machine learning to improve the more Coinbase experiences.
