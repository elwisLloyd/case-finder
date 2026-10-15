# (Attempting to) Engineer the chaos out of AI agents

Источник: https://trunk.io/blog/attempting-to-engineer-the-chaos-out-of-ai-agents

Engineers like determinism. After all, predictable outputs make testing and exception handling easier.
Thankfully, LLM outputs are very deterministic, always produce output in a consistent, reliable format, and are never overly verbose. (This is a lie).
We’re building an AI agent to handle DevOps/DevEx tasks in CI and needed to find a way to work with this nondeterminism. We don’t want to build an agent that presents three different solutions to the same problem when run on the same inputs. Our goal was to construct tight, measurable feedback loops so we can move forward and build an agent that doesn’t suck 50% of the time.
After much experimentation, we found that making small adaptations to general software engineering principles was the best way to handle nondeterministic LLM output.
None of this is rocket surgery, but these lessons helped us build an agent that produced better output, more reliable tests so we can make incremental tweaks and measure progress, and, maybe most importantly, keeps us happy and relatively sane.
If you gaze long into an abyss a black box, the abyss black box also gazes into you.
The black box nature of LLMs makes A/B testing difficult. It is best to accept that upfront. Then you can start to focus on the things you can control.
Treat LLMs like an end user who may or may not have read the instructions. Sometimes, they do dumb stuff. This is expected and needs to be handled.
On to the actual lessons.
It is tempting to build an “everything agent”.
An “everything agent” can and will do anything and everything. It might be magic.
It could be run on a single model, with one mega prompt attempting to handle multiple things. With the availability of libraries and toolkits like Vercel’s AI SDK, it can be tempting to just add more tools to the “everything agent” so it can do “everything”. But access to a bunch of tools doesn’t mean the agent will know how to use them properly.
Our advice: don’t build the everything agent from the start. Pick out one or two use cases, and get them working well. This will give you a good feel for writing system prompts, and you’ll have something to put in front of actual users.
Maybe this small agent fails. Maybe output is always unreliable. Maybe it makes too many tool calls. Maybe users don’t find the use case particularly helpful. That’s okay, try something else. If you start small, then you can test for failure right away and pivot if necessary.
At Trunk, we started by focusing on root cause analysis (RCA) for test failures. Our existing Flaky Tests feature stores historical stack traces from test failures in CI, so we already have a rich dataset and existing infrastructure to support this use case. We just (just) needed to add an agent into the stack that examines failures and posts summaries to GitHub PRs.
Even then, we started by focusing on tests that had a relatively simple failure reason. Test failures can range in complexity, and we knew our approach for large code changes would be different from how we diagnose failures for smaller changes.
Real data also exposes your agent to edge cases, so you can see what the LLM does when it is fed unexpected results. (We’re also testing on agent-generated PRs from tools like Claude Code and the Gemini CLI because this is what we expect some future input to look like.)
Secret lesson 1.1: The LLM also doesn’t need to do everything for you. Preprocess data when it makes sense. We group similar failures and remove non-relevant info so we stay within our LLM’s context limit when processing CI logs. Otherwise, a single log can blow the context window, much less historical logs from the last X runs.
Starting small and pivoting fast also relates to the next lesson…
Despite earlier jokes, building a good system prompt is still very important.
You can use existing public system prompts as a guide to get started (especially ones from LLM providers like Claude or the Gemini CLI) and use LLMs to generate a starting point.
But don’t spend too much time on it. At some point, you can only capitalize and bold markdown so many times before you start to go crazy.
If “DO NOT EVER SUGGEST THAT THE USER JUST CLOSE THEIR PR” appears in your prompt, perhaps it is time for a different approach.
Instead, change the model powering your agent.
Tyler, one of our engineers, almost went crazy trying to tweak our main prompt so that Claude would call our tools in a more deterministic manner. Flipping to Gemini solved the problem. Tool calls became more reproducible at the expense of some LLM reasoning.
LLMs are not magical machines that can do anything with the right prompt. Different LLMs excel at different tasks, and it might take some experimentation to figure out which model is best suited to solve your problem.
Big sledgehammers before small chisels.
Use what you are building. Get your team to use it. Get your project manager to use it.
This is the best way to get feedback before putting your agent in front of actual users (but you should do that too).
We use our agent on our main trunk monorepo so everyone is exposed to what we’re building. And just as importantly, we have a feedback form attached to the PR comments left by the agent so devs can leave feedback, both positive and negative.
This exposes the agent to a variety of inputs, keeps the whole team synced on progress being made, and provides valuable feedback so we can investigate exactly what is going on behind the scenes when we produce both good and bad outputs. (We currently use LangSmith for observability of our agent’s inputs, outputs, and tool calls.)
Eating our dog food helps us build confidence that what we’re doing is actually valuable.
Evaluating the output of your LLM is only part of the testing loop.
Set the LLM aside for a minute, it is still important to properly test the rest of your system.
We need to know that the tools we build are properly tested, that we are providing the correct information to the LLM, and that we handle structured LLM output properly.
So validate your inputs, your outputs, and make sure that different test cases are handled by mocking out the LLM like you would any other service when writing unit tests. We use MSW and Vercel’s AI SDK mock tooling to mock the LLM network responses.
This doesn’t mean you shouldn’t run integration and end-to-end tests that call the LLM. These tests provide additional examples of potentially bad output that lead to better error handling. But this shouldn’t be the sole focus of your testing efforts.
In addition to our unit tests, we have integration tests and evals for the entire workflow, providing observability into each step of the agent’s process. This is an important part of our developer experience loop and makes it easier for us to catch regressions and A/B test prompt tweaks.
An infinite number of monkeys hitting keys on an infinite number of typewriters will eventually write the complete works of Shakespeare.
And at any given time, an LLM might write Hamlet in a PR comment. They occasionally output like they are in high school, desperately trying to reach the assignment word limit.
Good user experiences enable users to complete tasks quickly. Good UX is intuitive.
This still applies when working with LLMs. An LLM can output the correct information that helps solve a problem, but it is a failed experience for users if the info is buried in a novel.
But unlike traditional applications and services, you don’t have fine-grain control over the end-user experience when LLMs are producing user-facing output. Your ability to manage the verbosity of outputs will play a big role in the end-user experience of your agents.
Just like you focus on developer usability when building APIs or end-user experience when designing and building frontends, put some effort into the format of your agent’s output.
We have systems in place that try to ensure we consistently produce high-quality, actionable output. If the agent fails to meet deterministic output validation, like surpassing a character limit, we can rerun it. (Provided that reruns are cost-effective and capped at N retries. As prices of LLMs continue to drop, reruns become much more feasible.) Subagents are used to extract relevant, structured outputs, summarize them, and funnel them to the user. We also capture usage metrics and errors at every stage where things could go off the rails, such as tool executions and LLM outputs.
And once again, actual user feedback is also important.
Another consideration: agent output and actions must be helpful and understandable to all end users, which might also include other AI tools.
Once again, these are all things that you should probably be doing whether you are building agents or not. Small tweaks to your development process and the acceptance that sometimes the LLMs are just going to LLM (along with proper error handling) helped us build an agent that is actually useful.
AI tools don’t have to take you from 0 to 1. Going from 0 to 0.5 can still be a massive speed boost for manual and repetitive tasks, even if an actual person still needs to finish the work. It is much better to do small tasks well than large tasks poorly. The ability to consistently “one-shot” a task doesn’t have to be how you measure success. Instead, try to make incremental performance gains on a task and work your way up to full-task automation as LLMs improve and the cost of running high-performance models goes down.
If you’re interested in trying our AI DevOps agent (that handles RCA for flaky tests and CI failure very well), the waitlist is open.
