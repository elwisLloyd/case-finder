# How To Build Agents Users Can Trust

Источник: https://builders.ramp.com/post/how-to-build-agents-users-can-trust

We recently prototyped, built, and shipped a suite of LLM-backed agents to further automate expense management on Ramp. While LLMs have improved significantly since ChatGPT first came out, it still takes some finesse to tame them. This is especially true for a finance product where it’s very easy to lose trust through low-quality or unexpected outputs.
In this article, we discuss how we optimized our suite of agents to deliver real business value, clearly explain their reasoning, recognize their own limitations, defer to human judgment, and ultimately build trust.
LLMs are best applied when your problem fits the following:
Fortunately for us, finance is full of problems like that:
These all manifest as tedious time sinks for users with low chance of catastrophic failure, making great targets for LLMs with the proper guardrails.
To illustrate our approach, we'll focus on approving expenses. This has traditionally been a manager's responsibility but we’re now applying a “policy agent” that finance teams can trust to match or exceed human judgment. Since enabling the policy agent at Ramp, we’ve seen more than 65% of approvals be fully handled by the agent.
How you communicate an LLM’s reasoning can matter even more than the accuracy of the final decision. For example, we've found that deferring to users when lacking certainty builds both user trust and system reliability.
Every decision needs a "why." It’s not enough to tell users "You should approve this expense.” This helps users verify the outcome, spot errors quickly, and understand how your LLM thinks.
This last point is also important to both developers and users:
LLM reasoning on its own can be flawed or filled with hallucinations. All facts and figures should be grounded in easily verifiable context coming from your product or the user.
For example, the policy agent links directly to sections of the user’s expense policy that its reasoning references.
Putting this together, here’s an example of how we present the reasoning and citations of the policy agent to users:
This first bullet point is output from an LLM explaining why the expense was approved. The info icon links directly to the section in the user’s expense policy describing the requirements.
Not every question has an answer. Forcing your LLM to come up with one and act on it is a recipe for hallucinations.
Early on, we gave our LLMs the ability to say “I’m not sure” and explain why. When the agent isn’t sure, we fall back to the pre-agent escalation process users are accustomed to. We can then use that explanation to:
It’s important that unsure doesn’t look like an error state in your product. Not only is it a valid outcome, sometimes it’s the ideal result given the information at hand. We’ve seen LLMs practicing humility be a very strong force for building user trust.
This receipt for golfing was accidentally submitted under the wrong transaction, and the agent was able to explain that because of the built in escape hatch.
Asking LLMs to output confidence scores is like asking a human to give a number off the top of their head. It’s usually reasonable, but not numerically relevant and certainly not reproducible. This can be especially misleading because:
Instead, we use predefined categories which are not only easier to explain but also more accurate:
This forces the model to bucket uncertainty into actionable states: users don't need a confidence score, they need to know what action to take.
Most consumer LLM systems treat context as a fixed input that’s defined once and rarely revisited. However, we've found that the most effective approach is to make context collaborative, allowing users to actively shape and refine it alongside the AI.
After many iterations, we found three factors to create context improvements over time:
Applying this to our product, we:
This feedback loop not only reduces the amount of work humans need to do over time, but also improves policy accuracy. After all, if an LLM is getting tripped up on an ambiguous part of the policy, it’s likely a human would be just as confused.
Our in-house expense policy editor. Each section is used directly for policy decision by the LLM depending on how relevant it is to the expense on hand.
Every customer will have a different level of comfort letting AI act on their behalf. When giving your systems agency it’s important you’re not removing agency from your users.
Our solution was to reuse the workflow builder that’s already used across the product to customize and define processes. That same workflow builder defines exactly where and when agents can act.
The autonomy slider works both ways. Users can greenlight agents AND set hard stops. Not everything needs to be an LLM decision. We layer deterministic rules on top: dollar limits, vendor blocklists, category restrictions. These guardrails aren't just safety nets, they're how users tell the agent "I'll never be comfortable with you touching this.”
The more conservative end of the autonomy slider, requiring human review on every expense above $50.
The more trusting end of the autonomy slider, only requiring human review when the agent thinks the expense is suspect. This is the policy we often reach for at Ramp.
The earliest AI IDEs started with inline edit suggestions before moving to full agentic behavior. Similarly, we started with suggesting actions to humans before moving to taking those actions autonomously.
This builds confidence. Users learned the agent's patterns, caught its mistakes, and most importantly saw it getting things right. Only after proving itself as a copilot did we let customers promote the agent to take real action.
The progression is deliberate: suggestions → acting on subsets → full autonomy. Each step validates the previous one, creating a natural trust curve that matches each customer's level of comfort.
Just as unit tests are needed to responsibly evolve a traditional application over time, evals are needed to responsibly evolve your LLM systems over time. We’re continuously improving our process for evals, but some of the lessons we’ve learned so far are:
Expanding on that last point, we’ve found that finance teams are nicer than you might expect: they’re frequently lenient and will approve reasonable but not totally in-policy expenses. If we always took the user’s action as the ground truth , the LLM could have been too lenient.
To address this, we created several golden datasets, each carefully reviewed by our team to define the correct decision based solely on information available within our system. This enables us to make more objective judgments, free from the affinity bias that can influence finance teams' decisions.
We’re committed to building LLM-powered agents that create value while staying trustworthy. The principles that we follow are anchored in:
We're incredibly excited about the future of agents at Ramp. With the right context and collaboration from our users, we believe these agents can deliver a huge amount of economically valuable work and transform how finance teams operate.
