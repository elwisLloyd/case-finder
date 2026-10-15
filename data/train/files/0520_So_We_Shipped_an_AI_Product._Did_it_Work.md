# So We Shipped an AI Product. Did it Work?

Источник: https://www.honeycomb.io/blog/we-shipped-ai-product

Like many companies, earlier this year we saw an opportunity with LLMs and quickly (but thoughtfully) started building a capability. About a month later, we released Query Assistant to all customers as an experimental feature. We then iterated on it, using data from production to inform a multitude of additional enhancements, and ultimately took Query Assistant out of experimentation and turned it into a core product offering. However, getting Query Assistant from concept to feature diverted R&D and marketing resources, forcing the question: did investing in LLMs do what we wanted it to do?
The short answer is… mostly. Query Assistant correlates with some extremely positive activation metrics and it’s inexpensive to run, thanks to OpenAI’s reasonable pricing. However, it doesn’t correlate strongly with every product activation metric we hoped it would, and although adoption is higher than we thought it would be, it isn’t as high as we hoped it could get. Overall though, it continues to be a worthy addition to the Honeycomb platform and we’re excited to continue investing in LLMs moving forward. Let’s dig into a few lessons learned, insights captured, and things we’ll continue to tweak!
But first, we’d like to hear from you! If you’re also building with LLMs, we have a short survey and we’d love to talk with you: 👉https://forms.gle/UXYWyTxGTs6BqKNS7
The learning curve of querying in Honeycomb
For Honeycomb’s business, everything comes down to your ability to seamlessly query your data. Since we charge only on how much data you send us—not how much you query—the more active you are in our product by querying your data, the more value you’re going to get out of it. We find that most people approach Honeycomb with an existing service they’ve instrumented with OpenTelemetry, a mental model of application behavior already, and a set of questions they’d like to ask of that data. When you query actively, you often find issues that you didn’t even know existed! And from Honeycomb’s perspective, that value typically leads to teams upgrading to a paid pricing tier as they instrument more services and query for different kinds of application behavior.
However, while this motion sounds great on paper, the reality is that Honeycomb has a learning curve. It requires a change in process (and sometimes culture) to make the most out of it. We’ve found that users can struggle to map the mental model of their data and what they want to query into our interface, especially if they don’t have experience with other observability or monitoring tools. Once new users learn Honeycomb’s interface—and in particular, the ability to create complex queries—they use it more and more. But that initial hump can be hard to get over.
LLMs’ promise of accelerating the learning curve associated with queries
When LLMs hit the market earlier this year with affordable prices, we were excited about the possibilities of the world’s most powerful ML models now available with a simple API call. If a machine can turn natural language into something else (in our case, a Honeycomb Query object), maybe it can help new users familiarize themselves with querying their data in Honeycomb, kicking off that flywheel where they find something interesting, instrument more, and query more.
Given the problem and potential fit for LLMs, we decided to invest resources into building Query Assistant. As we quickly found out, it was a bunch of hard work—so if you’re under the impression that LLMs are magic boxes that solve all your problems, let me stop you right there. We learned quickly that we stood no chance at predicting the variety of inputs users would provide in natural language against their data. We also had no way to predict how the LLM would respond to these inputs and contextual data that differs for every user. So we shipped very quickly, adopting a “ship to learn” mindset.
We believe that if you’re building with LLMs, you must ship early and often. You can’t debug or unit test LLMs in the traditional sense because they’re nondeterministic black boxes. You need to capture user inputs, LLM outputs, and important metadata about those interactions and systematically analyze them to understand what your users are doing and how an LLM responds to that. I also recommend using Service Level Objectives (SLOs) to monitor changes over time to make sure you’re fixing problems in your user experience without regressing behavior that already worked. Since you can’t write a regression test like you would with most software, you need a tool like an SLO to monitor your changes based on real-world data. If you don’t change your software engineering practices, you’ll be stuck forever with something too unpredictable and unreliable.
After a period of rapid iteration, sometimes shipping every day, we were able to bring Query Assistant out of experimentation and feel confident in its behavior as a core product offering.
Success metrics for Query Assistant
To measure the effectiveness of Query Assistant, we looked at several metrics for new teams created after we shipped the feature.
First, we distinguished between two kinds of activities: manual querying and natural language querying. Manual querying is when you use our Query Builder interface to create or modify a query. Natural language querying is when you only use the Query Assistant to create and run a query for you. We assessed the following criteria:
- Percentage of active teams who ran a manual query, who used the feature, by pricing plan
- Manual querying retention over several weeks
- Percentage of teams who ran a manual query and then created a “complex” query
  - A “complex” query consists of several WHERE and GROUP BY clauses
