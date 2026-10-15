# Background Coding Agents: Context Engineering (Part 2)

Источник: https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2

Background Coding Agents: Context Engineering (Honk, Part 2)
This is part 2 in our series about Spotify's journey with background coding agents (internal codename: “Honk”) and the future of large-scale software maintenance. See also part 1, part 3, and part 4.
In Part 1, we introduced how Spotify uses a background coding agent to extend Spotify’s Fleet Management system. It can edit code, run builds and tests, and open pull requests (PRs) automatically. Once we had our agents up and running, a new challenge emerged:
👉 How do we tell our background coding agent what to do?
In this post, we explore the craft of context engineering for coding agents. What makes for a good migration prompt? Which tools should the agent have access to? We’ve found that careful context engineering is essential for producing reliable, mergeable pull requests across real-world codebases.
Early open source agents
When we first got started, we experimented with open source agents such as Goose and Aider. When you first use these tools, it’s amazing how far they can get with just a prompt — exploring codebases on disk, identifying what to change, editing code, etc.
But we quickly ran into issues when we tried to scale these agents to our migration use case. It was difficult to get them to reliably produce mergeable PRs. Turns out, writing good prompts — and verifying that the agent did the right thing — becomes significantly more difficult if you want to apply a change over thousands of repos.
Rolling our own agentic loop
Chasing a more predictable agent, we built our own “agentic loop” on top of LLM APIs. Each task was composed of three parts:
- The user provides a prompt and a list of all files in scope.
- The agent takes a few turns editing files based on the prompt, incorporating feedback from the build system with each turn.
- The task is complete once the tests are passed or limits are exceeded (10 turns per session, three session retries total).
This worked well for small changes, for example, editing a deployment manifest, swapping out a config flag, or changing a single line of code. But for anything beyond that, it quickly became unruly.
First, it was hard for users to use this agent. Users had to pick the exact files they wanted to load into the context window by writing a git-grep command. Picking a too-broad search pattern — like git grep -l '*.java' — could easily overwhelm the context window of the LLM. Conversely, picking a too-limited search pattern would not allow the agent to solve the problem because it didn’t have enough context.
The agent also struggled with more complex multi-file changes. For example, we often want cascading changes, such as updating a public method in one file and then adjusting all call sites afterward. For this use case, our loop often ran out of turns. It also tended to get lost when it filled up its context window, forgetting the original task after a few turns.
Enter Claude Code
Our homegrown agentic loop had key challenges — it required overly rigid instructions and struggled with complex, multistep edits. We needed an agent that could interpret high-level goals, manage tasks dynamically, and reduce friction for users who just wanted to describe outcomes rather than dictate every step. We also wanted to avoid running into context window limitations when handling longer or more complex operations.
To solve this, we turned to Claude Code, which allowed us to use more-natural task-oriented prompts, and we benefited from its built-in ability to manage Todo lists and spawn subagents efficiently.
As of today, Claude Code is our top-performing agent, which we’ve applied for about 50 migrations and the majority of the background agent PRs merged into production.
"What Spotify's team has built here is remarkable—not just in the outcomes, but in how they got there. Spotify built a large scale system that used Claude Agent SDK to merge thousands of PRs across hundreds of repositories. Their deep understanding of prompt engineering and context management represents the leading edge of how sophisticated engineering organizations are thinking about autonomous coding. We built Claude Code and the SDK to enable exactly this kind of innovation, and seeing it power their background agent at this scale is incredibly exciting.”
The proof is in the prompt
Here’s the humbling truth: Writing prompts is hard, and most folks don’t have much experience doing it. What seem like simple instructions can lead to hilariously wrong outcomes if you’re not intimately aware of how to prompt your agent. In some ways, writing a prompt for an LLM is like writing clear instructions on how to make a peanut butter and jelly sandwich.
By giving Spotifiers access to our background coding agent without much training or guidance, we are starting to see two major anti-patterns:
- The overly generic prompt that expects the agent to telepathically guess the intent and desired outcome
- The overly specific prompt that tries to cover each and every case but falls apart as soon as the agent encounters something unexpected
But we’ve also seen some teams spend considerable time learning about Claude Code and how to best prompt it. Some of our hard-won lessons:
- Tailor prompts to the agent. Our homegrown agent did best with strict step-by-step prompts. Claude Code does better with prompts that describe the end state and leave room for figuring out how to get there.
- State preconditions. Agents are eager to act on your prompt, to a fault. This becomes problematic if you reuse prompts across repositories in a migration scenario: The agent will get a task that is impossible to achieve — for example, something that is not possible in the language level of the target repository. It helps to clearly state in the prompt when not to take action.
- Use examples. Having a handful of concrete code examples heavily influences the outcome.
- Define the desired end state, ideally in the form of tests. “Make this code better” is not a good prompt. The agent needs a verifiable goal so it can iterate on a solution as it goes.
- Do one change at a time. It can be convenient for users to combine several related changes into one elaborate prompt, but it’s more likely to get the agent in trouble because it will exhaust its context window or it will deliver a partial result.
- Ask the agent for feedback on the prompt. After a session, the agent itself is in a surprisingly good position to tell you what was missing in the prompt. Use that feedback to refine future prompts.
We use these principles to build and run elaborate migration prompts. To give you an idea, here is an example prompt we use to migrate from AutoValue to Java records:
The right tools for the job
As you can see from the example above, our prompts can become fairly elaborate. That’s because we prefer to have larger static prompts, which are easier to reason about. You can version-control the prompts, write tests, and evaluate their performance. This increases the overall predictability of the agent.
An alternative approach is to start with a simpler prompt but connect to Model Context Protocol (MCP) tools that allow the agent to dynamically fetch more context as it works on the problem. While this does make the agent capable of tackling more complex and ambiguous tasks, this also makes it less testable and predictable. The more tools you have, the more dimensions of unpredictability you introduce.
We keep our background coding agent very limited in terms of tools and hooks so it can focus on generating the right code change from a prompt. This limits the information in the agent context and removes sources of unpredictable failures.
At the moment, we give the agent access to:
- A “verify” tool that runs formatters, linters, and tests. We found it easier to encode how to invoke our in-house build systems in an MCP — rather than relying on AGENTS.md-style files) — because our agent needs to operate on thousands of existing repositories with very different build configurations. This also allows us to reduce noise in the tool output by summarizing logs into something more digestible for the agent.
- A Git tool that provides limited and standardized access to Git. This allows us to selectively expose git subcommands (e.g., never push or change origin) and standardize others (e.g., setting the committer and using standardized commit message formats).
- The built-in Bash tool with a strict allowlist of commands. It’s handy to have access to a few Bash commands such as ripgrep.
Notably, we don’t currently have code search or documentation tools exposed to our agent. We instead ask users to condense relevant context into the prompt up front, either by including all relevant information in the prompt before handing it off to the agent, or through separate workflow agents that can produce prompts for the coding agent from various internal and external sources.
We also recommend guiding the agent through the code itself where possible, for example, by setting up tests, linters, or API documentation in target repos. That will work for all prompts (and all agents) operating on this code moving forward.
Conclusion
We continue to explore state-of-the-art capabilities for our background coding agent. Our work with Claude Code carries great potential and unlocked a big step forward as we learned how to instruct the agent and build effective tools. Breaking down tasks into the right chunks, writing good prompts, and better integrating tools with our infrastructure are crucial for producing clean PRs.
But in practice, we are still flying mostly by intuition. Our prompts evolve by trial and error. We don’t yet have structured ways to evaluate which prompts or models perform best. And even if we make it to a merged PR, how do we know if it actually solved the original problem? Stay tuned for our next post on using feedback loops to achieve more predictable results.
