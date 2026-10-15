# Dead Ends or Data Goldmines? Investment Insights from Two Years of AI-Powered Postmortem Analysis

Источник: https://engineering.zalando.com/posts/2025/09/dead-ends-or-data-goldmines-ai-powered-postmortem-analysis.html

TL;DR: We adopted LLMs as an intelligent SRE assistant to analyze thousands of postmortems, transforming them from "dead ends" into "data goldmines." This solution automates the identification of recurring incident patterns, particularly in our datastores: Postgres, AWS DynamoDB, AWS ElastiCache, AWS S3 and Elasticsearch. While AI effectively speeds up analysis, uncovers hidden hotspots and investment opportunities, human curation remains crucial for accuracy, fostering trust, and addressing limitations like hallucinations and surface attribution errors. Despite this, we acknowledge the significant potential of AI with SRE that empowers engineering teams with this capability to facilitate rapid decision making.
Introduction¶
At Zalando, a group of colleagues is looking after the datastores in our Tech Radar, wanted to explore:
“What if every system outage could make our entire infrastructure smarter?”
Going forward, we took a Site Reliability Engineering (SRE) perspective to determine valuable learning from failures and postmortems. For us a critical aspect of SRE is the feedback loop where systems, teams, and investments evolve. So far, our traditional approach to the feedback loop is human-centric analysis about incident effects, the root cause analysis (RCA), and the corrective measures implemented to prevent future occurrences. This is a solid technique for immediate reactive learning but it does not work well for retrospective analysis of years of past incident reports at the company scale.
With the rise of Large Language Models (LLMs), we saw an opportunity. Could LLMs detect patterns, surface systemic issues, and even suggest preventive actions all by analyzing our postmortems at scale? Is it possible to transform past learnings into dynamically evolving datasets? We decided to validate this hypothesis specifically for datastore technologies, prior to scaling this approach further.
We adopted LLMs as intelligent postmortem review assistants. What began as a time-saving experiment quickly evolved into a valuable source of strategic insights. This post shares what we learned:
- How to turn postmortems into predictive signals for the reliable future;
- How to tweak AI to read between the lines, supporting decision makers;
- Practical tips about the automation of postmortem analysis.
Our experience suggests that the discussed automation is more than a productivity hack, even as we continue to fully adopt and leverage its benefits. It is a strategic lever for engineering teams.
The Traditional Postmortem Problem¶
Many companies have inherited the postmortem culture from Google’s Site Reliability Engineering book, described in the chapter “Postmortem Culture: Learning from Failure”. The postmortem culture at Zalando is highly similar. Having mitigated factors negatively affecting business operations, the team in charge of the incident starts with the root cause analysis and implementation of preventive actions. The review involves not just the directly responsible teams for the affected applications, but also stakeholders and adjacent teams. The incident is closed only when engineering leadership (up to VP Engineering depending on impact and severity) agrees on sufficient progress in implementation of preventive actions and signs off on the postmortem. Insights from these incidents are shared bottom-up through weekly operational reviews, and horizontally through engineering communities. This transforms each incident into a company-wide learning opportunity. Over time, we’ve accumulated a rich internal dataset: thousands of archived postmortem documents – a gold mine of technical and organizational knowledge.
Even with this culture of learning, there are limitations:
- Postmortems vary widely in depth and clarity. Comparing them and extracting patterns is often perceived as apples-to-oranges;
- Root cause analyses reflect team assumptions, subtle contributing factors often go unspoken;
- Making connections between incidents across teams requires immense cognitive load and informal networking. Taking an overarching company-level perspective still requires the goodwill of individuals and effective networking.
When your learning about site reliability depends exclusively on human effort, scale becomes the enemy. It takes about 15-20 minutes to thoughtfully read a single postmortem (a dedicated reviewer can process maybe four postmortems per hour assuming a continuous focus). Now multiply that by thousands of postmortems. Suddenly, strategic questions like “Why datastores fail most frequently at scale?” become impossible to answer quickly, or without excessive cognitive load. Even for a finite datastore area, it was a substantial time investment for us.
As a result, we risk:
- Missing systemic signals that could inform infrastructure investments;
- Reacting to symptoms instead of addressing root causes;
- Delaying decisions due to insufficient insights across domains.
This bottleneck in capacity led us to a clear conclusion: to get strategic value from our postmortem corpus, we needed speed and effectiveness. Specifically, we needed AI tools capable of reading, interpreting, and synthesizing text at scale.
Our hypothesis was simple: LLMs could turn a mountain of human-authored documents into a dynamic, decision-making dataset. The results, as we’ll explore next, proved even more promising than we expected. It solved for us cognitive load by reducing the information context and detected patterns across large postmortem corpus quickly.
Deploying AI: Automating Postmortem Analysis¶
Our focus was exclusively on our datastores Postgres, AWS DynamoDB, AWS S3, AWS ElastiCache and Elasticsearch. For each of them, we have a question “Why does the datastore fail repeatedly at scale?” and desire to get an instant answer. Google's NotebookLM was a natural choice as a toolbox for making the postmortem analysis. It was very effective for making a short summary from thousands of documents. Notebooks have boosted productivity three times, reading the summary and making a conclusion about root causes requires about 5 minutes. It is still slow at our scale – sifting through summaries takes weeks for a dedicated team of experts, still not allowing us to answer questions quickly. We have also observed severe hallucinations and loss of the incident context by LLM while producing summaries. It has required extra attention during the analysis, the excessive cognitive load has not been reduced for reviewers resulting in loss of effective productivity. All these factors led us to the decision that a sophisticated postmortem processing pipeline is required. We set out to build an AI-powered system to scale this cognitive task, not just automate it.
To solve this, we designed a multi-stage LLM pipeline instead of using high-end LLMs with large context windows. It is a deliberate design trade-off aimed at simplicity and reliability. While large context windows allow models to process more information, we observed a "lost in the middle" effect, where details in the middle of long inputs are often overlooked or distorted. In addition, large contexts do not guarantee perfect recall and can increase latency, memory usage, and cost. Our pipeline is a chain of a few models, where each stage strictly specialises on a single objective.
| Stage | Goals | Input | Output | 
|---|---|---|---|
| Summarization | Reduces reviewer load by condensing postmortem narratives into few data points. | Postmortem corpus | Summary corpus | 
| Classification | Enables technology-specific clustering across incidents. | Identity of technology buckets; Summary corpus | N-buckets, each containing postmortem summaries relevant to the technology | 
| Analyzer | Converts summaries into thematic failure fingerprints. | The bucket of summaries | The bucket of digests, each describing the role of technology in the incident, max 5 sentences. | 
| Patterns | Detects systemic issues over time. | The bucket of digests | The one pager report about the role of technology in all incidents over the time frame, patterns of technology incidents. | 
| Opportunity |  | Patterns of technology incidents; Postmortem corpus | Investment opportunity | 
Eventually, the pipeline sifts through high-entropy information and distill it into concise reasons for failure. A functional pattern “map-fold” is a key building block for the pipeline. A large set of documents is independently processed using a language model to extract relevant information (the "map" phase). These outputs are then aggregated either by another LLM invocation or a deterministic function into a higher-level summary (the "reduce" or "fold" phase). This modular design supports composable tasks like summarization, classification, or knowledge extraction. Pipeline’s input is thousands of postmortem documents, the output is a one-pager describing the trends and patterns for incidents in the focus. We have leveraged human expertise for each stage, involving examinations, labelling and quality control to address accuracy requirements.
Summarization¶
The stage is designed to distill “complex” incident reports into clear summaries. This step, designed for both humans and machines, ensures that stakeholders can quickly and accurately understand the critical aspects of each incident without sifting through large contexts.
Using a tightly scoped prompt, we have used Turn, Expression, Level of Details, Role (TELeR) techniques for prompt engineering, LLM processes each postmortem document and extracts only the most essential information across five core dimensions:
- Issue Summary - A brief overview of what happened;
- Root Causes - Clear identification of the underlying technical or procedural factors;
- Impact - A factual description of what systems, services, or users were affected and how;
- Resolution - The steps taken to resolve the incident;
- Preventive Actions - Planned or implemented measures to prevent recurrence.
The entire process is governed by strict constraints: no guessing, no assumptions, and no speculative content. If something in the original postmortem is unclear or missing, the summary explicitly states that. This ensures the final output remains accurate, focused and trusted with high-level confidence. Additionally, noise such as speculation, redundant phrasing, or tangential commentary is deliberately removed. What's preserved are the key technical and operational insights—delivered in a readable, structured format. This makes the output especially valuable for engineering leadership, reliability teams, and cross-functional reviews.
Below is the censored example of the summary produced by LLMs:
Issue Summary:
On [DATE], between [TIME] and [TIME], a library update deployment
caused a [DURATION] SEV2 incident affecting multiple services.
The deployment upgraded AWS SDK from version 2.20.162 to 2.30.20,
which led to a 5xx error spike and degraded functionality across
[PAGE A], [PAGE B], [PAGE C], and [PAGE D].
Root Causes:
The primary root cause was a missing [CLASS] dependency resulting
from version mismatch between the upgraded AWS SDK (2.30.20)
and the commons [LIBRARY]... Secondary causes included insufficient
integration testing that would have caught the DynamoDB connection
issues and incomplete deployment practices where PRs accumulated
before being fully rolled out.
Impact:
- Customers: [NUM_CUSTOMERS] received inaccurate [PAGE A];
  [NUM_CUSTOMERS] customers unable to view [PAGE B];
  customers experienced non-personalized [PAGE C];
  and unavailable [PAGE D]
