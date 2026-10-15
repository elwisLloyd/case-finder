# Introducing Test-Driven Vibe Development

Источник: https://medium.com/asos-techblog/introducing-test-driven-vibe-development-0effe6430691

Note: The draft was submitted on the 8th of August. Some of the processes and challenges mentioned in this article have been refined since. We’ll be sharing these updates soon.
In the coding sphere, technology is sprinting at a breakneck pace, with new LLM-driven capabilities debuting nearly every day. When it comes to software development, the nirvana — “software developing software” — has shifted from fantasy to a realistic proposition. We are in the eye of a genuine paradigm shift in how we deliver products.
But revolutionary changes are rarely clean. And this one is not without its challenges and a sea of sceptical voices questioning its viability.
In this piece, I’ll share how we’ve experimented with adapting this incredible, if disruptive, technology into our software development lifecycle in a way that limits some of the common pitfalls accompanying agentic LLMs in real-world enterprise-level product builds. Along the way, I’ll recount a few humbling lessons and observations from our journey close to the edge of this exciting frontier.
Vibing Coding
In the beginning of 2025, AI researcher Andrej Karpathy coined the term vibe coding to describe the process where, “developers primarily use natural language prompts — speaking or typing in plain language — to instruct AI tools to generate, refine, and debug code.” In this approach, users focus on what they want (the “vibe”) while letting the AI handle the code implementation.[1]
Below is a diagram illustrating the vibe coding cycle:
There are challenges with vibe coding. These include managing the quality of code due to hallucinations, missing defects buried deep in the code which can become a costly fix later on, or the agentic tool developing insecure code.
LLM limitations
When I first tried using an AI agent to develop code, my experience matched these widely documented concerns. Plenty of vibe coding energy but not much rigour. But coming from a quality engineering background, I could see that this was fundamentally a quality problem, be it in process, prompting, or AI output.
Whenever I approach a new project, I start with the solution architecture to gain a better grasp of what I’m dealing with. And so here too, I turned to the LLM’s own architecture.
LLMs are built on the transformer model. While the responses of LLMs are often mind-bendingly impressive, at their core, these systems are fundamentally probabilistic pattern-recognition engines. At the basic level, they ingest words (tokens) and predict the next token by assigning probabilities to a sequence of words to generate the output.[2]
A major challenge with this architecture is attention management: how the model decides which words in the input deserve focus when working out what words to use in the generated output. The probability function used in this process (softmax)[3] is intrinsically unable to handle large complex sentences as the “attention” becomes too thinly spread.[4] This means that accuracy declines as the context increases and the attention diffuses.
Agents have strategies to mitigate this limitation, but the takeaway was clear. To help the AI agent maintain its accuracy, it would make sense to employ fewer, more atomic tasks for a single instruction prompt.
Given this insight, I felt a part of the solution wasn’t to shoehorn the AI agent into the existing software development lifecycle or remain bound by vibe coding, but to rethink the lifecycle in a way that factored the LLM’s inherent constraints.[5]
Test-Driven Vibe Development (TDVD)
The concerns with vibe coding can be addressed by fusing the mature test-first quality engineering practices, which we have already established here at ASOS, with vibe coding. The result is Test-Driven Vibe Development (TDVD): a restructuring of the classic Vibe Coding process that integrates the discipline of established test-first quality engineering practices with the useful aspects of the vibe coding AI paradigm:
· Architecture driven testing to form a highly relevant test strategy.[6]
· ATDD to establish quality-refined acceptance criteria/test scenarios.
· BDD for consistent domain language expression.
· TDD to front load the tests in the implementation phase.
In TDVD, natural language prompts drive the definition of the expected behaviour of the solution upfront through acceptance criteria or tests. This test-first, intent-driven approach ensures that:
· Clear testable requirements as code are generated before functional implementation.
· Code generation is aligned with testable requirements.
· AI-generated implementations are continuously validated against those requirements.
· Bugs and hallucinations are caught early, before they become costly.
· Security and quality risks are managed proactively.
In short, TDVD inverts the current (vibe coding) development lifecycle approach, which sees the functional code generated first before testing occurs. It creates a flow from intent → specification → test → code → validation → deployment.
The activities within the TDVD flow fall within three broad categories.
· Plan — defining the intent in a test-first manner
· Implement — developing the intent in a test first manner.
· Harden — final layer of deepening functional and non-functional test depth.
The Trial
From May through to June, I fleshed out details of a potential TDVD lifecycle and built out supporting prompts. With the framework in place, the next step was finding a a low-risk candidate for a real-world test.
The chosen candidate was an internal reporting solution that calculated stock discrepancies based on stock movement transactions. Although it could indicate a misalignment, it was unable to show what was missing or why, resulting in time-consuming manual investigations and delays in resolving physical versus system stock discrepancies.
What was needed was a solution that could precisely identify and report missing or mismatched stock transactions by comparing actual physical stock position in our warehouse management systems and stock reconciliation records in an automated manner. The solution would enable earlier discrepancy detection, proactive alerting, reduced reliance on manual investigations, faster resolution of stock mismatches, better accountability, and improved stock accuracy for downstream consumers.
The team had several constraints: an engineering lead already juggling multiple commitments, a single part-time senior developer, no frontend expertise, and no dedicated product manager.
Get Irfan M’s stories in your inbox
Join Medium for free to get updates from this writer.
Still, I kicked off the trial with the brilliantly forward-thinking Engineering Lead, Caroline Perryman, and the ever-adaptive Senior Developer Cian Moloney. Together we set out to push the limits of what was possible with this vibe-infused, quality first lifecycle model in an environment that was anything but conducive.[7]
Findings
The MVP we set out to build consisted of the following:
· A backend comprising an API, Azure Functions for data handling, timed triggers, and discrepancy calculation logic, and two data stores.
· A React-based frontend report with three views, each supporting search and dynamic filtering capabilities, plus a notes modal
· Standard essentials: authorisation, authentication, and logging.
Initial estimates for a team of developers to build an MVP was between 4–6 months — 3–4 months for the backend and 2–3 for the frontend.
With Caroline, Cian (at 50% availability), and myself, we delivered the MVP plus some nice-to-have capabilities (an additional File Detail View, which provided a detailed drill-down view showing comprehensive file-level metadata and SKU-level discrepancy data, and a report export feature) in 4 weeks.
During this period, we rebuilt approximately 80% of the MVP twice to refine our prompts so that they achieved higher-quality outputs.
If we exclude the two tear downs and combine the Planning and the actual Implement phases, the total time active development time was 42 hours or 11 workdays.[8]
The results are positive. We were 7–10 times faster than the original MVP estimate and we also delivered extra capabilities, all with a team effectively consisting of two and a half people.
Of course, it must be stressed that the original estimate was based on the team’s lack of experience in the technology stack. Another team might have quoted something leaner. Even so, within our context and constraints, the acceleration was undeniable.
Lessons
TDVD combines some of the fluidity, speed, and creativity of Vibe Coding with the discipline of a test-first blueprint, and guardrails attuned to the LLM’s architecture. Our experiment proved the concept has legs, but the journey wasn’t exactly smooth sailing.
We tore down the solution and rebuilt it twice even though we got it working each time. Why? Our features were not small enough and, consequently, not iterative enough. We failed to maintain the LLM’s context between lengthy prompt phases. We adapted by revising our PRD by breaking the capability features down into much smaller user stories, and rebuilding our implementation step guides so that each cycle focused on no more than two features. We also introduced implementation summaries using our own custom prompt to provide continuity for subsequent implementation phases.
Other niggles included the agent building out tests and the associated code, but not executing the tests, which resulted in mounting technical debt. At other times, the agent confidently claimed it had completed a revision or fix but left failing tests unresolved. The solution was what any good TDDer would do in this situation. We prompted the AI to never proceed to the next task step until all tests passed.
On the specificity of instructions, we discovered a curious trade-off. Slightly more vague instructions gave the AI room for creative assumptions. For example, when asked to “add a page,” it not only built the page but updated the navigation bar too. Overly precise instructions, on the other hand, killed that initiative. When we sharpened the prompt and told the agent exactly how to add the page, it did so, but didn’t update the navigation bar.
Finally, it pays (premium request!) dividends to really think about the dependencies. Before starting the Implement phase of TDVD, it’s worth ensuring the skeleton solution includes all the prerequisites and installations already. Failing to consider this or failing to guide the agent on handling missing dependencies will result in token-draining technical debt and rework.
Final thoughts and next steps
Perhaps the most radical of all observations weren’t about the AI. They concerned us humans in the experiment.
First, the obstacles to delivery. The biggest time sink wasn’t necessarily the code generation. It was the infrastructure plumbing. Chasing down people for access and configuration cost us several days of development time. This is an area which could do with increased automation and perhaps some “agentic” attention to accelerate delivery further.
Second, rapid skill acquisition and augmentation. We started as backend specialists and walked out having built a full stack solution with technologies we had never touched before the trial.
Third, roles in the TDVD lifecycle. I wanted to push the boundaries of the experiment and from the outset stipulated that we were not assuming fixed roles. The results were both surreal and empowering at the same time:
· Caroline shifted between product manager, systems specialist, solutions architect, and a tech lead.
· Cian assumed the roles of a solution architect and platform engineer, while vibe coding and testing chunks of both the backend and frontend solution.
· I designed, orchestrated, and continually revised the TDVD development process, helped Caroline define the product, designed the solution, and coded and tested portions of the full stack implementation.
We mobbed, we swapped roles, and we blurred boundaries beyond our specialisms. The dynamism in the teamwork was on a higher plane, an organic outcome of the TDVD flow.
So, what does this all mean? Well, it’s an exciting time to be involved in software engineering, for sure. But more significantly, early signs suggest TDVD might just be the recipe for stable, quality-infused, yet rapid product delivery.
Or, to put it less formally: the vibe is strong with this one.
Citations:
[1] Google. “Vibe Coding Explained: Tools and Guides.” Google Cloud, 2025, cloud.google.com/discover/what-is-vibe-coding.
[2] For a useful and easy to digest overview, see: Google. “Introduction to Large Language Models | Machine Learning.” Google for Developers, 8 Aug. 2023, developers.google.com/machine-learning/resources/intro-llms.
[3] https://en.wikipedia.org/wiki/Softmax_function
[4] Veličković, Petar, et al. “Softmax Is Not Enough (for Sharp Out-of-Distribution).” ArXiv (Cornell University), 1 Oct. 2024, https://doi.org/10.48550/arxiv.2410.01104.
[5] There is some academic support for pre-emptive measures through workflow optimisation to assist agentic responses. The researchers in one study examining why agents struggle to resolve real-world GitHub issues stated the following:
“Improving the workflow of software development agents is a promising direction. Enhancing an agent’s process with early, proactive measures that pre-empt common yet pervasive errors may reduce overhead and improve resolution rates.” — Chen, Z., Ma, W. & Jiang, L. (2025) ‘Unveiling Pitfalls: Understanding Why AI-driven Code Agents Fail at GitHub Issue Resolution’, arXiv preprint arXiv:2503.12374. Available at: https://arxiv.org/abs/2503.12374.
[6] ADT is a model I developed for forming test strategies directly from architecture diagrams.
[7] I’m grateful to Caroline and Cian for believing in the idea, backing the trial, and showing such patience and commitment in bringing it to life.
[8] We recorded 32 hours mob sessions and approximately 10 hours of individual work.
Irfan is a Principal Engineer specialising agentic delivery at ASOS. He is passionate about leveraging AI beyond AI-assisted coding to deliver quality products at pace. Currently proving a reimagined, real-word, quality-first, AI-driven product development lifecycle.
