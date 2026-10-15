# Swarm-coding: agentic development with multiple background agents

Источник: https://craft.faire.com/swarm-coding-agentic-development-with-multiple-background-agents-3549adc7460d

Featured
Swarm-coding: agentic development with multiple background agents
How Faire leverages GitHub Copilot’s background agents to accelerate large scale changes and common workflows
Imagine if your codebase could maintain itself. At Faire, our engineers have historically spent countless hours on tedious tasks, like cleaning up expired feature flags or migrating test infrastructure — work that’s essential but time-consuming. Thanks to advances in autonomous AI agents, we’re now able to delegate much of this work to background agents, freeing up our teams to focus on innovation. In this post, we’ll share how we use “swarm-coding” — a method of coordinating multiple AI agents — to dramatically scale our engineering workflows.
Overview
Background agents are remote machines that use agentic development to create code changes autonomously. At Faire, we’re taking advantage of these autonomous background agents by creating tailored agent profiles for our most common workflows. Through autonomous agents, our non-engineering teammates are able to land simple changes to the code that they would otherwise have to delegate to an engineer, reducing the wait time on fixes for lower priority work such as minor bugs. More importantly, it enables parallelization, as we can fire off multiple asynchronous workers, having AI swarm on the tasks while the humans focus on the bigger picture — delivering value to the user.
Recently on The Craft, we blogged about how we were able to build out agent profiles by equipping agentic tools with MCP (Model Context Protocol) servers. Since that blog post was written, many autonomous background agents have been launched (e.g. Jules, Codex, Cursor, GitHub Copilot). Using the same strategies of custom instructions and MCP tooling, background agents can become highly effective at executing common engineering workflows — autonomously.
The impact of background agents
Our adoption of these background agents is in very early stages, but we’re already blown away by the initial metrics. We’ve had GitHub Copilot available to the team for just over a month, and we’ve measured adoption and time saved in the following ways:
- “Copilot users” are anyone who was assigned on a Copilot-authored pull request that was actually merged into the codebase.
- For Copilot users, we compared PR volume for the four weeks before Copilot to the four weeks after adoption.
- When a PR is merged, we ping the assignee on Slack to ask how much time it saved them. Time saved options are No time saved, 5 mins, 15 mins, 30 mins, 1 hour, 2 hours, 4 hours, or A day or more.
The results are:
- 18% of the engineering team are Copilot users (have merged at least one Copilot PR).
- We’ve merged over 500 Copilot pull requests.
- Copilot user’s PR volume rose 25% on average (or, 41% for DX’s TrueThroughput metric).
- Average time saved reported is 39.6 minutes per PR.
It’s exciting to see the impact that background agents can have on our tech debt, particularly by accelerating large scale changes through swarm-coding!
So, what is swarm-coding, and how does it work?
Swarm-coding
In software development, swarming is when multiple engineers (or other team members) work together on a single task, rather than independently on separate tasks. By swarming on a specific task, parallelizing the separate aspect, the team is able to deliver a working product sooner. With background agents, the swarming isn’t done by mobilizing large numbers of your workforce — it’s done by assigning multiple tasks concurrently to the background agents.
As a real example at Faire, the iOS team are migrating their test suites to use Mockolo. With a long list of instructions in a prompt template, and having Cursor find areas of the codebase that still need to be migrated, the team are able to have Copilot swarm on the migration task, parallelizing the work in the background while they continue working on other tasks.
By leveraging MCP tools, we’re able to re-use a prompt template to assign multiple tasks to the background agent in parallel.
GitHub Copilot background agent
GitHub Copilot’s background agent is an autonomous workflow that will generate a pull request when you assign it to a GitHub issue. At Faire, we’ve wired this into our MCP (Model Context Protocol) Servers, allowing us to trigger the agent to work on tasks from many different contexts, such as Slack, Jira, or even Cursor.
We’ve initially focused on GitHub because we’re able to trigger it programmatically, it’s easy to customize, and it meshes nicely with our existing pull request automation.
Case study: expired setting cleanup
At Faire we use a settings framework to control our feature launches. Once settings are configured to release the feature, they become redundant. In some cases, they mask a bunch of dead code, from the legacy behaviour before the feature was enabled.
Faire uses thousands of settings. We use a timestamped expiry system to keep track of all of the settings that should be cleaned up, but it can still be easy to lose track of expired settings, or hard to carve out the time to clean them up when that time could be used to develop new features instead.
A setting’s lifecycle consists of:
- Creating the setting definition
- Writing the code that depends on the setting
- Configuring the setting in production
- Waiting for any metrics to be validated, including A/B experiments
- Removing the setting branches from the code
- Deleting the setting
With agentic development, we can automate the cleanup steps. We just need an agent that can decipher the next steps in the setting’s cleanup process, and delegate to a background agent to actually execute the work.
Fetch the following information:
- The setting's production configuration using fetch_setting_configuration
- The codebase's client references to the setting using find_setting_usages
- All of the codebase's references to the setting using search_github_code
A setting is in the CONFIGURATION_ACTIVE state if it provides more than one
possible value for users. The next step is to roll out the same value of the
setting to all users.
A setting is in the STILL_REFERENCED state if the production configuration
provides precisely one possible value for all users, and the setting is still
referenced in the codebase.
For STILL_REFERENCED, the next step is to deprecate the setting, by removing
any usages of the setting from the codebase, replacing lookups with the
production configuration value of the setting.
A setting is READY_FOR_REMOVAL if it is not referenced in the codebase
(other than the declaration, configuration, and generated files).
The next step is to remove the setting declaration and configuration from
the codebase in either the backend or frontend repo.
Using the functions available to you, fetch the information needed to
determine the setting's cleanup readiness and the next steps to take.
Much like our automated code reviews, we can create assistants for the workflows that have access to the necessary tools. Agentic development takes this one step further, with the agents exposing themselves as tools that other agents can call.
To support swarming on expired settings, we need three tools for a custom assistant:
- ExpiredSettingFinderAgent: An agent that can find expired settings to clean up, and manage allocation of the cleanup tasks.
- SettingCleanupReadinessAgent: An agent that determines the stage of clean up, and generates instructions for the next step.
- GitHub Copilot: A tool for assigning a GitHub issue to copilot to execute the work.
By wrapping these three tools together in a custom assistant, and assigning it to a Slack channel, we’re able to track the tasks, and parallelize the execution of work.
With our Fairey Slackbot leveraging the custom assistant, which in turn accesses other agents as tools, we’re able to schedule messages in the slack channel to throttle the number of tasks tackled by the agent, as well as supporting ad-hoc requests from users that want a specific setting cleaned up.
Improving the GitHub Copilot background agent
GitHub’s background agent is an autonomous workflow that can be invoked by assigning it to GitHub issues. This causes a specialized GitHub action to run in the background, which will put up a placeholder pull request that it incrementally updates with a TODO list and the progress towards it. Eventually, it will consider its changes ready and request review from the user that assigned it to the issue.
Get Luke Bjerring’s stories in your inbox
Join Medium for free to get updates from this writer.
The following sections detail strategies for maximizing the efficacy of the agent.
Custom instructions
By adding custom instructions to .github/copilot-instructions.md, you’re able to tailor the responses to your codebase’s specific style.
We use Yarn for managing our dependencies, not npm, so when talking about
npm packages, always give me instructions and code samples that use Yarn.
Our team uses Jira for tracking items of work.
Our monorepo is managed using Nx.
Custom setup steps
With .github/workflows/copilot-setup-steps.yml you can specify additional Copilot setup steps.
jobs:
copilot-setup-steps:
runs-on: ubuntu-4cpu-16gb # Yarn install seems to run out of disk space
# Clone the repository
permissions:
contents: read
steps:
- uses: actions/checkout@v4
- uses: ./.github/actions/setup-node
env:
NODE_AUTH_TOKEN: ${{ secrets.PRIVATE_NPM_REGISTRY_TOKEN }}
In the above example, we have a shared node setup script which runs yarn install with a token that has access to our private NPM registry, which allows us to install all the dependencies to build and test the changes that copilot is making as it iterates on the instructions it was given.
MCP servers
You can add MCP (Model Context Protocol) servers to your Copilot setup, which extends the capabilities of the agent executing the task.
{
"mcpServers": {
"ts-morph": {
"command": "node",
"type": "local",
"args": ["./scripts/mcp/ts-morph.sh"],
"tools": ["*"]
},
"jira": {
"url": "https://mcp.faire.com/jira",
"type": "sse",
"tools": ["*"],
"headers": {
"Authorization": "Bearer $MCP_API_KEY"
}
}
}
}
The above example shows a couple of MCP servers that can improve Copilot’s capabilities:
- ts-morph: Local shell script that boots up a local stdio ts-morph server, allowing programmatic changes to the codebase such as moving files.
- jira: A remote SSE server which wraps Jira allowing us to fetch the details of a Jira ticket that the agent may be working on.
In practice, we have MCP servers for Notion, Slack, Jira and Buildkite — each of which can be leveraged to provide additional context and state for the agent to use.
Programmatic assignment
By generating GitHub issues and assigning Copilot through GitHub’s API, we’re able to programmatically assign work. This means we can provide a function tool for LLMs to leverage in order to delegate work.
export const AssignIssueToCopilotArgsSchema = z.object({
repo: z
.string()
.describe(
"Name of the repository where the issue should be created, e.g.
'backend', 'frontend'"
),
title: z
.string()
.describe(
"Clear, concise title for the GitHub issue that describes what
needs to be implemented or fixed. Should be actionable and specific."
),
description: z
.string()
.describe(
"Detailed description of the task for the copilot bot to complete.
Include: 1) What needs to be implemented or changed,
2) Specific requirements and acceptance criteria,
3) Any relevant context, constraints, or edge cases,
4) Expected behavior and outcomes.
Be comprehensive - the copilot bot relies entirely on this description
to understand and complete the work."
),
});
export const create_github_issue_for_copilot = {
function: {
name: "create_github_issue_for_copilot",
description:
"Create a new GitHub issue and automatically assign it to the
copilot-swe-agent bot for automated code changes. Use this when you
need to: create a GitHub issue, assign work to copilot, request
automated coding assistance, delegate programming tasks to AI, or
convert requirements into actionable development tickets. The copilot
bot will automatically work on implementing the requested changes.
Examples: 'Create an issue to add a new API endpoint',
'File a bug report for copilot to fix',
'Create a feature request for automated implementation',
'Generate a GitHub issue for code refactoring'.",
parameters: zodToSchema(AssignIssueToCopilotArgsSchema),
},
callback: async (args, context) => {
const { repo, title, description } = args;
const copilot = await getCopilotBot({ repo });
const issueResp = await GithubStore.get().createIssue({
repo,
title,
body: description,
});
const issue_number = issueResp.data.number;
// Assign copilot bot
await assignBotToIssue({
repo,
issue_number,
bot_id: copilot.id,
});
},
};
Assigning issues as an MCP server tool
By defining the function for programmatic assignment, we’re then able to expose it as an MCP server tool that allows other agents to delegate work to Copilot.
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { create_github_issue_for_copilot } from "../chatbot/function/github/create_github_issue_for_copilot";
import { fetch_github_diff } from "../chatbot/function/github/fetch_github_diff";
import { fetch_github_issue } from "../chatbot/function/github/fetch_github_issue";
import { fetch_github_pull_request } from "../chatbot/function/github/fetch_github_pull_request";
import { search_github_code } from "../chatbot/function/github/search_github_code";
import { search_github_pull_requests } from "../chatbot/function/github/search_github_pull_requests";
import { registerTool } from "./registerTool";
const server = new McpServer({
name: "GitHub",
version: "1.0.0",
});
registerTool(server, search_github_code);
registerTool(server, search_github_pull_requests);
registerTool(server, fetch_github_diff);
registerTool(server, fetch_github_issue);
registerTool(server, fetch_github_pull_request);
registerTool(server, create_github_issue_for_copilot);
export const githubMCPServer = server;
Improved pull request automation
In addition to all the changes above, we’ve built automation to implement some changes to the way that Copilot PRs are created that improve the developer flow.
- Require two reviews on PRs authored by Copilot — the assignee’s initial review, plus another human.
- Don’t request review from code owners until the PR has at least one review — avoids prematurely pulling in domain experts.
- Notify the assignee when the build fails on the PR — avoids the PR sitting in a bad state unnoticed.
- Summarize the build failures for Copilot — automatically surfaces problems to Copilot to iterate.
- Mark the PR ready for review when it requests review from the assignee.
- Notify the Slack thread of updates when the issue was created from Fairey (our Slackbot agent).
With the improvements above in place, we saw a big increase in the efficacy of the pull requests Copilot was authoring. Without customizations, we saw most of the pull requests produced were left in a state that was “roughly the right idea,” but had various style guide violations, and failing build and/or tests, requiring a human to bring it up to our quality bar and over the finish line. After implementing the additional instructions, and extra setup steps to be able to install our private dependencies, Copilot’s iteration loop was then able to incorporate the style guide, and actually execute the Nx targets to verify the code compiles and the tests pass.
This means that most of the time, reviews are requested for a pull request that’s actually ready for action. With a more effective background agent, we were ready to throw it at some more interesting workflows.
Lessons learned about swarm-coding
To get the most out of swarm-coding, consider prompt templating, meta-prompting, and state management. Here’s how we use each of these.
Prompt templating
For the task that you want to swarm on, produce a generalized template of the explicit instructions. Have variables in the template for the specifics that will allow the agent to quickly hone in on the relevant files or code, rather than burning context searching the codebase. Below is an abbreviated example of a prompt template for migrating iOS code.
Migrate the mocks from protocol `{protocolName}` from SwiftyMocky to Mockolo using the instructions below.
# INSTRUCTIONS
These are the instructions to migrate mocks of a given protocol from
SwiftyMocky to Mockolo
## Find all usages of the protocol's mock
- List all files in the codebase that are named `*Tests.swift` and
contain `mock.protocolNameInCamelCase`.
## Convert the protocol to Mockolo
- Replace the annotation `// sourcery: AutoMockable` in the protocol
file with `// sourcery: Mockolo`
- Add the annotation `/// @mockable` right below the `// sourcery: Mockolo`
annotation.
- When adding the annotation `/// @mockable`, check if there are any
`Publisher` properties in the protocol being annotated.
# […]
Meta-prompting
Meta-prompting is a technique for iterating on a prompt by prompting an LLM to improve on it. When the outcome isn’t quite what you want, ask an LLM how your instructions could be clearer so that the results are better next time.
For example, let’s say that even though your prompt includes instructions to avoid jest.mock and use your proprietary mockApi utility when stubbing API requests, Copilot still wrote code you didn’t want it to. Below is an example of meta-prompting to iterate on a prompt.
The following prompt caused Copilot to produce a PR which had incorrect test
imports, using jest.mock instead of our preferred utility, mockApi.
Rewrite the following prompt to maximize reliability and understanding by an
LLM coding agent using prompting best practices. Output in simple markdown
format.
[Original prompt]
State management
To swarm effectively, it’s important that any incomplete work is known to the agent (or human!) that is orchestrating the delegation of tasks.
In our experience, the best way to achieve this is using the same ticketing system that your engineers use — at Faire, that’s Jira. Give your agent access to MCP tools that allow it to check whether work is underway. Some examples include:
- Slack tools to search for threads mentioning the work
- Jira tools for searching for issues (e.g. all the tickets under a specific epic)
- GitHub tools for finding open pull requests
As long as you’re consistent about the way that it reports progress and the way that it consumes the progress state, the agent is able to avoid duplicating effort.
It also helps if you set up a regular job that checks on the in-flight work using the same agent. Are there open pull requests that are failing CI, or stuck waiting for a review? Have they been updated within the last day? If not, have the agent ping the owner to make sure they continue to drive progress.
Conclusion
Swarm-coding with background agents represents a powerful leap in developer productivity, enabling engineering teams to tackle large-scale changes and common workflows with unprecedented efficiency and reduced burden. By strategically leveraging these autonomous tools, Faire is paving the way for a future where more complex tasks are automated, freeing engineers to focus on innovation.
Background agents are a highly active work in progress, with contributions from Luke Bjerring, Justin Fangrad, George Jacob, and Blair McAlpine 🙏
Interested in joining a team leveraging agentic programming to serve small businesses around the world? Apply for open roles: https://www.faire.com/careers
