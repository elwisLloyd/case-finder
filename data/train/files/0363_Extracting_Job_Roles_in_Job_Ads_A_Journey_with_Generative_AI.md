# Extracting Job Roles in Job Ads: A Journey with Generative AI

Источник: https://tech.olx.com/extracting-job-roles-in-job-ads-a-journey-with-generative-ai-e8b8cf399659

In the dynamic landscape of job listings, we faced a significant challenge — the lack of clearly defined job roles within our jobs taxonomies. This resulted in job roles being buried within the titles and descriptions of job ads, creating a barrier to an efficient and organized search experience. Recognizing the importance of providing job seekers with a seamless and accurate search process, we set out to revolutionize our approach.
What will you learn?
This blog post unveils the journey we undertook at OLX to address this challenge, leveraging the power of Prosus AI Assistant, our generative AI (GenAI) model, specifically a Large Language Model (LLM), designed to understand and generate human-like text based on its given input.
The heart of the matter was the need for a more organized and accessible system of job roles within our taxonomies. For job-seekers seeking specific professions, this initiative aimed to significantly enhance the search experience by ensuring a closer alignment between their desired jobs and the relevant ads.
As you read through this post, expect to gain insights into the practical application of GenAI and LLM in a production environment. We'll explore the details of our Proof of Concept (PoC), showcasing how Prosus AI Assistant emerged as a powerful tool to refine our job taxonomy.
Job taxonomy refers to the systematic classification and organization of job roles within a hierarchical structure, facilitating efficient categorization for improved search and user experience.
Join us on this journey of improving search accuracy and user experience in job listings.
Prosus AI Assistant: A Key Player at Every Stage 🤖
Introducing Prosus AI Assistant — our versatile AI solution developed by Prosus, a global consumer internet group and technology investor. Like the well-known GPT models, Prosus AI Assistant is a generative AI (GenAI) and a Large Language Model (LLM) that excels in understanding and generating human-like text. This AI is far more than just a tool; it functions as a valuable addition to our workflow, seamlessly integrated into Slack. With its wide range of capabilities, including transcribing audio and video, handling text files, generating images with AI, and applying OCR to understand the contents of PDF and image files, the Prosus AI Assistant is adept at assisting with technical questions and tasks such as compiling reports or tweaking code. In July 2023, Prosus provided us with an API, granting us the freedom to explore and innovate, leveraging the power of AI to enhance our day-to-day operations.
Prosus AI Assistant vs Self-Hosted LLMs: A Strategic Decision 🧠
In the deliberation of language models, the selection of Prosus AI Assistant was driven by its proven accuracy, cost-efficiency, and, notably, the advantage of swift time-to-market.
Accuracy was informally monitored during the annotation process, specifically extracting job roles from descriptions. An initial examination of 100 samples revealed a notably low incidence of flaws. This task aligns seamlessly with GenAI's proficiency, given the predominant focus of the job ad description on job requests.
The term ‘cost-efficiency’ is subjective and context-dependent. Depending on the problem we aim to solve, the use-case specifics, and the volume of requests, Prosus AI Assistant may emerge as a superior choice compared to a self-hosted LLM. The latter demands more time for fine-tuning and necessitates proper infrastructure with associated costs. We will delve deeper into how these considerations influenced our project in the upcoming ‘Cost Reflection and Future Pathways’ section.
Moreover, Prosus has a special agreement with OpenAI, ensuring that our data is handled with extra care and enhancing privacy and security measures. Notably, we follow a zero-day data retention policy, prioritizing the confidentiality and security of user information.
As for the potential risks, one may inquire about slightly longer response times, dependence on external API reliance, and the long-term viability of using Prosus AI Assistant as an enduring solution. However, every superhero has its quirks, right?
It's worth highlighting that while we currently leverage the Prosus AI Assistant, we remain open to exploring custom LLMs to optimize costs and further refine our language processing capabilities. The decision to choose Prosus AI Assistant was strategic, focusing on rapid deployment for immediate benefits and acknowledging the potential for future enhancements.
The High-Level Implementation 🚧
Now, let's go through the high-level implementation of our job-role extraction pipeline. Explore how Prosus AI Assistant plays a crucial role at each step, enhancing job taxonomy and ensuring accurate search results.
Job-Role Extraction Pipeline: From Concept to Reality
Job-role extraction is the process of systematically identifying and isolating specific job roles or professions from unstructured data, such as job ad titles and descriptions.
Our journey from concept to reality involved meticulous steps — sampling data, preprocessing, and unleashing Prosus AI Assistant's magic to extract job roles.
Data Sampling and Preprocessing
In our quest for job-role extraction excellence, we carefully sampled 2,000 job ads. To ensure accuracy, we accounted for the uneven distribution across sub-categories. Our preprocessing dance included meticulous text cleaning, trimming to the first 200 words/tokens, and a touch of translation magic. The result?
A pristine dataset ready for Prosus AI Assistant to work its job-role-extracting wonders!
Search Keyword Analysis: Unveiling Job-Seeker Preferences
Beyond just job extraction, we've delved into the minds of job-seekers! While focusing on job roles, we've simultaneously dissected the most searched keywords in the Jobs categories. Using Prosus AI Assistant, we've categorized keywords into professions, job types, locations, and broader descriptors. Astonishingly, 60% of these keywords focus on specific professions, guiding us to tailor our platform for users searching for precise opportunities.
Job-Role Taxonomy Tree
To establish a normalized job-role taxonomy, our approach involved leveraging up to the top 100 profession-related searched keywords and up to 50 job roles extracted from randomly selected job ads within the specified category. The process was guided by a well-defined prompt, resulting in a hierarchical taxonomy. This taxonomy served as a foundational structure for subsequent steps.
Here is an overview of the corresponding prompt:
### Task Description ###
Consider the following top-searched keywords and job-roles in the {category} category in an online Job platform. your task is to categorize them into normalized job-roles considering both responsibilities and department.
- <list of detailed instructions>
### Expected Output Formatt ###
<specify the proper output format>
- keywords:
{search_keywords}
- roles:
{job_roles}
Output: ?
Here is a translated example of the job-role taxonomy for the "Agricultural and Gardening Category" in Jobs.
It's worth noting that we focused on the Polish market for our POC, considering its prominence as one of the largest markets in OLX. The following taxonomy represents a translation from Polish to English:
Job-Role Extraction with Prosus AI Assistant
With a comprehensive taxonomy in place, we moved on to extracting job roles from actual job ads. This process required specific information, including the ad content (title and description) and the associated category. A dedicated prompt facilitated the identification of relevant job roles within the established taxonomy tree.
This intricate production pipeline is a testament to the power and practicality of Prosus AI Assistant in enabling the transformation of our conceptual ideas into a functioning system.
Journey to Production: Overcoming Challenges 🚀
Bringing a solution to life has its challenges. From backfilling existing ads to continuous extraction for new ones, Prosus AI Assistant is seamlessly integrated into our pipeline.
Productionizing the Job-Role Extraction Pipeline
Taking our project from proof of concept to practical implementation required careful consideration of production steps. This involved:
- Backfilling Existing Ads: A comprehensive backfill operation on all existing ads to extract and store job roles retrospectively.
- Continuous Job-Roles Extraction for New and Updated Ads: Ensuring a constant extraction of job roles for all new and updated job ads to maintain an up-to-date job-role database.
The pipeline was smoothly integrated into our existing infrastructure. A new service subscribed to ad events utilized Prosus AI Assistant to extract job taxonomy information and sent job roles to the Kinesis platform used by our Search team.
Resource Utilization in Production
Get Mahnaz Namazi’s stories in your inbox
Join Medium for free to get updates from this writer.
In the production phase, our process adapts to the dynamic job landscape with around two thousand daily newly created or updated ads. Focusing on efficiency, we break down the task into two sub-tasks — job-role extraction and matching within the standardized tree — resulting in approximately four thousand daily requests to the Prosus AI Assistant API. This streamlined approach ensures responsiveness and adaptability in maintaining an effective job-role extraction pipeline.
Challenge: Navigating Category Evolution
Our job-role extraction pipeline needs to keep pace with the changing nature of Job categories. As our team consistently improves categories, changes are bound to happen. Here's how we handle these changes:
Implications:
- Job-Roles Recreation: Changes to sub-categories within the jobs category may necessitate the recreation of job-role taxonomies.
- Consistency Concerns: Evolving categories might introduce disparities between job-role taxonomies created before and after the change in a specific sub-category.
Our Future Strategy:
We're working on implementing an automated process that senses changes in sub-categories and swiftly adapts by regenerating the necessary job-role taxonomies. This proactive approach ensures our extraction model seamlessly aligns with the ever-evolving job landscape.
Resource Utilization:
In the process of generating job-role trees, the API requests can be estimated as follows:
These estimates are based on a single pipeline run, and we need to trigger the pipeline only when there is a change or update in our category tree. This update frequency is expected to be no more than a few times per month.
Tips for Effective Prompt Engineering 🎨
Crafting prompts is an art that shapes the dance between humans and language models. Here are concise tips from our job-role extraction journey:
- Be Specific and Clear: Precision is king. Clearly define tasks to ensure the AI grasps nuances. Avoid ambiguity for accurate results.
- Iterate and Experiment: Prompt crafting is a journey. Experiment with phrasings, structures, and lengths. Test, refine, and embrace the iterative process.
- Leverage Context: Provide context. Including job ad titles and descriptions significantly boosts Prosus AI Assistant's accuracy. Context matters!
- Address Token Limits: Navigate token limitations strategically. Break down complex tasks, trim ad descriptions, and optimize for effective communication.
- Balance Specificity and Flexibility: Find the sweet spot. Craft prompts specific to tasks yet flexible enough to handle variations. Embrace the diverse job landscape.
- Simplify with LangChain Framework: Streamline Prosus AI Assistant interactions using the LangChain framework. Simplify outcome specifications and seamlessly chain tasks for enhanced efficiency.
Cheers to a well-prompted journey! 🌟
Initial Results and Future Prospects📈
The moment of truth — what were the initial results?
We'll present our findings and share how implementing standardized job roles affected search results and user interactions.
Did our hypothesis hold? Dive into the data and discover the real-world impact of our solution.
Estimating Impact: The Art of Patience
In our quest to elevate the job search experience, we've launched a job-role extraction pipeline, focusing on the retrieval stage of search. As we estimate the impact, here's the inside scoop:
- Experimental Horizon: Setting expectations right. We designed this step to understand that significant results need time. Patience is our ally.
- Retrieval Focus: Currently, the impact dwells in the retrieval stage, not yet integrated into search ranking. So, finding it in the top results? Not just yet.
- Segmentation Wisdom: Strategic segmentation during experiment design. We divide results into low, medium, and high segments, honing in on the low segment for impactful insights.
While we await the magic, remember that great things take time!
Experiment Results
The A/B test aimed to evaluate the impact of a new model on various metrics related to Successful Events (SE), search extensions, and user interactions in the Jobs category. While some metrics have reached significance, others with positive impacts exhibit small effect sizes. Here's a breakdown:
Observations and Insights
- Positive uplift in most metrics, especially those related to SE, suggests a promising impact.
- While results are not statistically significant across all metrics, observed patterns and confidence intervals indicate potential significance with additional data.
- A significant decrease in extensions and keyword searches per user when results are <50 aligns with the hypothesis, indicating a meaningful impact in that scenario.
Cost Reflection and Future Pathways 💡💸
Reality check: Prosus AI Assistant's brilliance comes at a cost — approximately 15K per month. It's time to reassess. Do we stick with Prosus AI Assistant or venture into the world of self-hosted models? The journey has just begun.
Balancing Costs and Benefits:
The revelation of the project cost prompts a deeper reflection on sustainability and efficiency. While Prosus AI Assistant served well in exploration and POC, the financial lens urges us to explore alternative paths for the future.
A Pivot Towards Comprehensive Solutions:
This juncture is an opportunity to reassess job-role extraction and envision a more comprehensive solution. A dedicated self-hosted model opens doors to capture a broader range of information, enriching the search experience beyond job roles.
Educational Insights for the AI Journey:
Our experience offers insights for AI enthusiasts. While external services expedite exploration, long-term considerations, especially related to costs, guide strategic decisions. Our journey reinforces the importance of adaptability aligned with evolving project needs.
Continued Iteration and Refinement:
Though conclusive insights may need time, potential collaboration with the ranking mechanism underscores the anticipated impact on search relevance. As we refine, we eagerly anticipate unlocking the full potential, delivering a more precise job-search experience.
Looking Ahead: An Informed Future 🔮
As we stand at the crossroads of possibilities, the lessons learned from this project propel us toward an informed future. The commitment to delivering an exceptional job-search experience remains resolute. The following steps involve careful evaluation, exploring alternatives, and shaping a path that not only meets today's needs but anticipates tomorrow's demands.
Join us in the next chapter as we navigate the evolving landscape of AI solutions, committed to providing a search experience that transcends expectations.
