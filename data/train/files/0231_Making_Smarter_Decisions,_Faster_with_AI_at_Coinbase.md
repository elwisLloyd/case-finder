# Making Smarter Decisions, Faster with AI at Coinbase

Источник: https://www.coinbase.com/en-it/blog/making-smarter-decisions-faster-with-AI-at-Coinbase

Making Smarter Decisions, Faster with AI at Coinbase
TL;DR: An inside look at the AI-powered tool built to enhance the RAPID decision-making framework at Coinbase.
At Coinbase, our mission to increase economic freedom around the world demands that we operate at the cutting edge of technology—not just in our products but in our core business operations. We are pioneering the use of advanced AI to build a more intelligent and resilient organization.
While the established RAPID (Recommender, Agree, Perform, Input, Decider) decision framework provides a solid structure for accountable decision-making, we recognized an opportunity to augment it with sophisticated AI. At Coinbase, we use RAPIDs for making critical decisions where inputs are taken from key stakeholders across functions and an accountable “decider” makes the final decision based on these insights.
Here’s the format of a RAPID:
- Date of Recommendation
- Date of Decision: (Ideally within a week of the Recommendation)
Recommendation: (what the Recommender thinks the outcome should be). This includes details behind the recommendation, pros and cons, risks and benefits.
- Recommend: Name of Person A
- Agree (or Disagree): Name of Person B
- Perform: Other employees who are involved
- Input: Other employees who are involved
- Decide: Name of Person C
Each of the named persons has the opportunity to put their own Agree or Disagree in, with their additional context.
The goal of using AI for RAPIDs was not simply to optimize a process but to engineer a system that could systematically surface unseen risks, mitigate cognitive bias, and provide a transparent, auditable layer of analysis for our most critical choices. What was created is a system called “RAPID-D,” an internal, AI-powered decision support tool designed to augment our RAPID framework.
How RAPID-D Works: Under the Hood
RAPID-D isn’t a monolithic AI that provides a single, black-box answer. It's a modular, multi-agent system where specialized agents collaborate, debate, and synthesize information, mirroring a team of expert advisors.
Agents: Specialized Decision Collaborators
- Single Shot Recommender Agent (The Analyst): This agent first performs a thorough, impartial review of the primary RAPID document, i.e. the document that uses the RAPID framework to outline roles and responsibilities for a project or decision. The agent generates a baseline recommendation based strictly on the facts and arguments presented in the document..
- Contextual Recommender Agent (The Seeker): This agent intelligently probes the decision by first generating critical questions about the RAPID document. It then leverages our enterprise search tool to find answers across all internal knowledge sources. By synthesizing these findings, it provides a deeply informed decision with wider organizational context that might otherwise be missed.
- Contrarian Agent (The Devil's Advocate): This is where we directly combat bias. This agent’s sole purpose is to build the strongest possible case against the initial recommendation. It deliberately probes for weaknesses, unstated assumptions, potential risks, and unintended consequences.
- Debate and Decide Agent (The Synthesizer): The final agent acts as an impartial moderator. It meticulously evaluates the arguments from the Analyst, the broader context from the Seeker, and the challenges from the Devil's Advocate. It then produces a comprehensive final recommendation for the human Decider, complete with a detailed explanation of its reasoning and the trade-offs it considered
Tools: Enabling Informed Decisions
Document Context retrieval: This contains the key question generator block which examines each decision document and formulates targeted questions around critical areas like security, market impact, cost, user experience, and scalability. For every question, it retrieves relevant information by searching Coinbase’s enterprise knowledge base. This process helps ensure recommendations are comprehensive, less biased, and tailored to the specific context of each strategic decision
Rapid-D Assistant Architecture
This structured, multi-step pipeline ensures a rigorous examination of the facts and trade-offs. More importantly, it makes the entire decision-making process transparent, consistent, and reproducible.
Journey Behind the Scenes
We developed RAPID-D through a deliberate, iterative process focused on user feedback from our own leaders.
- We started with a single agent that analyzed a RAPID document and presented its reasoning. Early feedback was gathered manually, helping us understand what Deciders valued most.
- The current version is a far more dynamic and interactive experience. It incorporates the multi-agent debate and provides deeper explainability for the AI’s conclusions. We also implemented an asynchronous architecture, ensuring that for complex decisions requiring more time, users are kept informed and receive a well-reasoned output without unnecessary delays.
Evaluating Accuracy
We measured RAPID‑D Assistant’s accuracy through a human review process, comparing each of its final recommendations against the real decisions documented by Coinbase’s RAPID Deciders. This yielded the following benchmark scores across leading models:
Claude 3.7 Sonnet was ultimately chosen for its strong balance of quality, stability, and reliability.
RAPID‑D assistant is built to adapt in real time by incorporating feedback directly into its decision process. Comments or corrections — whether provided by the user during an active session or later by any stakeholder in the RAPID document — are captured and analyzed against the assistant’s original recommendation. This evaluation is then used to optimize subsequent recommendations within the same decision flow, ensuring the Assistant’s output reflects the most up‑to‑date perspectives and context from all participants.
Conclusion: A Commitment to an AI-Native Future
RAPID-D is a powerful example of our philosophy on applied AI. It is not designed to replace human oversight but to augment it with a scalable, AI-driven diligence engine. By providing a clear, well-reasoned, and transparent analysis.
This system is more than an internal tool; it is a reflection of our commitment to building a more robust and intelligent organization.
