# How We Built Our SRE Agent using FastMCP

Источник: https://www.fuzzylabs.ai/blog-post/how-we-built-our-sre-agent-using-fastmcp

In modern cloud‑native applications, Site Reliability Engineering (SRE) teams spend a lot of time chasing down the root cause of production incidents—sifting through logs, inspecting Kubernetes services, hunting for error messages, scrolling through source files, and then communicating findings to the wider team. What if an AI agent could shoulder much of that routine work, triaging errors end‑to‑end and even posting diagnostic summaries for you?
This deep dive shows our proof-of-concept autonomous SRE agent, built on Anthropic’s Model Context Protocol (MCP) with FastMCP. We’ll walk through the reasoning cycle, demonstrate the agent handling a simulated incident, and preview the research questions we’re exploring next.
Problem Statement
This project builds on our earlier MCP experiment, a chess-playing agent, and aims at a real-world, fully autonomous application that can diagnose issues in cloud-hosted software.
To create a realistic testbed, we forked Google’s “online boutique” micro-service demo and introduced deliberate application and system errors. The agent’s job is to identify and diagnose those faults and recommend fixes.
Agent Architecture
An MCP-based agent has three tightly coupled layers, mirroring the human nervous system:
Large Language Model (Brain / Cortex) – Thinks, plans, imagines possible next steps, and issues motor commands.
MCP Client (Motor-sensory nerves) – Carries those commands to the periphery and returns sensory feedback, translating high-level intent into concrete MCP calls.
MCP Server(s) (Sense-and-action organs) – The agent’s eyes, ears, vocal cords, and limbs: specialised interfaces (APIs, databases, actuators) that execute commands and generate fresh observations.
In practice, the LLM reasons over its context and decides what should happen next. The MCP client packages those decisions into calls, dispatches them, then feeds results back to the LLM, closing the perception-action loop.
Trigger-to-Diagnosis Flow
The following architecture diagram illustrates the high-level design of an SRE (Site Reliability Engineering) Agent that leverages a large language model (LLM) to automate the diagnosis of issues via Slack.
A Cloudwatch trigger starts the agent (also directly trigger-able via Slack).
The trigger sends a prompt to the MCP client, outlining its responsibility to diagnose issues.
The MCP client and LLM decide which troubleshooting tools to call.
The MCP client invokes tools from MCP servers (Slack, GitHub, Kubernetes) and returns responses to the LLM.
The LLM generates a diagnosis and posts a clear summary back in Slack.
This streamlined architecture enables proactive, intelligent infrastructure monitoring and response with minimal manual intervention.
Key components:
Kubernetes MCP Server (tools: list_pods, get_logs)
GitHub MCP Server (tools: get_file_contents)
Slack MCP Server (tool: slack_post_message)
Building Our Own Client
When developing our Chess Agent, we relied on an AI application like Claude Desktop and Cursor’s implementation of an MCP client to interact with our MCP server for playing chess. Whilst Claude Desktop provided an entry point into developing our own agent, we found that Anthropic would gate-keep token usage making it difficult to perform full agentic workflows. Additionally, these tools required users to accept tool calling on the agents behalf, removing full autonomy from the application.
A key area of exploration as part of this work was to remove the training wheels provided by these AI applications. We wanted to understand what the MCP client in these applications was actually doing and responsible for, if there were any optimisations we could make, as well as tailoring it towards our goal of an autonomous SRE agent. To do this we implemented our own MCP client using FastMCP, making calls directly to an Anthropic LLM through their API. The code for the MCP client we built can be found here.
Under the hood our MCP client does the following:
Initialises an Anthropic Claude client (the brain of the agent)
Discovers available tools (the agents real-world actions trigger-able by the client) via the Model Context Protocol (MCP).
Initiates a reasoning loop where the LLM can decide to call any of the registered tools.
Client components:
As part of our bespoke MCP client we have implemented the following:
Tool caching: given that we are repeatedly making calls to an LLM caching repetitive information like the tools and message history can have a significant impact on cost. We found that implementing this caching reduced our cost per-diagnose by 83%.
Toolfiltering: We used community build MCP servers but we didn’t need all the tools they provided. This not only mitigated a security risk of using tools we don’t need but it also reduced our potential token usage of the LLM (reducing costs).
Enforcedagenttimeout: we enforce a five-minute timeout on the agent where we stop the agents reasoning loop if doesn't terminate in this time period. This stops the agent from getting stuck and continuing unnecessarily.
Stopconditioning: we enforce that the agent stop once it has sent a message to the Slack channel, this stops the agent from continuing its reasoning loop unnecessarily.
Incident Simulation: “Internal Server Error”
Scenario: The cart-service crashes with an HTTP 500.
A user attempting to buy Fuzzy Labs loafers sees the error, which logs a CRITICAL error and triggers the agent to investigate the issue.
Step‑by‑Step
AWS CloudWatch detects the CRITICAL 500 error and alerts the agent.
The alert instructs the agent to investigate the cart-service.
The agent prompt specifies: check the latest 1000 Kubernetes pod logs, scroll for errors referencing a file, fetch that file from GitHub, then report findings to Slack.
The LLM plans its actions, starting with list_pods to locate the cart-service pod.
Next, get_logs retrieves the pod logs.
The LLM analyses the logs and identifies RedisCartStore.cs as the culprit.
It fetches the file from GitHub for additional context and drafts a fix.
Finally, it posts a diagnosis and recommendation in Slack.
Example Slack message
🔍 Cartservice Error Diagnosis
I've identified an issue in the cartservice application. The problem appears to be located in the `RedisCartStore.cs` file.
The error is triggered when users attempt to add a product with ID "AAAAAAAAA4" (loafers) to their cart. The code explicitly throws an exception:
if (productId == "AAAAAAAAA4")
{
await NotifySlackAsync(productId);
CallExternalApiAsync();
throw new Exception("Uh-oh, you tried to buy loafers");
}
Recommendation: If this is intended behavior, consider adding proper error handling and user feedback. Otherwise, remove or modify the conditional check to allow purchasing loafers.
What’s Next?
Our SRE agent is our vehicle to understand the engineering behind Agentic AI and to dive deeper into three key research areas.
Effectiveness: Does the agent actually do what it’s meant to? And how do we measure that in a meaningful way?
Security: How do we put boundaries around what the agent can and can’t do? What might a malicious user try to exploit? If we want the agent to go beyond diagnosis and start fixing issues on its own, how do we manage that safely?
Cost: LLMs are expensive to run, and agentic workflows often use them heavily. Can we make that more efficient? Would running our own models—like Deepseek, LLaMA, or Mistral—be cheaper than using hosted services like Claude or OpenAI? Could a serverless setup bring the cost down even more?
We’ll dig into each of these areas in separate blog posts and link them here once they’re live.
By clicking “Accept”, you agree to the storing of cookies on your device to enhance site navigation, analyze site usage, and assist in our marketing efforts. View our Privacy Policy for more information.
