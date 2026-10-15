# Deep Research in Westlaw and CoCounsel: Building Agents That Research Like Lawyers

Источник: https://medium.com/tr-labs-ml-engineering-blog/deep-research-in-westlaw-and-cocounsel-building-agents-that-research-like-lawyers-508ad5c70e45

Featured
Deep Research in Westlaw and CoCounsel: Building Agents That Research Like Lawyers
Legal research is a skill taught in law school and honed through years of practice. It requires knowing which paths to follow, which authorities carry weight, and when enough support has been gathered to confidently take a position. For decades, Westlaw has been the foundation lawyers rely on to efficiently navigate this complex landscape.
Today, we’re advancing that foundation. Deep Research, an agentic AI system capable of conducting legal research with the sophistication of a practicing attorney, is now live in Westlaw Advantage and CoCounsel. This is not just another RAG (retrieval-augmented generation) tool or search interface, it’s a rethinking of how AI can perform within complex, high-stakes professional workflows.
Why Legal Research Demands Agentic AI
Westlaw’s existing AI-Assisted Research uses large language models (LLMs) to review relevant portions of cases, statutes, regulations, and secondary sources to produce a narrative response. Lawyers consistently tell us these summaries are helpful, but they’re just a starting point. Attorneys then dive deeper in Westlaw to gather more authority, surface edge cases, and resolve nuanced legal questions.
Take, for example, a discrimination claim in New York where the company hired someone of the same race and gender as the rejected applicant. A traditional RAG system might suggest the claim can proceed. But that’s not enough. Lawyers want to understand: How strong is the inference? How does it vary by jurisdiction? What arguments exist on both sides? How have recent statutory changes affected the analysis?
With recent advancements in LLMs, agentic systems can now do this deeper work. Legal research is inherently iterative. Skilled researchers plan their approach, reassess findings along the way, and adapt as new information emerges. It’s more than searching — it’s the orchestration of tools, sources, and legal reasoning to surface what matters most.
To replicate this behavior, agentic systems need to do five key things:
- Plan multi-step strategies from the initial question
- Execute research steps in parallel
- Select the right tool at the right time
- Update approaches based on new findings
- Apply clear stopping criteria (harder than it sounds)
In Deep Research, the system can search, open documents, analyze content, and react in real time. It uses KeyCite warnings to flag questioned or overruled cases. When a case references others, the system follows those breadcrumbs and adjusts its strategy, just as a skilled researcher would.
Three Dials of an Agentic System
We designed Deep Research by tuning three core dials that control the behavior of the system.
The Autonomy Dial
This governs how the agentic system plans, executes, and adapts its research. In Deep Research, we dialed up autonomy significantly. The system generates multi-step research plans and explores alternative theories when its first approach fails. Thomson Reuters attorneys worked closely with our research and engineering teams to iteratively refine the system’s behavior, grounding it in legal research best practices rather than unguided exploration.
The Tools and Context Dial
This controls how agents interact with the environment. We didn’t just give the system access to Westlaw content. We reimagined Westlaw features as modular building blocks for agent-driven research. Just as we’ve designed Westlaw to be intuitive for lawyers, we applied the same design empathy to the tools our agent uses: how information is presented, how errors are handled, and how exploration is guided.
The Memory and Coordination Dial
Get Omar Bari’s stories in your inbox
Join Medium for free to get updates from this writer.
This enables persistence and orchestration across long-running workflows. Instead of one monolithic agent, we orchestrate specialized components, each tuned for a particular document type (case law, statutes, secondary sources). The system maintains memory across the session, tracks explored arguments, relates findings, and integrates parallel research threads into a coherent report. Our most comprehensive analyses take about 10 minutes to complete and verify.
Together, these three dials give Deep Research real research autonomy and produce results that raise the bar for depth, accuracy, and trust.
Engineering the Generation and Verification Loop
Despite major advances, LLMs can still make mistakes. Verification is essential in legal research. As Andrej Karpathy has noted, “the key to AI products is better cooperation between humans and AI.” In Deep Research, the system generates; the lawyer verifies.
We’ve built tools to accelerate this loop. All citations in Deep Research come from authoritative Westlaw sources. The Sources tab presents citations visually, with direct links and highlighted excerpts, mirroring how lawyers already work in Westlaw. The main report includes inline citations, KeyCite flags, and excerpts to support fast verification. Both outputs are tightly integrated with Westlaw’s full research toolkit, allowing seamless transitions from AI-generated insight to human review.
How We Choose and Evaluate Models
Deep Research is model agnostic. We work with multiple frontier model providers and open-source options so we can select the best model for each workflow. At launch, a core part of the system uses Claude 4 for its tool orchestration. We collaborated closely with Anthropic to make this aspect of the system optimally effective. Rigorous model selection and evaluation are performed for each component of the system.
Long-running research tasks are difficult to measure. Auto evaluations help when the rubric is sound. Our editorial staff defines objectives across categories such as completeness and correctness, with dozens of more granular rubrics. We build evaluator models to apply these rubrics at scale, calibrating them to mirror human judgment as closely as possible. As our rubrics evolve, so do our models. And while automated evaluations help guide many intermediate steps, we continue to invest deeply in manual review to ensure quality and trust. It is costly, and we believe it builds the trust this work demands.
Evaluations drive model choice. We test new models early within each task and adopt them only when results improve our metrics. When working with any of these models, we always ensure we meet enterprise privacy and security requirements that have made Thomson Reuters a trusted partner.
Building for What’s Next
The core challenge in legal research remains balancing comprehensive discovery with minimizing noise. Every additional search may uncover a critical precedent or introduce irrelevant results. Legal language is nuanced, and current context window limits make it difficult for models to process extensive documents.
We’ve found a balanced starting point for a best-in-class experience and we’re already testing what’s next. Our roadmap includes:
- Smarter tool design and context navigation
- Multi-agent collaboration with lawyers in the loop
- Integrating firm-specific knowledge and precedent
Creating a flashy demo is easy. Building a system lawyers trust with critical work is much harder. That’s the gap between prototype and professional-grade AI and it’s where Thomson Reuters Labs excels.
💬 Let the Conversation Begin!
Do you have experience in building prototypes using AI? What are your thoughts on using AI for use cases geared towards professionals and what are the challenges you encountered in your AI projects?
Join our community of AI practitioners in our LinkedIn Group to continue the discussion and connect with others who share your passion for pushing the boundaries of AI research and innovation!
We’re hiring. If you’re an engineer or scientist excited about professional-grade agents and transformative legal tech, reach out to the Thomson Reuters Labs team.
