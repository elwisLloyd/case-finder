# A Retrospective: Agoda’s GenAI Journey Thus Far

Источник: https://medium.com/agoda-engineering/a-retrospective-agodas-genai-journey-thus-far-b0739683d53e

Featured
By Shaun Sit
Introduction: Two Years In
We recognized the potential of GenAI early and began exploring how it could transform the way we build software, support customers, and empower our teams. In February 2023, we launched a company-wide GPT Hackathon, the spark that set in motion a multi-year journey of adoption, experimentation, and lasting transformation.
As of mid-2025, GenAI is deeply woven into our operations. What began with a few experiments has grown into more than 200 applications and services, spanning everything from customer service and engineering to marketing and internal tools.
And the impact is real, by the numbers (as of July 2025):
- 73% of employees use GenAI productivity tools
- On average, 45% of internal tech support tickets are handled by GenAI
- GenAI-driven features boosting customer experience and engagement
In this blog, we’ll take a retrospective look at Agoda’s GenAI journey: where we started, what we’ve built, what we’ve learned, and where we’re headed next.
Igniting the Spark — The GPT Hackathon
Our GenAI journey began not with a strategy deck or a top-down directive, but with a hackathon.
In February 2023, over 200 developers across product and tech came together for a three-day company-wide event to explore one question: What could we build if we put large language models in the hands of our people? Teams were given a one-hour crash course on GenAI and its APIs and then set loose. The results were immediate and inspiring.
More than 40 ideas were prototyped, ranging from customer support bots and internal case summarizers to hotel information assistants and SEO content generators. Not every project made it to production, but what emerged was far more valuable: a shared confidence that GenAI could meaningfully enhance the way we work and how we serve our customers
Even though GenAI was still in its early days, the hackathon demonstrated three things clearly:
- LLMs were already capable of real work, not just chat demos.
- Prompt engineering mattered more than expected (back then), and subtle phrasing led to wildly different results.
- Access to internal context and the right data was the biggest challenge — and the key to unlocking value.
But most importantly, it created momentum. A wave of GenAI curiosity swept through Agoda, setting the tone for everything that would follow — a grassroots, builder-first approach to GenAI.
Embedding GenAI — Building a Company-Wide Culture
After the hackathon, something unusual happened: the energy didn’t fade. Instead of fizzling out, interest in GenAI grew organically. The Slack channel used during the event was renamed mastering-gpt, following our mastering-* naming convention for community-driven learning spaces. These are informal hubs where engineers and teams share relevant news articles, showcase new projects, ask for help, and exchange knowledge freely.
mastering-gpt quickly became the nerve center of our GenAI journey. From sharing prompt techniques to announcing new tools and updates, the channel grew into a living knowledge base powered by its contributors. It wasn’t owned by any one team, and that was the point. It represented a self-sustaining community of people curious about what GenAI could do and eager to help each other figure it out.
This grassroots momentum became the foundation for a broader GenAI movement. To lower the barrier even further, we introduced a custom Slack bot integration that allowed employees to interact with GenAI directly inside Slack. That early experiment helped build confidence and curiosity, and soon after, we launched our own internal ChatGPT-like web interface, giving teams a more powerful and secure space to explore GenAI on their own terms.
Underpinning this evolution was a deliberate “Inside-Out” approach to improving internal workflows and developing the skills, patterns, and infrastructure needed to build GenAI products responsibly and effectively. The goal wasn’t just to use GenAI; it was to learn how to build with it.
- Learn how to build GenAI-powered applications: from designing assistant behavior to handling tool integrations, from shaping good UX to knowing when GenAI is the wrong choice.
- Develop prompt mastery: treating prompting as a new kind of interface design, with patterns, debugging techniques, and documentation.
- Figure out how to test GenAI features: what does quality look like for an assistant? How do you detect regressions? When do you simulate vs go live?
- Build infrastructure that supports rapid iteration and safe deployment: internal use gave us the space to learn and adapt without the high stakes of a customer environment.
To support this momentum, especially as mastering-GPT turned into an active learning hub and the Slack bot became a go-to tool, we focused on practical enablement. One of the earliest steps was rolling out coding assistants like GitHub Copilot across IDEs, letting developers explore GenAI inside their daily workflows. These accessible tools turned early curiosity into a daily habit, helping integrate GenAI into workflows and lowering the barrier to experimentation.
Scaling Responsibly — Infrastructure and Access at Scale
As interest in GenAI grew across the company, so did the number of tools, teams, and experiments. This was exciting, but also came with new challenges: How do we ensure good governance? How do we manage costs? How do we prevent duplicated effort?
To scale responsibly, we began building shared foundations that could support growth without friction.
The GenAI Proxy
A core part of that foundation was our GenAI Proxy, a centralized access point for all GenAI traffic inside Agoda. It allowed us to:
- Centralize compliance and legal review for new use cases, ensuring secure and responsible access.
- Route requests between different GenAI Providers as needed — we started off with OpenAI.com and Azure OpenAI models and gradually added more over the years.
- Track usage by service and team, down to the request and token level.
- Automatically attribute cost and usage back to teams.
- Enforce rate limits, block risky calls, and monitor usage patterns.
The GenAI Proxy gave teams a central gateway for all GenAI traffic, with built-in controls to support responsible usage. As part of registering a new use case in the Agoda Service Catalog, teams undergo a compliance and legal review process. Once approved, they gain access to GenAI capabilities without needing to manage authentication, billing, or usage tracking. This centralized model enabled rapid experimentation while maintaining governance.
Our Internal Chat Assistant Platform
At the same time, we introduced our internal Chat Assistant Platform (akin to ChatGPT UI Clone) — a cost-effective, secure tool designed to give every employee broad access to GenAI-powered chat assistants for everyday tasks, boosting productivity and shifting mindsets around GenAI adoption. Rather than relying on external interfaces, we built our own platform for three key reasons: to define assistant behaviors in a GenAI-agnostic and internally controlled way, to avoid costly per-seat pricing models, and to ensure a unified interface that could work across any model provider.
Get Agoda Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
The platform was built as a Progressive Web App that brought together useful GenAI tools in one place. This included:
- A Chat UI with access to Agoda’s internal systems
- Ability to create custom Assistants with pluggable tool support tailored for tasks like SEO, prompt testing, or data queries. Built specifically to integrate with our systems and workflows.
- Playground for prototyping prompts, function calls, and model parameters.
- Additional Chrome extension that opens a side chat for any saved assistant, using the full page context to provide smarter, more relevant responses.
This platform helped make GenAI a natural part of daily work, embedded across roles and workflows, and adopted organically across teams because it consistently proved useful.
Laying the Groundwork — Unlocking Adoption and Scale
These infrastructure investments may not have been as flashy as GenAI demos, but they laid a solid foundation for sustainable growth, enabling both employee adoption and service expansion.
By Q1 2024, a third of our employees were using GenAI tools weekly. That number grew steadily, surpassing 50% by Q3 2024 and reaching 73% by Q2 2025.
In parallel, Agoda teams launched 119 applications and services using GenAI in 2023, growing to 204 by mid-2025, a reflection of how accessible and scalable the process of using GenAI in Agoda has become.
These foundations allowed teams to move quickly but safely, building with confidence and clarity. They normalized GenAI as a trusted part of daily work, setting the stage for the next phase: turning these tools into durable business outcomes.
Powering Internal Teams — GenAI in Everyday Work
With over 200 GenAI-powered applications and services now live across Agoda, we won’t attempt to catalog them all here. Instead, we’ll highlight a few internal-facing examples that demonstrate how GenAI is reshaping the way teams work, from decision-making and documentation to development and support.
Assistants/GenAI Powered Applications for Specialized Work
Purpose-built assistants have helped teams go beyond generic prompting. For example:
- Query Assist lets non-technical users generate SQL queries from natural language, and when paired with the sidechat browser extension, can even be used directly on a website without requiring code changes
- Document Processor lets users apply GenAI to process structured data in spreadsheets, such as translating hotel names, categorizing text, or summarizing free-form responses. This effectively turns GenAI into a smart cell-by-cell assistant.
- AskGoda supports technical support channels by auto-answering internal questions using documentation and past tickets, reducing load on teams by handling 50% of incoming tickets.
- Meeting Helper automatically summarizes meetings, captures key notes, and allows users to ask questions about past discussions. Attendees who can’t join can delegate questions in advance, and the assistant proactively follows up with answers once the meeting concludes.
- Many Bespoke Assistants/Applications have been developed across domains, from data platforms, security, fraud detection, marketing, design, legal, finance, supply, customer service, human resources, and many others. These assistants are often deeply embedded in specific tools or workflows, built for narrow but high-impact tasks.
These tools weren’t built as one-off demos; they’re maintained, used, and continuously improved as part of everyday workflows.
Accelerating Engineering
Developers have embraced GenAI inside the IDE, using tools like GitHub Copilot, Cursor, Claude Code, OpenAI Codex, and others for coding agents. Internally-built tools extend this with:
- Jira Planning Assistants: that enrich new stories using internal knowledge, flag inconsistencies, link relevant resources, and generate descriptive test plans.
- Autonomous Coding Agents: that automate large-scale migrations, such as replacing legacy testing libraries or upgrading frameworks with test-validated output and minimal manual intervention.
- Code Review Assistants: that help engineers catch common issues, suggest improvements, and enforce code quality guidelines consistently across pull requests, providing consistent, automated feedback on every review.
- Auto Documentation Tools: that detect code changes and generate or update developer documentation in the same merge request using GenAI.
- Monitoring and Log Analysis Agents: triggered by anomaly detection systems, which then get agents to analyze selected error log streams with GenAI, comparing with known past incidents to assist on-call personnel during triage.
- Custom MCPs: exposing Agoda’s internal systems, like build tools, documentation, and environments, to enrich coding assistants with additional context.
These engineering assistants reduce repetitive tasks and streamline development workflows, allowing engineers to shorten the development lifecycle time.
Reducing Manual Load and Improving Efficiency
GenAI tools are helping reduce cognitive overhead across functions. Internal support workflows, for instance, have seen meaningful improvements through automated triage, knowledge retrieval, and repetitive task handling. These tools are now embedded in daily work, helping teams move faster and focus on higher-value problems.
Shipping Value to Customers — GenAI in Agoda Products
While much of our early GenAI focus was internal, the experience we gained in building robust GenAI systems laid a strong foundation for customer-facing innovation, enabling us to deliver smarter, more intuitive experiences for travelers.
A few highlights include:
- Q&A Assistants: embedded across Agoda to help users get quick, natural language answers, whether about hotels, policies, or booking form details — improving clarity and conversion
- Review Helper: that helps users summarize and filter large volumes of guest reviews, making it easier to make informed decisions.
- Better Content Curation: through automated tagging and enrichment — using GenAI to derive insights from unstructured content like hotel descriptions, amenities, or user reviews
There are also many more GenAI-powered features on the roadmap for our end users. While this blog won’t go into detail on these future initiatives, we are just getting started with reimagining the travel experience with GenAI.
Conclusion: What We’ve Learned and What’s Next
Two years into our GenAI journey, the results are clear: with the right infrastructure, an empowered builder community, and a focus on practical adoption, GenAI has driven meaningful transformation across Agoda. This shift has touched everything from how we write code and support our teams to how we serve our customers.
What made this possible?
- A foundation-first approach that prioritized access, scalability, governance, and flexibility: We understood early on that sustainable GenAI adoption required robust infrastructure. By building a centralized proxy, secure internal platforms, and clear governance processes, we created a safe and efficient environment for experimentation and deployment. This minimized friction and enabled programmatic adoption, giving teams the confidence to move fast while staying compliant.
- A grassroots culture of exploration — where ideas grew from hackathons into production: The initial hackathon wasn’t a one-off event; it sparked lasting curiosity. Our community-driven culture, exemplified by the “mastering-GPT” channel, empowered developers to share, learn, and build together. Many of our most impactful tools emerged not from mandates, but from this bottom-up momentum.
- Focusing on impact — we started with automating the repetitive, accelerating the complex, and freeing people for higher value work: Exploration alone wasn’t the goal. We stayed grounded in use cases that delivered measurable value, things that reduced manual effort, improved speed and clarity, and helped teams do more with less.
- Bridging the Gap from Prototype to Production: Creating a GenAI-powered demo is deceptively easy, but building a high-quality, reliable production application is much harder. We invested in helping teams bridge that gap by developing skills in prompt and context engineering and learning how to test, monitor, and refine GenAI applications at scale.
- Leadership commitment from the top: Our journey was backed by clear, consistent support from our leadership, not just in vision, but in investment and priority. This top-down alignment enabled GenAI to become a company-wide effort, amplifying the grassroots innovation already underway.
As GenAI technology evolves, so does our ambition. The building blocks we’ve laid down give us the ability to scale thoughtfully, safely, and boldly into what’s next!
This journey wouldn’t have been possible without the talent, energy, and creativity of every team and individual at Agoda. From the engineers who built the first prototypes to the product teams scaling real-world solutions to every employee who embraced new tools, thank you. Special thanks to the teams featured throughout this blog for sharing their work. It’s a collective achievement, and we’re excited to see what we build together next.
