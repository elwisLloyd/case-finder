# AI at Zapier: How we use artificial intelligence to streamline work

Источник: https://zapier.com/blog/how-zapier-uses-ai/

At Zapier, we love solving challenges with artificial intelligence. It lets us focus on more pressing strategic tasks. That's why 97% of the company actively uses AI to do their work.
To achieve that level of adoption, we took full advantage of our own suite of AI tools and products. They let us build mission-critical systems across Zapier to help us securely scale our impact—and bring any automation idea to life, no matter how complex, with or without code.
Curious about our AI-powered workflows? We figured you might be. So we searched our AI hackweek database and asked our fellow Zapiens to help us assemble some of the best examples. These include Zap workflows that use AI apps, AI-powered agents that handle internal operations, AI tools enabled to act in your apps through Zapier MCP, and Zapier Chatbots that talk to customers and prospects.
Keep scrolling for some of the top ways we're using AI at Zapier.
Build automations from wherever you work. Describe the outcome you want, and Zapier connects your tools, runs the steps, and stays on the job after you close the chat. Combine AI with reliable, deterministic automation across 9,000+ apps. Get started for free.
Table of contents
- Customer success operations
- Sales
- Onboarding and HR
- Technical support operations
- Technical writing
- Content and video
- PR and social media
- User education
- Learning and development
- Engineering
- Accounting
- Revenue operations
To get started with a Zap template—what we call our pre-made workflows—just click on the button. It only takes a few minutes to set up. You can read more about setting up Zaps here.
Customer success operations
Carrying out customer calls helps both our sales ops and customer success teams get a detailed glimpse into the customer journey, see what's working, and better understand what Zapier users need.
With AI, we were able to streamline that process from start to finish. Here's how:
One workflow lets team members reduce the prep time before customer calls in Gong by having AI look at a record or deal in HubSpot, gather information about the company, come up with any automation challenges they may be experiencing, then share it with the right person in Slack.
Another workflow pulls recordings of customer calls from the sales CRM. Then it summarizes each call with a quick overview and posts it in Slack, so the team can learn from the interactions.
That includes using AI to analyze and share customer sentiments, giving us a comprehensive view of a customer's interaction with the platform so we can help improve our product.
Sales
Determining which leads are most likely to convert can take up a lot of time and resources. Our sales teams use AI to bridge that gap.
First, they use AI and Zapier to generate transcripts of their calls with leads. AI then creates a summary of those meetings, and Zapier adds that information automatically to the right lead in HubSpot.
That way, sales managers have better insight into the deals that are nearer to closing. They also know who they should be spending time nurturing, without the administrative overhead.
Sometimes, sales managers need to do research to answer prospects' questions about Zapier. Our blog contains a treasure trove of insights. But rather than have managers manually scan the archives, Zapier has a dedicated Slack channel called #blog-post-search-agent, which helps teams easily and proactively find published content relevant to their needs. 
They just go to the channel and type in a topic they're interested in. The channel—powered by a Zapier table and a mix of Agents and Zap workflows—returns a list of relevant posts.
The table even includes tags for post category, so teams can specify what type of post they want (like, say, customer stories or automation inspiration posts).
Here's an example response:
Onboarding and HR
Today, a hot topic among talent acquisition teams is the issue of fraudulent job applications. Some applicants say they work from a certain country, but their actual location makes them ineligible for the role. Or, worse, some applicants try to gain access to company systems to carry out malicious attacks.
AI makes it easy to submit these problematic applications. But you can also use AI to identify them, protecting the integrity of your hiring funnel. That's what our senior talent acquisition analyst, Casey Fiery, did.
Casey built a Zap that enriches every applicant's IP's address and phone number, compares their stated location to their real one, flags mismatches, checks for internet-based numbers, then categorizes them as no, moderate, or high fraud risk. If the Zap detects any level of risk, the recruiter gets a Slack alert with review steps. And for historical tracking, all results get logged in our recruiting software.
AI supports our other HR processes, too. When it comes to sending out forms and surveys, there's a lot of ground for HR to cover, from surveys related to onboarding experiences to general employment feedback forms and retreat assessment surveys.
That's why our onboarding team collects and analyzes sentiment ratings (positive, neutral, or negative) for every response received using AI. It's a great way to save valuable time trying to understand the overall sentiment toward survey topics.
Technical support operations
Dealing with technical incidents is a pretty important piece of the puzzle when it comes to ensuring customer satisfaction, on top of managing a support team's regular workload. At Zapier, AI helps streamline some of these processes.
One team member built an AI-powered bot and pulled it into a Slack support channel. It helps them troubleshoot issues with Zap workflows, get automation ideas, and learn how to use Zapier features more quickly.
Another workflow uses AI to create a formatted daily summary of all the previous day's activities in Slack. This includes all the escalated tickets and issues resolved and discussed for visibility, helping enhance team communication.
AI by Zapier, our built-in AI tool, lets you choose among the latest models and comes with an intuitive prompt assistant. Connect it to Schedule by Zapier to build your own ops workflow.
Another nimble workflow that saves time? Creating the copy for status page updates based on templates and rules provided by the team. With the Zap below, whenever the support team specialists submit an entry in Typeform that describes an issue, AI will create a status page message and send it to Slack for approval. Then a webhook sends the approved message as a new update on Zapier's status page. Job done.
Finally, the support team receives a lot of questions in Slack from other departments about common troubleshooting steps. To deal with these queries automatically, the support team built this Zapier support sidekick:
- When a member of the support team reacts to a question in Slack with a specific emoji, ChatGPT analyzes the message and generates a specific search term.
- Webhooks then pulls together help docs or blog posts that might be relevant to that search query.
- A ChatGPT assistant then reviews the entire history related to that search, including ticket messages, customer interactions, and troubleshooting notes.
- Finally, the ChatGPT assistant responds in the Slack thread with hyperlinked steps to the most relevant help documentation and blog posts returned from the search.
This is what a typical output looks like in Slack:
Technical writing
When it comes to understanding how to use Zapier and troubleshoot issues, Zapier's Help Center is a go-to resource for our users, jam-packed with quick-start guides and helpful tips.
But creating articles for every new product and feature—as well as keeping everything up-to-date across the board—is no small feat. It requires a dedicated team effort to ensure the content remains accurate, so that users can always find the help they need.
To better deal with product updates for release notes, one team member trained a dedicated Zapier agent to help offload the work.
Now, whenever a team member publishes a help center tutorial in Zendesk, the agent verifies whether the article contains a product update according to a few rules. If it does, the agent drafts a product update in Google Docs based on the article's context. The agent then notifies the team in their dedicated Slack channel to let them know it's ready for publication.
Content and video
We're big fans of AI on the content team. Whether it's using AI to summarize articles, create blog outlines, or write meta descriptions, it's proven to be pretty effective.
For the most part, a lot of our writers' time is spent researching articles for this very blog. This workflow uses AI to read and analyze articles before summarizing the key points and takeaways.
We also created a multi-agent system to generate first drafts of feature guides. (These are posts that cover our built-in tools, each one walking you through features, sample use cases, and setup instructions.)
It's time intensive to pull research from various sources to put these guides together. This system speeds up that research, and quickly creates a strong first draft for us, too:
- For each new feature guide, the writer submits the name of the built-in tool and links to relevant help docs through a Zapier form.
- This triggers a Zap that creates a record in a Zapier table, which becomes the single source of truth for a series of Zapier agents.
- The first agent researches customer insights from the Zapier Community for recurring questions, common issues, positive feedback, and desired outcomes surrounding the tool's function.
- The second agent uses Glean to search internal documentation for everyday and advanced use cases.
- The third agent uses this research to write a barebones first draft, using a template created in Google Docs. Then it saves the draft to the table.
- Four more agents edit this draft, each one carrying out a different aspect of the editing process. One weaves customer language into the draft. Another enforces Zapier’s style. The next rewrites structures that sound AI-generated. And the last agent adds relevant links to Zapier posts. Each time a draft is created, it gets saved to the table.
- After the agents finish, the Zap creates a Google Doc with the completed first draft and sends the writer a Slack DM with the link.
When you give AI a ton of instructions to follow, it might miss some details (even if it has a massive context window). Splitting instructions up using a multi-agent design makes it easier for us to ensure our draft incorporates every desired data point and style guideline.
Want to build your own content production system? Use Zapier Copilot, our built-in AI assistant. It can brainstorm ideas, set up automated systems across Zapier products, and troubleshoot issues for you.
Our video team also leverages AI—and one of their best use cases is writing rough scripts for YouTube based on article outlines they source from the blog team. Although these scripts aren't used as final products, the team gets them in Slack and can review and refine them from there.
Another handy way of leveraging AI to write content? The partnerships team built a workflow that watches for any changes external developers make to their integrations, then uses AI to rewrite the updates according to Zapier's style guide. Then we review and publish them inside our release notes.
PR and social media
The PR team writes a lot of press releases. They're often quite templated, too, so it makes sense to use AI to lighten the load. Their workflow takes basic information (like event details, company information, quotes, and key points), and turns it into a coherent and professionally styled press release, according to the rules they give the PR bot. That way, they can spend less time editing a mostly put-together piece rather than writing similar pieces from scratch over and over.
They've also created a range of other bots employees can use to generate employee feedback with suggestions for improvement, strengths and weaknesses, and an overall evaluation. The way it works is simple: AI analyzes a piece of work (like a doc or a design) and generates constructive feedback based on predefined criteria and patterns.
The social media team, on the other hand, uses a range of bots to automate various tasks on social media platforms. From posting content to responding to comments and messages to liking and sharing posts (and even following users), these bots can post content at optimal times for engagement and analyze data to understand trends and user behavior.
We even have an automated workflow for turning social media signals into a structured account-based marketing pipeline. Whenever an account matching Zapier's ideal customer profile engages with LinkedIn content posted by our executives, the AI-powered app Ordinal—connected through a webhook—sends that lead data to Zapier.
The workflow then looks up additional information about the lead in Google Sheets, filters to ensure they meet our qualification criteria, and stores qualified leads in a table for our sales team to follow up on.
User education
Zapier's video courses are designed to help our customers build their first workflows, develop their skills, and explore workflow solutions relevant to them.
The only problem? They're all in English—which isn't exactly ideal for Zapier's international customers.
To tackle this, the user education team came up with a brilliant idea: use ChatGPT to generate the closed captions for each video in ten popular languages.
To do this, they added the English SRT (SubRip subtitle) file of each video course to a table. Then they built a Zap that pulls in ChatGPT and asks it to translate those captions into a specified language (while retaining the same timestamps). Here's a quick glimpse of the result:
Additionally, the team also leveraged the use of Zapier Chatbots to deliver a more tailored learning experience to their customers. These bots were intentionally designed to help customers discover automation ideas and use cases most relevant to their roles and their tech stack.
Now, as customers complete modules in their courses, they can interact with AI:
Learning and development
Members of the learning and development team at Zapier are big fans of bots and already use automation to help design learning and user experiences.
But with the release of Zapier's Chatbots, the team has created dozens of chatbots to aid the learning experience. From bots that give employees coaching tips to others that generate ice breakers for training sessions and team meetings, the team has mastered prompt engineering. The trick is to provide AI with specific company context around Zapier, role context as a learning designer, and a clear purpose—so that the output is always directly related to Zapier.
Here's an example of the result:
Engineering
The engineering team at Zapier deals with a lot of Jira and Zendesk tickets for product-related tasks and sprint planning.
The incorporation of AI into their existing workflows has proven a game-changer. For example, the team built a workflow that summarizes Slack messages, transforms that summary into a Jira ticket, then adds it to the next planned sprint.
When analyzing customer interactions and key performance indicators, the team also leverages a workflow that takes every message within a Zendesk ticket, uses AI to categorize the conversation, and adds all the metrics (like number of replies) to an existing Google sheet for metrics tracking.
The engineering team has also built a number of automated workflows that allow them to collect their achievements over time.
"Daily standups are the individual updates we post to our team that aggregate everything we've done for the day," explains Maggie Storino, a Frontend Engineer at Zapier. "But these accomplishments get logged across a great many systems and tools, like Google Calendar, Jira, Slack, or GitLab."
That's why the team uses Zapier to automatically collect them all in a table. A Zap then pulls from this information and uses ChatGPT to summarize and organize it into succinct messages or updates.
Another engineer created a workflow to speed up writing self-performance reviews—an idea other teams across Zapier are adopting, too. Using Zapier MCP, he equipped Cursor with Glean actions to access internal company data, past reviews he's written, and his achievements scratchpad.
Then, right from Cursor, he can ask to create properly formatted reviews and submit them to our performance management tool.
Want to equip ChatGPT, Claude, and other AI tools with the power to act across 9,000+ apps? Learn how to use Zapier MCP.
Accounting
Our accounting department has to keep track of an incredible amount of tasks throughout the week, so they've incorporated AI into the project management flows to make things easier. A favorite: they use AI to pull a list of tasks in Slack, prioritizing them in order of importance, along with an estimated time slot to complete them.
Although used for personal finances, this is an interesting one: One employee set up a workflow with AI that lets them keep track of all their credit card transactions.
It works like this: Whenever a user receives an email alert about an expenditure, ChatGPT extracts relevant information (like vendor and amount), then categorizes it and adds it to a Google sheet for further analysis. Pretty neat if you like an informative overview of expenses. In a business context, this could do wonders for financial planning and tracking.
Revenue operations
When it comes to creating personalized emails at scale, every email ops team knows how time-consuming they can be, what with the amount of logic and personalization tokens needed to build effective marketing messages.
That's why the revenue ops team experimented with AI, as they realized that ChatGPT could generate dynamic copy in any format. For example, they created a workflow that automatically builds trial expiration emails (including the copy) that highlight specific Zapier features that are most relevant to the user. How? The workflow pulls in user information from their marketing automation system, saving a massive amount of time—no if/then logic required.
The team also built a bot in Slack that answers common questions from internal sales reps about lead stages, lead definitions, and how certain sales processes work. This workflow uses Zapier internal documentation to answer questions, so all answers are as up to date and accurate as possible.
Another bot, trained on ICP upmarket transcripts from deals Zapier has won and lost, gives go-to-market teams all kinds of useful information. Zapiens have used it to source messaging advice, competitive intel, trends they're curious about, and product feedback.
Stay on top with AI and automation
By using any of these workflows, you'll be freeing up whole departments to focus on more creative and strategic work.
From customer support to content creation and engineering, AI and automation combined is a game-changer, with the potential to save time and money, improve efficiency, and increase productivity.
Related reading:
This article was originally published in June 2023 by Elena Alston. It was most recently updated in January 2026 to showcase newer AI use cases.
