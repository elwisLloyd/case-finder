# Improving Security Incident Response at Agoda with Large Language Models

Источник: https://medium.com/agoda-engineering/improving-security-incident-response-at-agoda-with-large-language-models-78b1f33151e0

Featured
Improving Security Incident Response at Agoda with Large Language Models
Agoda operates a global travel platform that serves millions of users and processes sensitive data at scale, including personally identifiable information (PII), payment credentials, and booking histories. With this volume and sensitivity comes a constant stream of security alerts, user reports, and investigations that the Security Incident Response (IR) team must handle efficiently and accurately.
Our infrastructure spans hundreds of microservices, distributed systems, and multiple cloud environments. Maintaining high service availability while responding quickly to potential threats requires a level of operational scale that traditional, manual processes can’t sustain.
To solve this, Agoda’s IR team began exploring the use of large language models (LLMs) to reduce manual overhead and increase response speed. Over time, this evolved into a set of production-ready, AI-powered workflows that assist with alert triage, phishing analysis, and report generation.
This post details the design and deployment of these systems, how they were integrated into existing security operations, and the challenges and outcomes observed since launch.
The Problem
Agoda’s incident response process spans multiple workflows from alert triage to phishing report review to post-incident documentation. As our infrastructure and user base grew, each of these areas started generating more volume than we could comfortably manage with manual processes alone.
- Security alerts required investigation even when the pattern was well understood, adding noise and draining analyst time.
- Phishing reports submitted by employees needed to be acknowledged and reviewed individually, despite most being harmless.
- Incident reports were important for knowledge sharing and compliance, but took hours to compile from scattered sources.
These weren’t fundamentally broken processes, but the repetition, volume, and context switching across tools introduced friction that made it harder to scale effectively.
Rather than automate everything at once, we focused on targeted, high-impact workflows that had clear structure and repeatable patterns. That led to the development of three independent LLM-powered systems integrated at different stages of our incident lifecycle:
- Triage automation for recurring security alerts
- Phishing report classification for user-submitted emails
- Incident report generation for documenting investigation outcomes
Each was built around a specific problem, designed to be easy to measure, and integrated directly into our existing workflows.
Incident Triage: Security Alert Level 1–2 Investigations using LLMs
Security alerts are generated continuously across Agoda’s infrastructure. Many are low- to medium-risk but require careful triage to determine if escalation is needed. Prior to automation, this process involved manually reviewing logs, correlating historical incidents, and writing investigation summaries, each alert taking 20 to 40 minutes to handle.
How the LLM Workflow Works
- Trigger: Alerts enter the system through Agoda’s existing security pipeline.
- Context Collection: The system gathers a timeline of events and metadata related to the alert.
- Historical Reference: A Retrieval-Augmented Generation (RAG) system queries a vector database of past incidents and root cause analyses.
- LLM Inference: The model receives the alert timeline, metadata, and similar past cases. It’s prompted to emulate a seasoned security analyst.
- Output: The model generates a summary, impact assessment, and a verdict.
Since integrating the LLM-based triage system, Agoda’s Security Incident Response team has significantly improved both speed and consistency in handling relatively minor Level 1–2 alerts.
The average analysis time per alert has dropped from 20–40 minutes to under 5 minutes, enabling the team to handle over 400 alerts every 15 days more efficiently. Alerts are automatically enriched with historical context and analyzed using a retrieval-augmented LLM workflow, which reduces the manual effort involved in log review, pattern recognition, and report drafting.
Internal validation over the last three months shows a 97%+ alignment with human analyst conclusions during peer review. The system is tuned to favor over-escalation, minimizing the risk of missed threats. In practice, false positives are quickly reviewed and closed, and no high-impact incidents have been misclassified since rollout.
Beyond performance metrics, the workflow has helped reduce alert fatigue and increase focus on higher-priority investigations. Tasks that previously consumed significant analyst time, like timeline reconstruction and incident comparison, are now handled end-to-end by the LLM, resulting in faster decisions and more consistent triage outcomes.
Automating Phishing Email Analysis with LLMs
We also receive hundreds of user-reported phishing emails each week. These reports are valuable, but fewer than 2% of them turn out to be actual phishing emails. Before automation, each email was reviewed manually by an analyst to determine whether it was malicious, benign, or simply spam.
Get Agoda Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
The manual review process involved reading the email body, analyzing headers, cross-checking against threat intelligence feeds, and then responding to the user with a verdict. While most submissions were safe, each report required time and attention from an analyst, creating operational overhead and delaying feedback to users.
To streamline this, we developed an LLM-powered workflow that automates the entire review process in near real time.
How It Works
- When a phishing report comes in, the email is parsed and enriched with threat intelligence based on its headers and metadata.
- The LLM receives the full content and context and classifies the email as phishing, spam, or safe.
- Based on that verdict, an automated response is sent to the reporter in real time.
This system now runs fully autonomously, 24/7. It classifies emails and responds in under 25 seconds, compared to 2–3 minutes with manual analysis. In production, it has maintained over 99% classification precision, correctly identifying both malicious and benign submissions. Since deployment, there have been no known false negatives, and response queues have been virtually eliminated.
The result is a significant reduction in manual workload and turnaround time, allowing analysts to shift focus to more targeted phishing campaigns or threat patterns that require deeper investigation.
Incident Report Generation:
While triaging alerts and reviewing phishing emails were early targets for LLM automation, another high-friction task quickly stood out: incident reporting.
For every notable security event, the Incident Response team is responsible for producing a detailed report. These documents summarize the timeline of events, affected systems, detection signals, containment actions, root cause, and business impact. They’re essential for knowledge sharing, post-incident reviews, and compliance, but they’re also time-consuming to write.
Gathering the necessary context often meant reviewing Slack conversations, Jira tickets, Confluence pages, Teams meeting transcripts, and email chains, sometimes across multiple teams. Writing a complete report would typically take 5 to 7 hours, much of it spent just consolidating fragmented information.
To streamline this process, the team built another LLM-powered workflow, this time focused on multi-source summarization and structured report drafting.
How It Works
- When an incident is resolved, the workflow collects relevant data associated with the investigation.
- An LLM summarizes the incident timeline, detection signals, impact, and resolution steps in a structured report format.
- A reviewer validates the content and publishes the final version to our internal documentation system.
This approach has reduced report drafting time to under 10 minutes, with another 30 minutes allocated for review. The reports follow a consistent structure, use standard language, and allow faster delivery of post-incident documentation. In production, this system maintains over 95% factual accuracy and is now part of our regular reporting process.
The automation ensures reports are written promptly, use consistent language, and don’t miss important sections, especially in fast-moving incidents where timelines are scattered across tools.
What We’ve Learned
Large Language Models (LLMs) are non-deterministic by nature — meaning the same input can sometimes produce different or even conflicting outputs. To increase confidence in results, it’s often helpful to have one LLM cross-check the response of another. Still, human oversight is crucial, especially when high-stakes decisions are involved.
When the LLM doesn’t have access to full context — such as prior alerts or historical signals — it’s better to over-escalate and route the case for human review rather than rely solely on the model’s limited understanding.
We’ve also found that providing accurate, concise, and well-documented input leads to significantly better outcomes. While models don’t require exhaustive data dumps, the more structured and enriched the input, the stronger and more reliable the analysis.
Conclusions
LLMs coupled with automations are great assistants in the security incident response domain, especially in lean but highly technical teams. They can clearly help lower the repetitive workload, especially in cases where sufficient data is available for the LLM to make decisions and provide correct analysis and responses. Humans will always be required to be in the loop to validate the results and analysis done by LLMs.
LLMs are also very competent at finding outliers and interesting, unique behaviors while going through security incident data and logs. They can help find a needle in the haystack in case of large data, but they are also capable of losing context and getting it wrong when supplied with too much data. The right data and the context are always the key.
