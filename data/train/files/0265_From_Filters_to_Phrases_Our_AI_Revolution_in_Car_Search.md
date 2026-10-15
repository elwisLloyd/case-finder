# From Filters to Phrases: Our AI Revolution in Car Search

Источник: https://medium.com/adevinta-tech-blog/from-filters-to-phrases-our-ai-revolution-in-car-search-2d7c73ca4886

From Filters to Phrases: Our AI Revolution in Car Search
By David Manzano, Engineering Mind and Mauro Ferrantelli, Product Manager and AI Enthusiast
Introduction
As the first light of dawn broke over Barcelona, our team huddled together to kick off a bold new initiative. We are the minds behind the search experience at coches.net, Spain’s leading vehicle marketplace. Excitement mixed with nervous energy filled the room as we embarked on a mission: to revolutionise our car search functionality with the power of artificial intelligence. We began the project in secret, and gave ourselves just 15 days to bring this vision to life.
The Spark of Innovation
It started with a simple observation. We noticed a colleague struggling with our existing search system, applying multiple filters just to find a specific car model. It became clear that there must be a more efficient way to search our site. Our users deserved the convenience of typing natural phrases and getting accurate results.
Our car search system faced several challenges:
- Complexity: Users wanted to search using natural language like “Audi A3 2020 in Barcelona” but had to navigate through several filters instead.
- User Experience: The system wasn’t intuitive, requiring users to know which specific filters to apply, such as “environmental stickers needed in Madrid”.
Discovering the AI Solution
While experimenting with Amazon Bedrock for another project, we realised its potential for natural language processing. We developed a proof of concept and shared it with the development team. The results were promising, and we agreed that implementing this feature could significantly improve the user experience.
Our goal was to enable searches like “family-friendly SUV for mountain trips” or “sporty convertible under €30,000 in Madrid,” making the search process more intuitive.
The 15-Day Challenge
We set a self-imposed deadline of 15 days for this sprint to develop the AI-powered search. Wanting to avoid spending too much time on an unapproved initiative, we took a slightly unconventional approach. We dedicated all of our efforts to bringing this feature to life without attracting attention until we were sure it would work.
We worked diligently, refining the system and testing its capabilities. Our approach was collaborative and focused to ensure we stayed aligned with our objectives.
Technical Approach
We used AI to translate natural language queries into our existing search filters. The AI doesn’t perform the search itself; it converts the user’s input into filter parameters that our system can process.
Here is a simple flow chart with the steps of the search process.
As you can see, the user’s query is first moderated to ensure it’s appropriate and relevant to car search. If it meets the criteria, we instruct the AI model to translate the query into our filters. We provided the AI with context about our filters and examples to enhance accuracy.
After verifying the AI’s response, we send the filters to the Frontend, where the website applies them to perform the search.
Moderation
It’s necessary to moderate user questions, as we should not and cannot answer questions that are not ethic, nor questions that have nothing to do with car searches.
Imagine that the user suggests looking for a car to carry out an illegal activity; we should not pass this query to our search filters. That is why we will moderate all messages before forwarding the question to the AI. Also, this pre-filtering action is quite cheap (in processing terms) and saves us from including the whole context of coches.net.
How do we do it? We simply send the user’s question to the AI model and ask it to return the following codes in its response:
- 0: if the question is valid
- 1: if the question is unethical
- 2: if the question is invalid
AI Engine Selection
We chose Amazon Bedrock’s generative AI service, aligning with our AWS infrastructure. Specifically, we used Anthropic’s Claude model, opting for the Haiku version due to its balance of speed and cost-effectiveness.
Prompt Engineering
We employed the Few-shot prompting technique, supplying the AI with context about our filters and examples of searches. This approach helps the AI generate accurate and relevant responses.
Cost Considerations
In AI processing, “tokens” represent units of text that the AI reads and generates. Each token consumes computational resources, affecting latency and cost.
Get Adevinta’s stories in your inbox
Join Medium for free to get updates from this writer.
Our AI search generates approximately 6,000 input tokens and 500 output tokens per query. Using the Haiku model:
- Price per 1,000 input tokens: \$0.00025
- Price per 1,000 output tokens: \$0.00125
With our current traffic on coches.net:
- Around 20,000 model invocations per day
- 55 million input tokens
- 4 million output tokens
This results in a cost of about €19 per day, which is a reasonable value for the improved user experience.
The Unveiling
As we concluded our sprint, we prepared to demonstrate the new feature to our stakeholders. The product demo showcased the AI-powered search bar’s capabilities, handling complex queries efficiently. The response was positive, and we were encouraged by the potential benefits for our users.
The Impact
Implementing AI in our car search system yielded notable improvements:
- Enhanced Efficiency: Users utilising the AI search generated more value compared to traditional methods.
- Improved User Experience: The AI search applies necessary filters automatically, including specific requirements like environmental stickers in Madrid.
Feedback from users has been encouraging. One user mentioned:
“I typed ‘eco-friendly family car for city living,’ and it provided suitable options, considering Madrid’s environmental sticker requirements. It made finding my ideal car much easier!”
However, we recognise that adoption is still limited. A small portion of our traffic uses filters, and fewer are leveraging the new AI-powered search. We are working to improve the user experience and encourage more users to try this feature.
Lessons Learned
Our experience taught us several valuable lessons:
- Importance of Data: Quality and quantity of data significantly impact AI performance.
- Team Collaboration: A focused and dedicated team can achieve meaningful results in a short time.
- Continuous Improvement: Iterative development is essential. We need to refine the feature based on user feedback and evolving requirements.
Looking Ahead
We plan to continue enhancing our new AI search function, making it more intuitive and accessible. Our filters are evolving, and we aim to improve usability to increase adoption and impact on our users and metrics.We encourage others in the tech community to share their experiences and insights. If you have questions or feedback, please reach out. Your input is valuable as we refine and develop this technology further.Implementing AI in our car search tool has improved our system and user experience. This project reinforces our commitment to innovation and continuous improvement.
Thank you to all the contributions of our team:
