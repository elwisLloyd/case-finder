# Agents in production: Lessons shared at MLOps World 2025

Источник: https://digits.com/blog/mlops-world-2025-slides/

Agents in production: Lessons shared at MLOps World 2025
Agents in production: Lessons from building AI systems that actually work
By the Digits Machine Learning Team
Our team has spent years building and deploying machine learning systems for accounting. We've learned that putting AI agents into production is less about the hype and more about the hard-earned lessons that only come from real-world deployment. At Digits, we've been running AI agents in production for over 2 years at this point, and we want to share what we've learned—starting with why we should probably stop calling them "agents" altogether.
The problem with "agents"
Let's address the elephant in the room: the term "agent" sets the wrong expectations. It conjures images of autonomous assistants bringing you martinis and handling everything independently. The reality is far more nuanced—and far less glamorous.
Spy agents from movies like "James Bond" perform nondeterministic work with potentially catastrophic outcomes. They usually operate with a degree of opacity that can obscure their decision-making process. However, in artificial intelligence, we need transparency, not mystery. That's why, we think they should be called Process Daemons — a term that better captures what they actually are: background processes that execute tasks with oversight and observability.
What is a process daemon (or agent, if you must)?
Strip away the marketing hype, and an agent is surprisingly simple. At its core, it's about 100 lines of code that combines four elements:
- An objective - What needs to be accomplished
- An LLM - The language model that processes and reasons
- Tools - The capabilities the system can invoke
- A response - The output delivered back
That's the foundation. Everything else is infrastructure built around these core components.
How we use process daemons at Digits
At Digits, we've deployed agents for three primary use cases:
Hydrating vendor information - Automatically enriching our data about vendors, reducing manual research time and improving data quality across our platform.
Simplifying client onboarding - Streamlining what used to be a complex, multi-step process into a smoother experience for new clients joining our platform.
Handling complex user questions - Addressing queries that require reasoning across multiple data sources and business logic, providing answers that would otherwise require significant human intervention.
Building production-ready infrastructure
Moving agents from prototype to production requires much more than the basic four components. Here's what we've learned about building the infrastructure:
Language models and frameworks
All major LLM providers now offer models with tool-calling capabilities, and open source alternatives are increasingly viable. We evaluated numerous agent frameworks—LangChain, CrewAI, and others—but found them often too complex with too many dependencies for production environments.
Our approach: Implement the core agent loop ourselves. It's more work upfront, but it gives us control, reduces dependencies, and ensures production readiness.
Agent tools: reuse, don't reinvent
Production environments already have APIs. Rather than manually defining agent tools (too time-consuming) or automatically exposing all RPCs (too noisy), we wanted a curated approach.
Our solution leverages Go's reflection capabilities to dynamically introspect function handlers and generate JSON schemas for inputs and outputs. This gives us the best of both worlds: automated tool generation with curation. Crucially, the existing APIs already handle access rights, so we're not creating new security concerns.
Observability is non-negotiable
Understanding what happens under the hood isn't optional in production. We needed lightweight decision traceability to debug issues and understand agent behavior.
We use OpenTelemetry to integrate with our existing traces, making agent observability part of our broader system monitoring. Prompt comparison capabilities help us understand when changes improve or degrade performance.
Memory vs. storage
Here's a critical distinction: storage isn't memory. True agent memory combines semantic search with relational or graph databases, establishing context across conversations in a fundamentally different way than simple data persistence.
We implement memory as a tool rather than relying on provider-specific memory solutions. This avoids vendor lock-in and gives us flexibility as the landscape evolves.
Guardrails: don't trust your LLM
Use a different LLM to evaluate responses. Simple guardrails can be implemented via LLM assessment, while more complex scenarios benefit from specialized guardrail frameworks. The key principle: never trust a single model to police itself.
Lessons from the trenches
After running agents in production, here are our hard-earned lessons:
Frameworks require scrutiny - Open source frameworks offer great starting points, but evaluate them carefully for production readiness. Often, they're not ready for prime time without significant modification.
Let applications drive infrastructure - Don't build infrastructure in a vacuum. Let real application needs guide your architectural decisions.
Task planning accelerates performance - Using reasoning models to plan tasks upfront achieves faster completion times and higher accuracy with lower latency.
Build for responsibility - Responsible agents require observability, user feedback mechanisms, guardrails, and team notifications when things go wrong. This isn't optional; it's foundational.
Continuous improvement
The work doesn't stop at deployment. We capture user feedback about agent responses, design reward functions, and explore reinforcement learning to fine-tune agent-specific models. Each iteration makes our agents more effective at their specific tasks.
A note on MCP and discovery protocols
You might wonder about the Model Context Protocol (MCP) and other agent-to-agent communication standards. We haven't adopted these yet. For internal data discovery, MCP isn't necessary—we already have that infrastructure. The security scenarios remain unclear, and honestly, much of the current discussion feels more like marketing than practical necessity.
Conclusion
Building AI agents for production is less about dependency-heavy frameworks and more about practical engineering. Focus on the fundamentals: clear objectives, appropriate tooling, comprehensive observability, and robust guardrails. Reuse your existing APIs and infrastructure where possible. Stay vigilant about prompt injection attacks. And perhaps most importantly, set realistic expectations—both internally and with users.
The future of AI in production isn't about magical agents. It's about well-engineered process daemons that reliably execute specific tasks with appropriate oversight and permissions. That might be less exciting than the hype, but it leads to more reliable and predictable systems.
The Digits Engineering Team has over a decade of collective experience deploying machine learning systems across multiple industries.
Want to dive deeper? The full presentation covers implementation details, demos, and specific technical recommendations for each component of a production agent system.
https://drive.google.com/file/d/1cgbQsBlWyO13DnN8jZtYXlByEw_wDbeP/view?usp=drive_link
Stay up to date with Digits
Unsubscribe anytime.
