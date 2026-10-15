# How we are improving product quality at Coinbase with AI agents

Источник: https://www.coinbase.com/en-it/blog/How-We-are-Improving-Product-Quality-at-Coinbase-with-AI-agents

How we are improving product quality at Coinbase with AI agents
Using AI to 10x testing effort
In 2025, AI agents have experienced rocket-like acceleration. We started questioning how we could leverage this exciting technology to improve product quality at Coinbase. We believe building the financial infrastructure of tomorrow for billions of users requires a stable and robust product experience; users will consistently gravitate towards the most trusted platform over time, and trust is cultivated through upholding the highest bar on quality.
We started with an idea to 10x our testing effort at 1/10 the cost. We believe leaning into AI represents a mindset shift for our organization, enabling us to stay ahead of the competition by embracing the principle of doing more with less. The Quality Assurance AI agent (qa-ai-agent) emerged from this initiative.
Manual testing
First and foremost, qa-ai-agent functions similarly to a traditional QA engineer. It processes testing requests in natural language; for example, a prompt such as "log into coinbase test account in Brazil, and buy 10 BRL worth of BTC" is sufficient to initiate a test. Rather than relying on text-to-code intermediary steps, the agent directly uses visual and textual data from coinbase.com to determine the next logical action to complete the task. To assert test results, it leverages the LLM’s reasoning capabilities to identify issues intelligently. What’s the end result? What used to take a human tester a week to complete, now can be done in minutes.
Test automation
Our test automation strategy centers on eliminating manual testing. We, like many companies, currently have many traditional end-to-end integration tests. However, these tests are prone to flakiness; minor layout adjustments can cause failures that require hours of debugging. The qa-ai-agent eliminates this flakiness thanks to its no-code nature, bringing a huge productivity gain. We've also streamlined the process for users to add new test cases. This means a test will pass as long as the underlying feature is functional and creating new test automation simply involves describing it in natural language, which is significantly faster and easier to maintain than code.
Technical Implementation
qa-ai-agent relies on several critical dependencies that enable its core functionality. At its core, we use an open-source LLM browser agent, browser-use, to enable AI to control a browser session. Our service includes both a set of gRPC endpoints and WebSocket-based connections to start a test run. For data persistence, MongoDB provides the storage backbone for test executions, session history, and issue tracking. Browser automation capabilities are powered by BrowserStack, enabling remote browser testing across different environments.
Evaluating AI Agent Performance
From the project's inception, we've treated AI performance evaluation as a first class citizen. Our guiding principle is that qa-ai-agent should consistently perform at or above the level of our current human testers. To evaluate its performance, we benchmarked qa-ai-agent against human testers using a defined set of key success metrics.
Evaluation framework
- Productivity: Total number of issues identified within a given period
- Correctness: Percentage of identified issues accepted as valid by dev teams
- Scalability: Speed at which new tests can be added
- Cost-effectiveness: Token cost associated with running a test
Comparing to human testers
To assess the performance of our AI agent against human testers, we employed a data-driven A/B testing approach, mirroring our standard feature launch process. Both human testers and our AI agent conducted test runs under identical parameters. Our findings reveal the following:
- Accuracy: 75% (AI) vs. 80% (Manual)
- Efficiency: qa-ai-agent detected 300% more bugs in the same timeframe
- Scalability: New tests can be integrated within 15 minutes if the prompt has already been tested, or approximately 1.5 hour if prompt testing is needed, as opposed to the hours required for training manual testers
- Cost Savings: Our token cost analysis shows an 86% reduction compared to traditional manual testing expenses
It's important to acknowledge that human testers retain an advantage in areas challenging for test automation systems, such as the user onboarding flow, which requires a real human ID and liveness tests (e.g., selfie verification)
LLM as a Judge
An innovation we introduced to improve correctness was leveraging LLMs as a judge to evaluate the quality of identified bugs. Based on the artifacts (screenshot, issue description, etc.), we ask another LLM to evaluate if the issue is genuine or potentially a false positive. A confidence score is then produced, which is later used for filtering out low-confidence issues.
Where we are today and what’s next
Today qa-ai-agent executes 40 test scenarios, encompassing localization, UI/UX, compliance, and functional aspects of the Coinbase product experience. The test execution is fully integrated into the developer's workflow including Slack and JIRA integration. On average, it identifies 10 issues weekly. Up until now we have accumulated two months of test results, which lead to deprecating manual tests that can be entirely supplanted by AI. We anticipate that at least 75% of current manual testing will eventually be replaced by AI agents, a goal we are rapidly approaching.
