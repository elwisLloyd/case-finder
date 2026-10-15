# (Part 2) From RAG to Agents : Doctolib’s journey to revolutionize Customer Care

Источник: https://medium.com/doctolib/part-2-from-rag-to-agents-doctolibs-journey-to-revolutionize-customer-care-6b14da40f5ae

(Part 2) From RAG to Agents : Doctolib’s journey to revolutionize Customer Care
Before diving into the advanced aspects of implementing an agentic architecture for Retrieval-Augmented Generation (RAG) applications, it is crucial to first understand the RAG foundations laid out in Part 1 of the series. If you haven’t read it yet, I strongly recommend starting here.
With the use of LLMs, we continued improving our customer care services by implementing a RAG. Due to some limits, we decided to research more powerful solutions, such as Agentic frameworks. We will discuss them in this article.
Agentic systems use AI agents to add a layer of intelligence by using LLM-based agents. The agents act as decision makers, analyzing input findings and selecting the most effective tools or other agents for the task. This multi-step reasoning capability enables more complex tasks like formulating follow-up questions, comparing documents, fetching data, making API calls or routing to other agents.
Agents are Natural Language systems capable of autonomously performing tasks
- It runs in a LLM
- It has a clear role, description, and context defined by a prompt
- It can have access to tools used to run specific tasks such as retrieving data, fetching data, reading a document, changing data in a database (running a function) or calling an API. Tools will be defined as functions.
An AI Agent is needed when we use reasoning to decide which actions to take and in what order. This is the main difference from a BOT system, which is hard-coded on what to do next. Here, the LLMs decide what to do and in what sequence. Essentially, we use agents, not a LLM, to perform tasks. They require planning, multi-step reasoning, and tool use.
Powered by powerful yet still evolving frameworks
To implement this new architecture, we explored several new frameworks (crew.ai, autogen, LangGraph). They are evolving rapidly, with very few examples of their use in production.
After a comparison, we chose LangGraph (reasons below), which is a powerful multi-agent framework for building stateful, multi-actor applications with LLMs, built on top of LangChain.
It best suits our use case. It offers the most flexibility to develop, while providing some security guardrails (sensitive tools) and simplicity to implement user interaction. The documentation was also the clearest Also, the easy integration with the LangChain ecosystem was a plus. It sped up code development.
LangGraph models all interactions as cyclical graphs. A graph is made of nodes and branches
- Each node is a computation/processing step, which can be an LLM based agent or a deterministic function
- Those agents interact with other specialized agents and / or human users (along branches) in Natural Language.
These graphs enable the development of advanced workflows and interactions with multiple loops and if-statements, making it a handy tool for creating both agent and multi-agent workflows.
Here is where things get really interesting. In agentic architecture, we’ve got multi-agent orchestration. Imagine having multiple specialized agents, each being an expert in their own domain or data source, collaborating and synthesizing their findings to provide you with a comprehensive response. It’s like having a team of experts working together to solve your toughest problems. It eases the pressure on having one agent do everything and enables better agents because they are specialized. It is very powerful.
Orchestrated together around specialities and tools
Our goal was to create an architecture as robust as possible to hallucinations and answer/tool choice variance, but also developing the most generalizable and scalable structure for our use case but also be used for other projects.
To do so, the agentic framework is built on two types of LLM agents:
- A primary assistant (or root assistant), an LLM responsible for greeting and routing the user to the correct specialized assistant
- Several specialized assistants, with each specialized assistant is meant to handle requests over a fixed scope (one or two use cases). We created those specialized agents to reduce the pressure on them, by limiting their scope, prompt size and number of tools associated.
The root assistant goals are :
- Interacting with the user until a clear query is mentioned regarding Doctolib
- Routing the user query to the correct specialized assistant (currently based on a ML classification model)
Every specialized assistant will share the following foundations:
- A tool allowing to fetch data on the user or its query context, instantiated with the documentation of the APIs that will be developed to access the relevant data resources of the Doctolib databases in the context of the user question
- A list of Execution Tools, eg:
- A FAQ search tool, which is actually the RAG described in the first paragraph
- Tools, classified as sensitive (asking for user validation), to automate the Customer Support back-end actions that are required to solve the use cases associated with the scope of the specialized assistant.
The sensitive tool is instantiated with applicative APIs documentationIt has a fact check step as a safety net, to make sure that the arguments of the tool are properly filled by the specialized assistant
- A tool indicating that the task is complete or canceled to loop back to the root assistant
- If the practitioner request is fulfilled
- If the practitioner canceled the request
This architecture enabled us to tackle a first use case that you can see in the demo above. We can see a conversation between the agentic system and the user. The user wants to give his secretary access to his agenda. The query is correctly rooted to the right specialized agent related to agenda rights issues. The agent then asks about the user’s name and the agenda. This gets the needed input. Then, it uses a tool to fetch more context data. Before giving his secretary access, the arguments are checked and we ask for user validation to execute the action on its behalf.
We had to address specific constraints
This is very promising and shows us all the powerful benefits it can offer, but we still faced some challenges with this framework to make it robust and reliable.
Agent behavior variance
One of the main issue we faced is related to the non-deterministic aspect of LLM models leading to agents not to behave consistently:
- It does not always invoke the correct tool at the right moment
- It does not always execute tools with the proper specified parameters
This is extremely problematic because the LLM agent behavior cannot be anticipated. This was especially true when the prompt of the LLM became extremely large. Reducing the task expected from a LLM and limiting its degree of freedom can mitigate this variance.
LLM Prompt size
To use an agentic architecture, we must feed all the relevant information about the agent (tools description and execution, stack of messages…) through the prompt of the LLM. This leads to very large prompts. The Positional Attention Bias problem in LLMs states that the more information the LLM gets in the prompt, the less likely the LLM will follow our guidelines.
Unstructured data
Also, to enrich the context around a user question, the agent should extract useful information and make sense of unstructured data in order to ask relevant questions. This is very hard for a model, especially in a consistent way.
Get Anouk Barnoud’s stories in your inbox
Join Medium for free to get updates from this writer.
So, even if this system works well, those limitations show us that it can be improved via labeling more data for the LLMs. Indeed, providing labeled data to better guide the agents will reduce the complexity of the tasks the agentic systems face and improve the reproducibility of the results.
It looks like it will revolutionize the way we develop products and actually code them
A generic layer to deal with the user intent and translate into an actionable applicative intent
That being said, it represents an incredible opportunity, for our project but also for many other use cases. Indeed, by using LLMs it adds a modal layer of Natural Language helping to understand and interpret human language effectively. This enables the system to better comprehend the user’s intentions and requests, leading to more accurate and contextually relevant responses.
Moreover, the agentic capabilities play a crucial role in bridging the gap between natural language understanding and the system’s ability to take action. It translates the user’s intent into a format that the system can comprehend and execute with the goal to minimize hallucinations. This allows for seamless communication between the user and the system.
It also provides a last layer : the Applicative Intent layer. By utilizing the translated intent to perform specific actions or provide relevant information, it enables the system to understand the purpose behind the user’s requests and respond accordingly , whether it is executing a command, retrieving data, or providing recommendations.
By combining these three layers, the agentic RAG architecture offers a comprehensive and efficient solution for natural language interaction. It has the potential to revolutionize various domains, such as virtual assistants, chatbots, customer support systems, and more. The promise lies in its ability to deliver a smooth and meaningful user experience by accurately understanding user intent and providing relevant and actionable responses.
The quality of the documentation of the applicative world and the functional data structuration will define the performances of our system
Functional data structuration
The effectiveness of agentic RAG agents hinges on the accuracy, completeness, and relevance of the data they use. Poor data quality can lead to unreliable outputs, making robust data management and quality assurance essential.
Thus, in order to better guide the specialized assistant on what data to check before calling the correct tool and which questions to ask the practitioner, we need to create a very clear and exhaustive data referential for all the different scopes/categories we want our system to be able to handle.
We define generic agents and this referential will define the specialized assistant by specifying
- Its prompt
- The user information passed as a context to the specialized assistant. This requires a detailed description in natural language of how the task to perform translates into code (essentially the documentation of the interface contracts of product APIs)
- The definition of the tool to carry out the actions required to solve the user issue, which requires a functional description in natural language of the tasks to perform.
- The tables available for further context enriching, requiring a strong data governance on key data assets
The goal is to create a structured dataset breaking down the user queries into big use cases or user scenarios with specific context data, instructions and definitions in a way that guides the LLM through a series of small, manageable tasks. This requires data governance to ensure that the dataset is always up-to-date and to harmonize semantics of analytic data to define all the key concepts.
This approach reduces the scope and ambiguity, reducing the risk of hallucination or deviation from the expected path, but it also enables the creation of a scalable system.
Documentation of the applicative world
To execute actions on behalf of the user, we will need the tech teams to create the connectors to the APIs that perform actions. The documentation of the APIs will be needed to create the right tools for our agents, all the relevant arguments with the correct type and description. As such, the quality of our system also depends directly on the quality of code, which can now be treated as a valuable source of information for our system. It creates a new paradigm for the developers as it is not only about writing functional and clean code but also about the quality of the code and documentation. The goal is to use the OpenAPI specifications of all the APIs to directly feed our system.
But we are still iterating to address challenges ahead
Even if it represents an opportunity full of promise that we hope could be a generic brick that we could plug before managing any user intent, we still have many challenges ahead of us to make this a real AI product, reliable and scalable. Indeed,
- The evaluation part of the system is a critical aspect, yet very complex as the system is composed of many bricks that need to be evaluated separately to understand the performance bottlenecks. Frameworks such as Literal or Langsmith can help us understand error root causes of our system.
- Making this a real AI product requires being able to deploy the framework in production, which entails many challenges. Indeed, we need a strong collaboration and synchronisation with the different teams involved (design, feature teams, PM, ML Platform…). We have strong dependencies to test our system and deploy it. Plus, LangGaph is a new and moving library. It does not provide many real use cases that went into production. Also, we need to achieve a very strong robustness level of our system to be confident to deploy it in production.
- Making this a scalable tool requires a smart design system with a good synchronisation between teams, as well as excellent data structuration and documentation. We need to develop real data assets that are correctly governed and maintained, which need organizational change in the whole company.
Contacts and thanks
Many thanks to the incredible team that worked on the project and developed the POC : Vincent Cornet Louis Melliorat Julien Richard Sinda SALEM
Don’t hesitate to contact us if you have any question :
- Anouk Barnoud : anouk.barnoud@doctolib.com
- Sinda SALEM : sinda.salem@doctolib.com
- Vincent Cornet : vincent.cornet@doctolib.com
- Julien Richard : julien.richard@doctolib.com
- Louis Melliorat: louis.melliorat.pro@gmail.com
