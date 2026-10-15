# A Platform-centric Approach to AI-assisted Code Generation at Intuit

Источник: https://medium.com/intuit-engineering/a-platform-centric-approach-to-ai-assisted-code-generation-at-intuit-03984a85558e

A Platform-centric Approach to AI-assisted Code Generation at Intuit
As generative AI tools become embedded in more and more developer workflows, a complex and nuanced challenge has emerged: how do we translate the excitement around these technologies into measurable improvements in engineering productivity?
At Intuit, with over 8,000 engineers building new experiences for ~100M customers, it’s been necessary to take a platform-first approach to scalably incorporating these tools into our development process. This means treating AI-driven development not just as an integrated development environment (IDE) extension, but as a capability — deeply integrated, highly contextual, and architected for scale.
In this blog we’ll share what we’ve learned on our journey to achieving 8x developer velocity over the past four years (Source: Intuit Investor Day 2024), and how we’re building the future of AI-native development through intelligent, context-aware systems.
Identifying where AI coding assistants can help
Intuit’s end-to-end product development lifecycle spans across multiple personas. To understand where AI could have the most meaningful impact, we started by analyzing how our developers spend their time. As shown below, the majority of engineering effort is concentrated in two key areas: the Inner Loop, where developers write, test, and iterate on code, and the Outer Loop, where they deploy, monitor, and operate applications in production.
Together, these phases account for over 70% of an Intuit developer’s day-to-day work — far more than upfront planning or design. It was in these high-effort, high-friction zones that we also observed the most persistent challenges: slow and tedious test authoring, infrastructure misconfigurations, delayed feedback cycles, and difficulty identifying root causes during outages. These pain points made it clear that to truly improve developer velocity and experience, we needed to focus our AI investments on solving real problems in the Inner and Outer Loops.
Off-the-shelf coding assistants have limits
Like many organizations, we began our AI coding journey by experimenting with many of the generally available IDE extensions that provide a simple chat interface or autocompletion that invoke LLMs to generate code. Having access to the latest models of AI coding assistants, developers quickly embraced their ability to generate boilerplate code, but over time usage declined, particularly among senior developers.
The reason? These tools didn’t understand Intuit’s environment. It wasn’t that they were not generating code that worked — AI coding assistants are pretty good at that. The bottleneck manifests in the lack of awareness of Intuit-specific APIs, architectural conventions, code quality standards, and compliance requirements. Suggestions often needed heavy editing, tantamount to writing the code from scratch. Sometimes they were flat-out incorrect.
Context is the key multiplier — golden repos can help with that
The breakthrough came when we started injecting internal knowledge (dubbed the Intuit Context) into the development experience, served in real time by our scalable backend with context-enriched query pipelines.
For a coding assistant to understand Intuit’s coding standards and conventions, it needs to learn from the best examples that we can offer. One key aspect of making the coding assistant aware of Intuit context relies on golden repositories.
A golden repository is a curated collection of high-quality, accurately-labeled code examples that serve as the definitive source of clean data for contextual code generation systems. It showcases how end users can effectively utilize a capability’s features within the context of Intuit-specific development practices. This curated data helps optimize code generation accuracy and streamline development workflows.
A golden repository typically contains:
- Code Examples: Practical code snippets demonstrating the capability’s usage, such as API specs and SDK documentation.
- Validation Data: Prompts and expected responses used to validate the CodeGen model’s accuracy and performance.
- Metadata and Tagging: Information used to categorize and organize examples for improved search and retrieval.
- Capability Overview: An about.md file that provides a comprehensive introduction to the capability, detailing its purpose and functionalities. This overview is designed to equip consumers with a clear understanding of the capability’s core value proposition.
Just as importantly, having golden repositories in place has enabled us to pursue a vendor-agnostic approach to AI integration. By anchoring our code generation strategy in internally-defined patterns and reusable scaffolding, we ensure that our models — regardless of provider — are generating output that aligns with our architecture, conventions, and quality expectations. This gives us the flexibility to evaluate or switch between AI platforms without sacrificing consistency or retraining every tool from scratch.
What this looks like for the developer
So far, we’ve been looking at AI-assisted coding assistants at a high level. Let’s now walk through a rudimentary example of what it might be like for an Intuit developer to build a new web app using an AI coding assistant with Intuit’s context. Say we are building a very simplistic example of a loan eligibility form. First, we begin with a quick mock-up of the end product:
Recent best practices suggest that we start with a lazy prompt. Let’s say we give our coding assistant the following prompt.
Generate a loan eligibility widget. The widget should be a form that contains fields “First Name”, “Last Name”, “Annual Income”and “Credit Score”.
Get Deepa Soundararajan’s stories in your inbox
Join Medium for free to get updates from this writer.
Predictably, after some npm commands we’d get a basic prototype of a form that matches the shape of our mockup.
Now this is a good start, but understandably (and this is the typical output if we were using generic coding assistants) they are not consistent with how Intuit products look. Now, if we were working with a coding assistant unaware of Intuit’s context, we’d have to examine the generated code, check against existing codes and documentation, and manually tweak each component so that the output is up to Intuit standard.
It is in taking care of this latter part that our contextually-aware coding assistants shine. Let’s see what happens if we just change the prompt a tiny bit:
Generate a loan eligibility widget by following Intuit Best Practices and coding patterns. The widget should be a form that contains fields “First Name”, “Last Name”, “Annual Income”and “Credit Score”.
Now compare the outcomes:
Observe how, by simply telling it to follow Intuit best practices, our coding assistant will know how to produce Intuit’s default patterns, buttons, colors, and even the logo at the top. Quite an improvement from the previous iteration with just eight more words added to the prompt. Note that this is entirely auto-generated, without any developer intervention.
To fully appreciate the work of Intuit’s context, we need to look at the code that was generated:
You’ll also notice the following bit stands out:
What’s new here is that the coding assistant has the foresight of pulling in the relevant Intuit Design System and AppFabric libraries and building the form accordingly. This is one example of the missing key in productively leveraging coding assistants- generating code that not only works, but also conforms with our standards and best practices.
How we measure impact
To evaluate our impact, we track:
- Test generation: 58% of AI-generated tests are used without modification, after review — these cover standard unit tests, such as form validations and common expected behaviors, allowing developers to focus on complex test scenarios
- Pull request (PR) velocity: Engineers using AI-assisted workflows merge PRs 56% faster
- Developer sentiment: High satisfaction and adoption across teams
- Backend code generation time dropped by 3×
- Frontend generation tasks improved by over 10×
One thing to notice in these metrics: they consistently scaled across developers of all types. This finding affirmed a simple but powerful idea: if context helps human engineers work faster, it helps AI, too. With it, the assistant became more than just a helper — it became a collaborative partner that understood our systems, our style, and our constraints.
What’s Next
There is a lot more to be done! With a goal to turn AI from a helpful assistant into a reliable teammate across every phase of the software development lifecycle. Our roadmap includes:
- Expansion of agentic task support
- Enhanced integrations with CI/CD pipelines and cost dashboards
- Real-time analytics for development value metrics
- Streamlined onboarding for internal capability owners
Takeaways
In retrospect, the most important lesson here is a simple one: Improving engineering productivity with generative AI is not only about adopting the latest tools, it’s about building the right foundation.
Our experience at Intuit has shown that real impact comes from treating AI-assisted development as a platform capability, not a plug-in feature. This means deep integration with existing systems, embedding organizational knowledge into the developer experience, and designing for scale from the outset. For organizations on a similar path, meaningful outcomes with AI-assisted coding begin when it understands your development environment as well as your engineers do.