- Percentage of teams who ran a manual query and then created a Board or Trigger
- Query Assistant retention
There’s likely more metrics we can look at, but we’d already established these as good indicators for product activation, and like most SaaS products, Honeycomb sees product activation as a critical business metric. Our sales team also feels this way: when people are more engaged with Honeycomb, it’s easier for them to sell our product.
What we hoped to understand
We hoped that all these measures would go up:
- High usage across all pricing plans, but in particular our Free tier teams, many of whom drop off after a certain amount of inactivity
- Higher manual querying retention for teams using Query Assistant
- More complex queries from teams using Query Assistant
- More Board and Trigger creation from teams using Query Assistant
- Continued use of Query Assistant, but not at the expense of manual querying
Additionally, we were looking for verbatim signals from customers and our sales team.
For customers:
- Did Query Assistant make it easier for you to start querying something?
- Did it help you get your team to use Honeycomb more?
For Honeycomb sales:
- Did Query Assistant help introduce our querying capabilities to new prospects?
- Did it help expand Honeycomb usage with current customers?
What we actually learned
Query Assistant did very well by some measures, but not all.
Percentage of active teams by pricing plan who’ve used Query Assistant
We found that, of active teams who ran manual queries:
- 82% of Enterprise and Pro Plus teams used the feature
- 75% of teams in our Self Serve tier used the feature
- 39% of Free tier teams used the feature
That’s not bad, but it’s not great either. It’s not surprising that people who already pay for our product would use the feature. But we were hoping for a much higher usage rate for Free tier teams because they don’t have a financial incentive to use things they’ve bought. When digging into why, we found that a lot of people didn’t even notice Query Assistant existed, even though it’s right below the Query Builder UI.
We initially thought that placing it below the UI was the right compromise between discoverability for new users and staying out of the way for existing users. We don’t want to move the UI around a bunch, and so to try and improve this measure, we changed our initial product onboarding and “nurture” email campaign for new users to let people know that Query Assistant is a great way to get started querying in Honeycomb. Hopefully this helps, but there’s likely more work to be done.
Manual querying retention for active teams
We found that new teams who used Query Assistant correlated strongly with manual querying retention.
- For new teams that used Query Assistant, by week 6, 26.5% still ran manual queries
- For new teams that did not use Query Assistant, by week 6, 4.5% still ran manual queries
This is one of the most positive signals we saw. It was our hope that Query Assistant would help people understand how querying works in our UI and then eventually “graduate” to running more manual and complex queries.
Percentage of active teams who created a “complex” query
When looking at the population of active new teams who ran manual queries:
- 33% of teams that used Query Assistant created a complex query
- 15.7% of teams that did not use Query Assistant created a complex query
This is also a positive outcome. We designed Query Assistant to often emit more “complex” queries—usually in the form of several groupings—to teach users that our querying interface is flexible. It was our hope that this could encourage new teams to create more interesting queries.
Percentage of active teams who created a Board or Trigger
We found another positive correlation for active teams who ran manual queries:
- 11% of teams that used Query Assistant created a Board
- 3.6% of teams that did not use Query Assistant created a Board
We see Board creation as a very strong signal for activation. The thinking is that if you’re saving a query for later, you intend to come back and possibly tweak it later.
Finally, we looked at active teams who ran manual queries and created a Trigger, which notifies them when a query result crosses a threshold:
- 5.8% of teams that used Query Assistant created a Trigger
- 3.6% of teams that did not use Query Assistant created a Trigger
Although there’s a jump, we’ve seen these figures be closer to one another depending on the window of time we measured. Overall, we don’t think that Query Assistant correlates terribly well with deciding what to alert on with Triggers. Trigger creation is one of the strongest signals we have for product activation. When people create Triggers, they’re much more likely to eventually upgrade to a paid tier because they’re looking to get alerted by Honeycomb. And so we can’t really say if Query Assistant helped our business along this line in particular.
Query Assistant retention
The final hard measure that we track is people sticking with Query Assistant itself. We found that over time, new users used Query Assistant a lot on their first day, but after a week, that usage dropped to almost nothing. People came back to it from time to time, but they usually fell into two groups:
- Active teams that query regularly
- Inactive teams that don’t use the product
Paired with our observation that teams who use Query Assistant query manually more often, it’s our belief that users tend to “graduate” from Query Assistant and stick with manual querying.
Finally, we still see semi-regular usage for existing teams across all pricing plans. When we dug into this, we found that it’s often when someone is new to a dataset and wants to “see what’s in there,” or it’s a new person on a team feeling their way around their data and Honeycomb. It seems that Query Assistant plays a consistent role in onboarding engineers in our existing customer base.
Verbatim feedback
We’ve heard some positive things from customers. Namely, several have called it out as helpful for getting started, especially when onboarding other teams. Conversely, when we initially launched, we also got a ton of feedback about how the feature was lacking capabilities. One customer in particular, Intercom, gave us extremely detailed feedback on the kinds of queries they’d ask and how Query Assistant was falling short of expectations. Their feedback was particularly influential towards one of the capabilities we baked into Query Assistant that pulls in team-defined Suggested Queries as a way to guide the model towards more accuracy for schemas with highly custom field names like theirs.
Our sales team has expressed that Query Assistant helped them with onboarding new prospects. In their own words:
“This never-asked-for feature continues to delight our customers and prospects. I love seeing their reactions. It’s the feature you never knew you needed, until it landed.”
We also hear from prospects from time to time that they really liked using it to get a feel for their data and see what Honeycomb is capable of.
Query Assistant isn’t some magical machine that automatically wins sales deals, but it’s often a delighter that engages prospects early and shows them what’s possible. Being able to shorten the introductory phase of an enterprise sales cycle is crucial for us. That initial phase is often centered around “time to value,” and if we can demonstrate that a prospect can see value in Honeycomb in very little time, it sets the rest of the deal up for success.
The cost of running Query Assistant
Outside of the investment to build Query Assistant in the first place, we also have operational costs. Operational cost is often a big concern for people, especially in today’s market. The two models we use for Query Assistant are GPT-3.5-turbo and text-embedding-ada-002. We spent a lot of time reducing the size of our prompt because OpenAI’s rate limits at time of launch (90k tokens per minute) were a big concern for us.
Each request to GPT-3.5 has about 1800 input tokens and 100 response tokens. Each request to text-embedding-ada-002 has at most 100 tokens.
On average, our monthly OpenAI bill is… $30. Even if we switched to GPT-4—which we won’t, due to GPT-3.5 performing very well—it would still cost us less than $1k per month. Especially considering that these are entirely hosted services, so the cost for us is inexpensive. Finally, we store embedding vectors for dataset schemas in a Redis cluster in AWS. Each node costs us about $100 to store vectors.
To summarize, Query Assistant only costs us a few hundred dollars per month. In both engineering and business lingo—that’s cheap! The primary reason why it’s so inexpensive is that we’re using GPT-3.5 and very few of our token usage comes from text generation. Text generation (often called inference) is the most expensive operation for LLMs. If we had a feature where we needed to produce several thousand tokens per request with GPT-4 instead, our costs would be higher.
There are a few lessons to take away from this:
- Limit the output of an LLM if you can. The more you can do with less data, the better.
- Limit the size of your prompts. Prompt engineering efforts go a long way towards cost reduction and being affected by rate limits.
- Use GPT-4 to prototype, but don’t automatically stick with it. It’s an order of magnitude more expensive than GPT-3.5-turbo. If you can spend time on better prompt engineering techniques and get reliable behavior for GPT-3.5-turbo, do it.
Latency measures
When we went live with Query Assistant in May, latency wasn’t great. The average request to GPT-3.5-turbo took about five seconds, but our P99 was measured in 30 seconds or higher. We’d often time out requests as a result.
However, OpenAI appears to have worked tirelessly to improve the quality of their service since May 2023. As of the writing this post, we see the following metrics:
The average request duration is halved and the P99 is several times lower. To us, this means OpenAI is taking their role of being a model hosting provider seriously.
Fun facts from production
Earlier I mentioned that we couldn’t possibly predict how users would use Query Assistant. That has turned out to be true. Here are some highlights.
Emergent behavior with DSLs
Honeycomb has a Domain Specific Language (DSL) for the Derived Column feature. The idea is that you open up the Derived Column editor, write an expression that computes a value based on the values of other columns in your data, and save it. You can then use that Derived Column as if it were a column in the data you send us.
But what happens when someone pastes in a Derived Column expression into the Query Assistant input box itself? None of us ever thought to do this because it… makes absolutely no sense to us. An expression from a DSL in a completely different part of the product has no relation to a natural language input asking for a query. Why would anyone do this? Well…
We noticed a customer inputting things like this:
IF(AND(EQUALS($service.name, "my-service"), AND (NOT(CONTAINS($http.url, "the-url"))),AND (NOT(CONTAINS($http.url, "something-else”)))
Query Assistant produced a runnable Honeycomb query for every kind of expression like this. Furthermore, sometimes the user would mark the result as helpful in our product feedback widget. We wouldn’t have expected that in a million years.
Similarly, people write pseudo-SQL expressions or other pseudo-code expressions and also get results. We never expected that to work either, but hey, that’s why we shipped to learn!
The 16-byte hex value
A lot of Honeycomb customers have an external tool that spits out a trace ID that they want to use in a Honeycomb query. Some users paste only that trace ID into Query Assistant to pull up that particular trace—and it works!
Again, we never tested for this scenario. How on earth is a 16-byte hex-encoded value supposed to be interpreted? We believe that GPT-3.5-turbo’s knowledge base is broad enough to understand that in the context of querying tracing data (which is clarified in our prompt), a value like this is likely to be a trace ID. As such, it’s able to infer that you likely want to filter based on the presence of that value. We do not have an example in our prompt that involves a trace ID, so that’s the best guess we have.
Modifying existing queries
People use Query Assistant to modify existing queries a lot. The idea is that you have a query showing some results, but maybe you want to add another visualization or filter by a new value. It seems that for some people, it’s faster for them to just type out that modification in the Query Assistant input box.
Under the hood, we also include the existing query as context for what we send to the LLM. We found that GPT-3.5-turbo was very effective at understanding if a user was asking for a modification of the existing query or something brand new/unrelated. Query modification wasn’t something we shipped with initially, and we got feedback about that within 30 minutes of launching the feature. The usage matches the feedback: people are using it to modify queries.
Overall takeaways when using LLMs to ship new features
Query Assistant has been quite a ride. If you were to tell me that we’d be incorporating a nondeterministic black box into our most core product activity—querying—I would have likely laughed you off. However, reality has panned out differently.
Using LLMs has been a net positive for us for the particular job we wanted them to do, correlating strongly with behavior that helps our business in a really fundamental way. Our running costs are also very small. This likely won’t be the last you see of LLMs in Honeycomb. We’re excited to see what other ways we can tastefully incorporate them into our product.
Want to read more on LLMs? Check out these blogs:
