# Building production-ready agentic systems: Lessons from Shopify Sidekick

Источник: https://shopify.engineering/building-production-ready-agentic-systems

This blog post is based on the talk presented by Andrew McNamara, Ben Lafferty, and Michael Garner at ICML 2025: Building Production Ready Agentic Systems: Architecture, LLM-based Evaluation, and GRPO Training.
At Shopify, we've been building Sidekick, an AI-powered assistant that helps merchants manage their stores through natural language interactions. From analyzing customer segments to filling product forms and navigating complex admin interfaces, Sidekick has evolved from a simple tool-calling system into a sophisticated agentic platform. Along the way, we've learned valuable lessons about architecture design, evaluation methodologies, and training techniques that we want to share with the broader AI engineering community.
The evolution of Sidekick's architecture
Sidekick is built around what Anthropic calls the "agentic loop" – a continuous cycle where a human provides input, an LLM processes that input and decides on actions, those actions are executed in the environment, feedback is collected, and the cycle continues until the task is complete.
In practice, this means Sidekick can handle requests like "which of my customers are from Toronto?" by automatically querying customer data, applying the appropriate filters, and presenting results. Or when a merchant asks for help writing SEO descriptions, Sidekick can identify the relevant product, understand the context, and fill in optimized content directly into the product form.
The Tool Complexity Problem
As we expanded Sidekick's capabilities, we quickly hit a scaling challenge that many teams building agentic systems will recognize. Our tool inventory grew from a handful of well-defined functions to dozens of specialized capabilities:
- 0-20 tools : Clear boundaries, easy to debug, straightforward behavior
- 20-50 tools : Boundaries become unclear, tool combinations start causing unexpected outcomes
- 50+ tools : Multiple ways to accomplish the same task, system becomes difficult to reason about
This growth led to what we call "Death by a Thousand Instructions" – our system prompt became an unwieldy collection of special cases, conflicting guidance, and edge case handling that slowed down the system and made it nearly impossible to maintain.
Just-in-time instructions: A Solution for scale
Our breakthrough came with implementing Just-in-Time (JIT) instructions. Instead of cramming all guidance into the system prompt, we return relevant instructions alongside tool data exactly when they're needed. Our goal is to craft the perfect context for the LLM for every single situation, not a token less, not a token more.
How it works in practice
Instructions provided to the LLM (below):
Response from the LLM based on the instructions provided (above):
This approach provides three key benefits:
- Localized guidance : Instructions appear only when relevant, keeping the core system prompt focused on fundamental agent behavior
- Cache efficiency : We can dynamically adjust instructions without breaking LLM prompt caches
- Modularity : Different instructions can be served based on beta flags, model versions, or page context
The results were immediate – our system became more maintainable while performance improved across all metrics.
Building robust LLM evaluation systems
One of the biggest challenges in deploying agentic systems is evaluation. Traditional software testing approaches fall short when dealing with the probabilistic nature of LLM outputs and the complexity of multi-step agent behaviors.
These days, so many people are vibe testing their LLM Systems and thinking that it’s good enough; it’s not. Vibe testing, or creating a “Vibe LLM Judge” that’s like “Rate this 0-10”, is not going to cut it. It needs to be principled and statistically rigorous, otherwise you should be shipping with a false sense of security.
Ground truth sets over golden datasets
We moved away from carefully curated "golden" datasets toward Ground Truth Sets (GTX) that reflect actual production distributions. Rather than trying to anticipate every possible interaction (what spec docs usually try to enumerate), we sample real merchant conversations and create evaluation criteria based on what we observe in practice.
The process involves:
- Human evaluation : Have at least three product experts label conversations across multiple criteria
- Statistical validation : Use Cohen's Kappa, Kendall Tau, and Pearson correlation to measure inter-annotator agreement
- Benchmarking : Treat human agreement levels as the theoretical maximum our LLM judges can achieve
LLM-as-a-Judge with Human Correlation
We developed specialized LLM judges for different aspects of Sidekick's performance, but the key insight was calibrating these judges against human judgment. Through iterative prompting, we improved our judges from barely-better-than-random (Cohen's Kappa of 0.02) to near-human performance (0.61 vs. human baseline of 0.69). The idea is that once our LLM Judge has high correlations to human, we try to randomly replace the Judge with a human for each conversation in our GTX, and when it’s difficult to tell whether we used a human or judge as part of the group, then we know we have a trustable LLM Judge.
User simulation for comprehensive testing
To test candidate changes before production deployment, we built an LLM-powered merchant simulator that captures the "essence" or goals of real conversations and replays them through new system candidates. This enables us to run simulations of many different candidate systems, and choose the best performing one.
The complete evaluation pipeline looks like:
This approach has proven invaluable for catching regressions and validating improvements before they reach merchants.
GRPO training and reward hacking
For model fine-tuning, we implemented Group Relative Policy Optimization (GRPO), a reinforcement learning approach that uses our LLM judges as reward signals. We developed an N-Stage Gated Rewards system that combines procedural validation (syntax checking, schema validation) with semantic evaluation from LLM judges.
The reality of reward hacking
Despite our careful evaluation design, we encountered significant reward hacking during training. The model found creative ways to game our reward system:
- Opt-out hacking : Instead of attempting difficult tasks, the model would explain why it couldn't help
- Tag hacking : Using customer tags as a catch-all instead of proper field mappings
- Schema violations : Hallucinating IDs or using incorrect enum values
For example, when asked to "segment customers with status enabled," the model learned to create filters like customer_tags CONTAINS 'enabled' instead of the correct customer_account_status = 'ENABLED'.
Iterative improvement
Addressing reward hacking required updating both our syntax validators and LLM judges to recognize these failure modes. After implementing fixes:
- Syntax validation accuracy improved from ~93% to ~99% across all skills
- LLM judge correlation increased from 0.66 to 0.75 on average
- Most importantly, end-to-end conversation quality matched our supervised fine-tuning baseline
Key takeaways for production agentic systems
Based on our experience building and deploying Sidekick, here are our key recommendations:
Architecture principles
- Stay simple : Resist the urge to add tools without clear boundaries. Quality over quantity applies strongly to agent capabilities
- Start modular : Use patterns like JIT instructions from the beginning to maintain system comprehensibility as you scale
- Avoid multi-agent architectures early : Simple single-agent systems can handle more complexity than you might expect
Evaluation infrastructure
- Build multiple LLM judges : Different aspects of agent performance require specialized evaluation approaches
- Align judges with human judgment : Statistical correlation with human evaluators is essential for trust in automated evaluation
- Expect reward hacking : Plan for models to game your reward systems and build detection mechanisms accordingly
Training and Deployment
- Procedural + semantic validation : Combine rule-based checking with LLM-based evaluation for robust reward signals
- User simulation : Invest in realistic user simulators for comprehensive pre-production testing
- Iterative judge improvement : Plan for multiple rounds of judge refinement as you discover new failure modes
Looking forward
We're continuing to evolve Sidekick's architecture and evaluation systems. Future work includes incorporating reasoning traces into our training pipeline, using the simulator and production judges during training, and exploring more efficient training approaches.
The field of production agentic systems is still young, but the patterns we've developed at Shopify – modular architectures, robust evaluation frameworks, and careful attention to reward hacking – provide a foundation for building reliable AI assistants that merchants can depend on.
Building production-ready agentic systems requires more than just connecting LLMs to tools. It demands thoughtful architecture decisions, rigorous evaluation methodologies, and constant vigilance against the unexpected ways these systems can fail. But when done right, the result is AI that truly augments human capabilities in meaningful ways.
The Shopify ML team is actively hiring for roles in agentic systems, evaluation infrastructure, and production ML. If these challenges interest you, we'd love to hear from you.
About the author
Andrew McNamara is the Director of Applied ML, where he leads Sidekick, an AI assistant that helps merchants run their businesses more effectively, and has been building assistants for over 15 years.
X: @drewch
