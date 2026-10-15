# Building Agoda’s Property Bot: How We Cut Response Time from 8 Hours to Seconds

Источник: https://medium.com/agoda-engineering/how-we-built-agodas-property-ama-bot-to-simplify-travel-decisions-b861c7ec7ff1

Featured
Building Agoda’s Property Bot: How We Cut Response Time from 8 Hours to Seconds
At Agoda, we strive to provide our users with all the information they need to make confident booking decisions. Our property pages provide a wealth of details about accommodations, but for many users, pinpointing specific answers can be a challenge. Common questions such as, “Does this hotel offer free breakfast?” or “Is there a bar in the hotel?” often require users to sift through long pages of information.
While the Agoda Customer Messaging platform allows users to ask properties directly, it often falls short: many inquiries remain unanswered, and responses often take an average of eight hours. This delay makes it difficult for users to get the timely information they need to decide which property best suits their needs.
Statistics show that 80% of properties allow an inbox messaging feature. But only 55% of questions actually receive a response from properties.
We recognized the need for a faster, more reliable solution to address these challenges and enhance the user experience.
Introducing the Property AMA Bot
To solve this issue, we developed the Property AMA (Ask Me Anything) Bot, our first AI chatbot that provides instant and accurate answers to property-related questions. The bot is designed to enhance accessibility and eliminate delays, allowing users to make quicker and better-informed decisions.
In this blog, we will share how we tackled these challenges, the technology behind the Property AMA Bot, and how it’s helping transform users’ interactions with property information.
How the Property AMA Bot Works
The Property AMA Bot is designed to simplify the way users access property-related information. Instead of searching through detailed property descriptions or waiting hours for a response from a property, users can now ask the bot directly and receive an instant reply.
The bot ensures users have access to property-specific information in seconds, making the decision-making process easier and more reliable. Additionally, the chatbot is accessible across platforms, including desktop, mobile web, and the Agoda app, ensuring a seamless experience wherever users interact with Agoda.
Technical Architecture of the Property AMA Chatbot
Property AMA Chatbot is a sophisticated system that leverages modern AI capabilities to provide insightful and accurate responses to users’ property-related inquiries. Here’s a detailed look into its architecture:
1. Chatbot Client (AIDE)
The chatbot client acts as the front-facing component, interacting directly with users. It is designed to interpret user queries and connect seamlessly with a bot, ensuring a smooth conversational experience.
The project is built as an NPM package library and micro-frontend (MFE) to enable easy reuse and seamless integration, allowing it to be rendered and utilized across websites and different repositories for desktop and mobile web view.
2. LLM API
At the core of our system is the (Large Language Model) LLM API, which facilitates communication between the chatbot client, Agoda ecosystems and advanced language model, ChatGPT. When a user poses a question, the chatbot client passes this request to LLM API. The API acts as a conduit, ensuring the question is parsed and relayed efficiently to ChatGPT for processing with context that is fetched from Agoda services. For property-AMA, we connect to Property API (PAPI) to fetch property information that enriches the chatbot’s knowledge base. This integration ensures that when users inquire about properties, the information they receive is comprehensive and current.
3. Prompt Engineering
ChatGPT + Utilizing In-Context Learning
Prompt engineering is key to making the P-AMA chatbot work effectively. It involves creating prompts that guide the chatbot’s responses for a smooth user experience. Here are the main components:
- Role and Reference: Knowing the chatbot’s role and context.
- Knowledge Base: Using available information effectively.
- Actions: Defining what actions to take based on prompts.
- Out-of-Scope Queries: Managing questions outside the chatbot’s scope.
- Do Not Disclose System Information: Keeping sensitive information secure.
- Instructions Adherence: Following instructions accurately.
- Unsupported Questions: Handling questions that can’t be answered.
- Response Guidelines: Crafting consistent responses.
- No External Referrals: Avoiding references to outside sources.
And a standout feature is in-context learning. The chatbot fetches relevant property data from Property API, enhancing responses with specific details. This ensures answers are accurate and contextually informed. By leveraging this architecture, the chatbot effectively merges AI language processing with contextual learning from Agoda property information. This combination results in precise and personalized responses to user queries, illustrating how advanced technology can be utilized to improve user interaction and help users make better decisions to book Agoda property.
Challenges
Our Property AMA bot should answer on behalf of Agoda. We want this bot to act like a professional customer service chatbot.
Get Agoda Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
There are several cases we need to address:
- Customers asking questions unrelated to the property
- Customers asking questions the bot can’t answer
- The bot attempting to answer with information we haven’t provided
To handle these situations, we’ve implemented an additional prompt called the “input topic guardrail.”
How does it work?
On the API side, we execute two prompts:
- Input topic guardrail — to check if the user’s question is allowed based on our provided topic list.
- Answer queries — the bot answers questions based on the property data we provide as context to OpenAI.
This ensures that if a user asks something not allowed, the bot will not provide an answer.
How do we ensure chatbot answers well? Our data science plays a key role in evaluating the question-and-answer data that will be explained in the next section.
Chatbot Evaluation
How effectively a prompt or AI model generates desired outputs can be evaluated using a systematic method called response labeling. This approach involves organizing the AI-generated responses into clear categories based on their relevance and accuracy in addressing the given queries.
The responses are classified into four distinct labels:
By applying these labels to chatbot interactions, we gain valuable insights that enable developers to refine prompts, adjust data inputs, and optimize algorithms, ultimately improving the chatbot’s accuracy and reliability.
After multiple iterations and refinements, these are the current statistics.
Another method we use is A/B testing, which allows us to compare different prompts or models to identify the most effective approach. By integrating the chatbot with our in-house experimentation platform, we can measure key metrics such as bookings, user engagement, and other business-critical outcomes to evaluate the success or failure of each prompt.
Future Expansion with AI Agents
While the Property AMA Bot currently focuses on property-related queries, we are already envisioning its next evolution. Our roadmap includes the introduction of AI Agents to expand its capabilities beyond property questions.
1. Expanding Capabilities with AI Agents
We are innovating our system with the introduction of a ManagerAgent, a pivotal component that will enable our platform to execute multiple tasks beyond its current scope. The ManagerAgent will orchestrate the subdivision of projects into manageable tasks, each assigned to specialized agents designed to tackle specific challenges.
2. Beyond the Property AMA Bot
This futuristic expansion transcends the current Property AMA Bot. By deploying AI Agents, we will be able to gather, analyze, and act upon data from a variety of Agoda products, including bookings, flights, activities, and more. Each agent will collaborate, sharing insights and strategies, to efficiently execute their individual missions.
3. Plug-and-Play Flexibility
Our AI Agent system is designed like building blocks, so different agents can be easily added or swapped. This makes it easy for us to adjust to new challenges and take advantage of opportunities, keeping our service adaptive and effective. Using AI Agents, we’re preparing for a big change in how artificial intelligence helps us operate. This advancement will not only expand what we can offer but also provide our users with better and more insightful experiences.
Conclusion
The Property AMA Bot represents a transformative step in how we help users access information quickly and make confident booking decisions. As we refine the bot and expand its capabilities, we’re excited about the opportunities to further enhance user experiences and shape the future of AI-driven travel solutions.