- Business: Approximately [GMV] loss
- Markets: All [PAGE B] [MARKETS]
- Partners: [PAGE D] unavailable during incident
Resolution:
The incident was resolved by reverting the faulty deployment.
Detection occurred through P5 alert at [TIME] followed by
P3 alert at [TIME] (high 5xx errors). Root cause was identified
at [TIME], revert initiated at [TIME], and full recovery by [TIME].
Preventive Actions:
- Immediate: Reverted deployment, reduced alert delay,
  pinned AWS SDK version to 2.20
- Follow-up: Implement automated e2e tests for DynamoDB,
  upgrade commons lib AWS SDK version, ...
Classification¶
The stage systematically identifies whether specific datastore technologies directly contributed to the incident. The process works as follows: the model receives a summary postmortem document along with a list of technologies in question. The LLM was prompted to return only the name of technologies with a confirmed direct connection or “None” if there is no such link:
- Identify any mentions of these technologies within the document;
- Verify whether the mention is explicitly connected to the root cause or impact of the incident.
Surface Attribution Error was an obstacle for our solution. We have to strictly prohibit inference or assumption, ensuring that only explicitly stated connections are flagged. Additionally, the prompt provides negative examples.
The implemented classifier works reliably to classify a technology giving us the capability to scale the analysis for all technologies at Zalando Tech Radar.
Analyzer¶
The most crucial part of the incident analysis is the extraction of a short 3 to 5 sentence digest that highlights (a) the root cause or fault condition involving the technology; (b) the role it played in the overall failure scenario; (c) any contributing factors or interactions that amplify the issue. The output is produced with a technical audience in mind. It is aiming to be precise and readable without requiring access to the full postmortem, requiring only 30 to 60 seconds to understand the critical aspects of each incident.
Below is the censored example of the digest produced by LLMs:
DynamoDB contributed to this incident as the affected data store,
but was not the root cause of the failure. The root cause was a
version incompatibility between an upgraded AWS SDK (2.30.20)
and an older DynamoDB support module (2.17.279) that still
depended on a class removed in the newer SDK version.
This dependency mismatch caused all DynamoDB write operations
to fail with a NoClassDefFoundError, which cascaded to affect
multiple [SERVICES] that relied on DynamoDB for storing [DATA].
DynamoDB itself functioned normally—the issue was entirely due
to the application's inability to properly connect to and
interact with DynamoDB after the SDK upgrade.
This stage adds critical interpretive value by turning raw incident data into a derivative dataset about technological failures usable for further processing by humans, LLMs or other techniques. For example, it has enabled us to discover common patterns of datastore incidents over these years.
Patterns¶
The real value emerges from a single-page description of cross-incident analysis, enabling engineering leadership to grasp recurring patterns, failure modes, and contributing factors comprehensively.
We are feeding the entire set of incident digests into LLM within a single prompt. Within the prompt, we are explicitly prohibiting inference, redundancy, or the inclusion of any information not grounded in the source data. This ensures the resulting output is both precise and actionable. The output is a concise list of common failure themes across the incidents.
Below is the censored example of the failure patterns as LLM report:
DynamoDB Capacity and Throttling: Multiple incidents
involved DynamoDB capacity issues, leading to throttling,
latency, and service failures.
Insufficient Testing and Scaling: Lack of adequate
pre-deployment performance testing and insufficient
automated scaling contributed to incidents.
Application Logic Errors: Bugs in application logic,
such as duplicate data creation or inefficient
algorithms, led to database overload and service degradation.
Monitoring and Alerting Gaps: Insufficient monitoring
and overly sensitive or insensitive alerting
thresholds were factors in some incidents.
The resulting patterns serve as a foundation for human analysis, initiating reviews and facilitating the identification of reliability risks, architectural vulnerabilities, or process gaps. This approach enables us to maintain a focus and narrow the communication. Rather than sifting through an extensive volume of raw data, we are provided with a clear direction towards the most critical areas for in-depth investigation.
Human curation¶
While the goal of our solution is to reduce human involvement, human curation remains essential. During the pipeline development, we conducted 100% human curation of output batches. This involved analyzing the generated postmortem digests and comparing them to the original postmortems. The curation process was purely labelling, requiring colleagues to upvote or downvote the results. The feedback loop from humans helped us refine prompts and make optimal model selections for each stage. As the system matured, we relaxed human curation to 10-20% of randomly sampled summaries from each output batch. We are still using human expertise to proofread the final report applying editorial changes to summary and incident patterns.
Two Years of Data: Key Findings¶
Two years of data analysis reveal recurring patterns are primarily related to how these datastore technologies are being used. Configuration & deployment, as well as capacity & scaling are primary reasons for datastore incidents. Below, we highlight examples of case studies:
- AWS S3 incidents: consistently tied to misconfigurations in the deployment artifacts preventing applications from accessing S3 buckets, often due to manual errors or untested changes. This insight directly led to the solution for automated change validation for infrastructure as code which is able to shield us from 25% subsequent datastore incidents, demonstrating a clear return on investment.
- AWS ElastiCache incidents: a consistent trend of 80% CPU utilization causing elevated latency at peak traffic. This AI-driven insight led us developing a strategic direction about capacity planning, instance type selection and traffic management for AWS ElastiCache.
We have established a comprehensive understanding of failure patterns within our datastores through two years of incident analysis. So far the most recurring incident patterns are:
- absence of automated change validation at config and infrastructure as a code, and poor visibility into changes and their effects;
- inconsistent or ad-hoc change management practices including manual intervention;
- absence of progressive delivery with datastores (e.g., canary or blue-green);
- underestimating the traffic pattern;
- failing to scale ahead of demand or delayed auto-scale responses;
- bottlenecks due memory, CPU, or IOPS constraints.
Our datastore portfolio is mature and resilient, with incidents very rarely directly attributed to technological flaws. In the past 5 years, we encountered problems with JDBC drivers and had incidents related two known PostgreSQL bugs:
- The incident was caused by a crash in the AUTOVACUUM LAUNCHER process due to a race condition, which in turn terminated all connections in the PostgreSQL database pool. This crash was attributed to a known bug in PostgreSQL 12.
- A major version upgrade of the Postgres database from version 16 to 17, which triggered a bug in Postgres' logical replication. It occurs when DDL commands are executed in parallel with a large number of transactions, leading to a memory leak.
The AI analysis significantly reduced the time for analysis from days to hours and achieved the scalability of the solution across multiple technological areas. It also surfaced 'hidden hotspots' like improper connection pool configuration or circuit breakers leading to cascading failures that were previously considered stable.
Dead Ends: Where AI Fell Short¶
The incident analysis pipeline has gone through a few evolutions, utilizing various models and hosting solutions. Initially, we employed open source models hosted within LM Studio. Subsequently, we evaluated different models, and the current iteration is powered by Claude Sonnet 4 on AWS Bedrock. Such evolution was primarily driven by compliance topics rather than technical necessity. Postmortem document contain PII data of on-call responders, companies business metrics, GMV losses, etc. The legal alignment was a pre-condition before using cloud hosted LLMs (e.g. AWS Bedrock). Within each of these environments, Hallucination, Surface Attribution Error and Latency are three key obstacles impacting on the pipeline and the quality of the analysis.
The earlier prototypes were built with small models from 3B to 12B parameters. We have observed up to 40% probability for hallucination at summary and analysis phases. The model has written up the text that sounded plausible but it was factually incorrect. Anecdotally, small models fabricated a plausible summary regarding a non-existent DynamoDB incident, solely because DynamoDB was mentioned in the title of a playbook linked to the postmortem. To solve this challenge, we have experimented with various prompting strategies, emphasizing strict requirements and clearly articulating expectations with examples. Then we conducted human-led curation until the effect of hallucination became less than 15%. Finally, we appreciated the effort to harden prompts when transitioning to a larger-scale model as hallucinations became negligible. It was crucial for enabling the strategic insights discussed earlier.
Surface Attribution Error is dominant almost in each stage of the pipeline. The model is making decisions based on surface-level clues rather than deeper meaning or causality. The model makes a bias to prominent keywords staging on the surface-level instead of reasoning through context to identify the actual causal factor. For instance, it could offer a well-structured and authoritative explanation regarding the contribution of AWS S3 to an incident, even if "S3" is merely mentioned without being causally linked. Although negative prompting was employed to mitigate the issue, it has not been entirely resolved; we still observe approximately 10% attribution, even with advanced models such as Claude Sonnet 4.
These are primary reasons for skepticism and acceptance of the results when we saw the first version of the report. By ensuring each stage's input/output was human-readable and subject to curation, we fostered trust and demonstrated the AI's role as an assistant able to produce a high quality. The pivotal role of digests allowed humans to observe all incidents as a whole and precisely validate and curate the reports produced by LLMs.
Surface Attribution Error often accompanies overfitting, since both involve relying on superficial patterns from past data rather than deeper, more reliable signals. General purpose LLMs are trained on publicly available data, and struggle to identify emerging failure patterns that haven't been seen before or properly deal with Zalando proprietary technology. Given that the datastore analysis focused exclusively on public technologies, the overfitting effect was negligible. Currently, we rely on human editorial work for the final report to address any novel failure modes that AI may have overlooked. An observable instance of this issue results in the unacceptable analysis of incidents concerning Zalando internal technologies (e.g. Skipper). Remediation of this and similar issues requires a model fine-tuning.
Fail fast and rapid iterations were essential for us during the pipeline development. Given the volume of our documents, we have concluded that the overall document processing time should not exceed 120 seconds; otherwise, the processing of annual data becomes impractically long. Initial releases utilized open source model with 27B parameters, which constituted the most time-consuming phase in the pipeline, typically requiring 90 to 120 seconds for completion, giving us no bandwidth to chain multiple stages. The “map-fold” architecture depicted earlier was released with multiple models 3B, 12B and 27B requiring about 20 seconds per document to classify and 60 seconds per incident to conduct analysis. This has enabled the processing of annual data analysis in under 24 hours. The most recent release, based on Claude Sonnet 4, processes each postmortem in approximately 30 seconds, offering immediate analytical opportunities.
The initial concept of a no-code agentic solution was quickly deemed unfeasible due to performance limitations, inaccuracies, and hallucinations encountered during prototype development. We have opted for a hybrid solution where the input and output of each stage are amenable to human evaluation, thereby enhancing confidence in accuracy.
Reliable accuracy in extracting numerical data, such as GMV or EBIT loss, affected customers, and repair time, from postmortems was not achieved. Consequently, we depend on our internal incident dataset that serves as a trustworthy source of truth for opportunity analysis.
Takeaways and Recommendations¶
The discussed solution has addressed our core problem – the inability of manual postmortem review to keep pace with the large volume of incidents, identifying systemic issues and making data-driven investments for preventing recurring failures. Our exercise is on par with industry insights about AI:
- AI's transformative potential: LLMs can effectively turn a vast corpus of human-authored postmortems into a dynamic, decision-making dataset, surfacing patterns and systemic issues that are impossible to identify manually at scale. Hallucination and Surface Attribution Error were significant obstacles initially, but could be largely mitigated through strict prompting strategies, negative prompting, and human curation.
- Multi-stage pipeline effectiveness: A multi-stage LLM pipeline, where each stage specializes in a single objective (summarization, classification, analysis, patterns), proved more effective and reliable than using single high-end LLMs with large context windows, mitigating issues like "lost in the middle" and improving accuracy.
- Human-in-the-loop is crucial: Despite automation, human curation, examination, labeling, and quality control at each stage, especially the "digests," are essential for refining prompts, ensuring accuracy, fostering trust, and addressing novel failure modes that AI might overlook.
Going forward and evolving the SRE-AI partnership, our takeaways and recommendations:
- Start small and iterate: Begin with focused use cases and embrace rapid iterations.
- Prioritize prompt engineering: Invest time in crafting precise and constrained prompts to minimize hallucinations and surface attribution errors. Design your solution with evolvability in mind and ship your pipelines along for golden datasets for testing.
- Design for human interpretability: Ensure intermediate outputs are human-readable to facilitate trust and validation.
In essence, Zalando's experience demonstrates that AI, when implemented thoughtfully with a human-in-the-loop approach, can transform postmortems from mere "dead ends" into invaluable "data goldmines," providing strategic insights to drive targeted reliability investments and cultivate a more intelligent infrastructure.
Conclusion¶
Dead ends or goldmines? By transforming thousands of incident reports into a dynamic, decision-making dataset, we've shown that every system outage can indeed make our infrastructure smarter. AI-powered pipelines bring speed to turning postmortems into predictive signals for the reliable future.
We trust that this discussion has provided valuable insights into fine-tuning AI for nuanced interpretation, supporting decision-makers, and offering practical advice on automating postmortem analysis to enhance system reliability for the benefit of your customers.
Your incidents hold the blueprint to your most strategic infrastructure wins - if you are listening correctly.
We're hiring! Do you like working in an ever evolving organization such as Zalando? Consider joining our teams as a Software Engineer!
