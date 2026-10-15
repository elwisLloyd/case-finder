# How GitHub’s agentic security principles make our AI agents as secure as possible

Источник: https://github.blog/ai-and-ml/github-copilot/how-githubs-agentic-security-principles-make-our-ai-agents-as-secure-as-possible/

Try out our new agentic products with GitHub Copilot >
We’ve been hard at work over the past few months to build the most usable and enjoyable AI agents for developers. To strike the right balance between usability and security, we’ve put together a set of guidelines to make sure that there’s always a human-in-the-loop element to everything we design.
The more “agentic” an AI product is, the more it can actually do, enabling much richer workflows, but at the cost of a greater risk. With added functionality, there’s a greater chance and a much greater impact of the AI going off its guardrails, losing alignment, or even getting manipulated by a bad actor. Any of these could cause security incidents for our customers.
To make these agents as secure as possible, we’ve built all of our hosted agents to maximize interpretability, minimize autonomy, and reduce anomalous behavior. Let’s dive into our threat model for our hosted agentic products, specifically Copilot coding agent. We’ll also examine how we’ve built security controls to mitigate these threats, and perhaps you’ll be able to apply these principles to your own agents.
Security concerns
When developing agentic features, we are primarily concerned with three classes of risks:
- Data exfiltration
When an agent has Internet access, it could leak data from the context to unintended destinations. The agent may be tricked into sending data from the current repository to an unintended website, either inadvertently or maliciously. Depending on the sensitivity of data, this could result in a severe security incident, such as if an agent leaks a write access GitHub token to a malicious endpoint.
- Impersonation and proper action attribution
When an agent undertakes an action, it may not be clear what permissions it should have or under whose direction it should operate. When someone assigns the Copilot coding agent to an issue, who issued the directive—the person who filed the issue or the person who assigned it to Copilot? And if an incident does occur as a result of something an agent did, how can we ensure proper accountability and traceability for the actions taken by the agent?
- Prompt injection
Agents operate on behalf of the initiating user, so it’s very important to ensure that the initiating user knows what the agent is going to do. Agents are prompted from GitHub Issues, files within a repository, and many other places, so it’s important to ensure that the initiator has a clear picture of all the information guiding it. If not, malicious users could hide directives and trick repository maintainers into running agents with bad directives.
Rules for agentic products
To help prevent the above risks, we have created a set of rules for all of our hosted agentic products to make them more consistent and secure for our users.
- Ensuring all context is visible
Allowing invisible context can allow malicious users to hide directives that maintainers may not be able to see. For example, in the Copilot coding agent, a malicious user may create a GitHub Issue that contains invisible Unicode with prompt injection instructions. If a maintainer assigns Copilot to this issue, this could result in a security incident as the maintainer would not have been aware of these invisible directives.
To prevent this, we display the files from which context is generated and attempt to remove any invisible or masked information via Unicode or HTML tags before passing it to the agent. This ensures that only information that is clearly visible to maintainers is passed to the agent.
- Firewalling the agent
As mentioned previously, having unfettered access to external resources can allow the agent to exfiltrate sensitive information or be prompt-injected by the external resource and lose alignment.
We apply a firewall to the Copilot coding agent to limit its ability to access potentially harmful external resources. This allows users to configure the agent’s network access and block any unwanted connections. To balance security and usability, we automatically allow MCP interactions to bypass the firewall..
In our other agentic experiences like Copilot Chat, we do not automatically execute code. For example, when generating HTML, the output is initially presented as code for preview. A user must manually enable the rich previewing interface, which executes the HTML.
- Limiting access to sensitive information
The easiest way to prevent an agent from exfiltrating sensitive data is… to not give access to it in the first place!
We only give Copilot information that is absolutely necessary for it to function. This means that things like CI secrets and files outside the current repository are not automatically passed to agents. Specific sensitive content, such as the GitHub token for the Copilot coding agent, is revoked once the agent has completed its session.
- Preventing irreversible state changes
AI can and will make mistakes. To prevent these mistakes from having downstream effects that cannot be fixed, we make sure that our agents are not able to initiate any irreversible state changes without a human in the loop.
For example, the Copilot coding agent is only able to create pull requests; it is not able to commit directly to a default branch. Pull requests created by Copilot do not run CI automatically; a human user must validate the code and manually run GitHub Actions. In our Copilot Chat feature, MCP interactions ask for approval before undertaking any tool calls.
- Consistently attributing actions to both initiator and agent
Any agentic interaction initiated by a user is clearly attributed to that user, and any action taken by the agent is clearly attributed to the agent. This ensures a clear chain of responsibility for any actions.
For example, pull requests created by the Copilot coding agent are co-committed by the user who initiated the action. Pull requests are generated using the Copilot identity to make it clear that they were AI-generated.
- Only gathering context from authorized users
We ensure that agents gather context only from authorized users. This means that agents must always operate under the permissions and context granted by the user who initiated the interaction.
The Copilot coding agent can only be assigned to issues by users who have write access to the underlying repository. Plus, as an additional security control, especially for public repositories, it only reads issue comments from users who have write access to the underlying repository.
Try it out now
We built our agentic security principles to be applicable for any new AI products; they’re designed to work with everything from code generation agents to chat functionality. While these design decisions are intended to be invisible and intuitive to end users, we hope this makes our product decisions clearer so you can continue to use GitHub Copilot with confidence. For more information on these security features, check out public documentation for Copilot coding agent.
Tags:
Written by
Related posts
GitHub’s context-aware secret classifier improves detection quality, raises weighted acceptance by 11.5%, and reduces median scan execution time by 86%.
Learn how to add custom instructions and skills to your repository, use custom agents, and connect MCP servers like Playwright.
Developers aren’t becoming more careless; they’re being outpaced. The tools that let developers create more software should also take on more of the work of protecting it.
