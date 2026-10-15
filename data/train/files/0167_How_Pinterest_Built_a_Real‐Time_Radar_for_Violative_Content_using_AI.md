# How Pinterest Built a Real‑Time Radar for Violative Content using AI

Источник: https://medium.com/pinterest-engineering/how-pinterest-built-a-real-time-radar-for-violative-content-using-ai-d5a108e02ac2

How Pinterest Built a Real‑Time Radar for Violative Content using AI
Faisal Farooq | Sr. Director Trust Engineering; Aravindh Manickavasagam | Staff Technical Program Manager; Attila Dobi | Sr. Staff Data Scientist
People come to Pinterest to find ideas they feel good about. To keep that experience safe, we need to know not just what gets reported, but what people actually saw. That’s what we call prevalence: the percentage of all views, on a given day, that went to content that violates a policy. Prevalence complements reporting by covering its blind spots, helping us spot under‑reported harms, track trends, and tell whether interventions work.
Why Prevalence Matters
Historically, our Trust & Safety teams leveraged multiple indicators to understand the extent of policy violating content on the platform. “In-app user reports” confirmed by human reviewers served as a key indicator alongside other measures of potential harm. While user reports are invaluable because they come directly from our community, a report‑only metric is incomplete.
What a Reports‑only View Can’t Tell Us
- Some harms are under‑reported (for example, self‑harm) due to stigma or sensitivity.
- Users who seek harmful content don’t report what they’re seeking.
- Rare categories generate few reports, so we lack statistical power to track progress or detect emerging threats.
- Scaling report handling with human review adds cost and latency.
Prevalence fills those gaps. Instead of waiting for reports, we measure what people actually saw each day by sampling based on user impressions and labeling them at scale. This gives us a stable, statistically powered view across a broader spectrum of policies, independent of enforcement thresholds, so that we can monitor risks, set goals, track progress, and act sooner.
Addressing Historical Challenges with Prevalence Measurement
Historically, measuring prevalence was expensive because it relied on human review. We could only run large, platform‑representative studies infrequently (roughly every six months and not always on a fixed cadence), so pre/post comparisons after interventions were slow and often hard to trust. Secondly, human review can oftentimes be unstable. In order to reach reliable and stable decisions, we required at least two independent reviewers per item, plus adjudication on disagreements, which further increased cost and latency.
To address these cost and latency constraints while enabling more frequent and reliable measurement, we built an AI-assisted workflow that allows us to focus on measuring the daily user experience.
What We Measure
We estimate how often violating content is seen vs. how much is posted on the platform because “impact comes from exposure.” A single violating Pin might be posted once but seen a million times, or not seen at all. Measuring the share of views that went to policy‑violating content better reflects what people actually experienced on Pinterest. We report this daily, with 95% confidence intervals to show precision.
Metric: prevalence on a given day is: (# views of content that violates a given policy) / (# total views).
For example, if 10 out of 100,000 views in a sample are policy‑violating, the estimated prevalence is 0.01% for that policy area that day.
Policies and segments
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
The measurement can be further broken down so that the team can act on it.
- Policy area, e.g. Adult Content, Self‑harm, Graphic Violence.
- Sub‑policy, e.g. within Adult Content we separate nudity from explicit sexual content.
- Surface, e.g. Homefeed vs. Search vs. Related Pins.
- Other segments, where appropriate (such as content age, geography or user age buckets)
Methods at a Glance
Sampling
- We sample images from the daily user impressions stream, using risk scores from our production enforcement models to improve sampling efficiency, not as labels or inclusion criteria (the same models that remove policy‑violating content).
- What if some content is missing scores? As a failsafe, missing scores are imputed with the day’s median so fresh content stays in frame.
- Inclusion probabilities: For each content unit i we assign a sample probability
- Implementation detail: We implement this with weighted reservoir sampling using an index defined by:
- Why ML-assisted sampling, and why it stays unbiased:
• Scores as a lens, not the ruler: Production risk scores focus label budget on high‑risk, high‑exposure candidates; the estimator then re‑weights to remove that lensing so the prevalence statistic reflects impressions, not the model’s threshold. This decouples measurement from enforcement.
• Design Consistent Estimator: We use inverse‑probability weighting to keep daily impression‑weighted prevalence design‑consistent and comparable over time. In practice we use the Hansen–Hurwitz ratio for PPS‑with‑replacement and the Horvitz–Thompson ratio for without‑replacement, which remain unbiased even if thresholds or calibration drift.
Labeling at Scale
- We bulk‑label the sample with a multimodal LLM (vision + text) using prompts reviewed by policy subject matter experts (SMEs). The system logs decisions, brief rationales, and full lineage (policy version, prompt, and model IDs) for auditability.
- Calibration and de-biasing are critical to maintaining measurement accuracy at scale. We employ human validation of strategically sampled subsets immediately after launch as part of post-launch metric evaluation. These calibration samples are designed to capture edge cases and potential AI blind spots that could introduce systematic bias into our prevalence estimates. Before launching to production the LLM must meet a minimum decision quality requirement relative to human review. Additionally, LLM + prompt quality is periodically checked against Subject Matter Expert‑labeled gold sets (ground truth) to detect model drift and ensure the labeler/classifier remains accurate and aligned with current violations policy. This continuous monitoring process allows us to maintain measurement conviction as content patterns and policy interpretations evolve.
- LLM‑assisted labeling lets us run large, daily probability samples across more policy areas at a fraction of the latency (15x faster) and orders of magnitude lower operational cost than a human‑only workflow at comparable decision quality-while also preserving statistical validity and governance.
System Overview
Implementation Notes
- Inputs: Engagement at the entity × day level (e.g., impressions, Pin clicks, hides, reports) plus the latest production risk scores, used only as auxiliary signals. Missing scores are imputed with the day’s median.
- Sampling: We use a weighted reservoir sampler that gives more chances to items with higher impressions and higher risk scores, while still preserving an unbiased estimate when we reweight the sample [1]. This emulates probability proportional‑to‑size with replacement (PPSWR) and yields unbiased estimators when paired with the right weights [2]. A toggle also supports pure random sampling for validation studies.
- Labeling: The LLM returns any policy‑defined label hierarchy (e.g., {safe, not_safe, unsure}). The workflow records token usage and per‑run cost for budgeting and is model‑agnostic for future flexibility.
- Estimation: We compute overall prevalence and pivots, persist estimates, weights, and labels to production stores, and write diagnostics/lineage for audits. The dashboard surfaces the point estimate, 95% CI, CI width, and effective sample size.
Dashboard and Alerting
- Cards: Daily prevalence with 95% CI, sample positive rate (for monitoring sampling efficiency), auxiliary score distributions for context, and run health/lineage (prompt/model/taxonomy/metric versions).
- Pivots: The dashboard owners can slice prevalence by policy area, surface (Homefeed, Search, etc.), and selected sub‑policies.
- Validation: A random subsample of labels routes to an internal human validation queue for continual checks of the AI’s decision quality; a config switch enables pure random sampling to sanity‑check assumptions.
Impact
AI-assisted prevalence measurement has transformed how we understand and respond to platform safety challenges:
- Proactive Risk Detection and Response: We now have continuous measurement without historical blind spots. Dramatically faster labeling turnaround enables real-time monitoring, providing clearer understanding of platform risk and user experience. This leads to faster root cause analysis when issues emerge and more proactive identification of emerging trends before they scale.
• Faster Product Iteration and Data Driven Policy: Prevalence measurement provides immediate insight into how product launches impact platform trust and safety, enabling us to course-correct quickly and build more effective enforcements and interventions. The system also creates a valuable feedback loop for policy development and prompt tuning, helping us understand how clear and enforceable our policies are in practice.
• Strategic Decision Making Beyond Monitoring:
— Benchmarking and goal setting: establishing measurable targets for platform health and tracking progress
— Cross-team alignment: providing shared metrics that unite product, policy, and enforcement teams around common objectives
— Data-driven resource allocation: directing enforcement efforts where they’ll have the greatest impact
— Precise intervention measurement: with reliable prevalence baselines established, we can now A/B test enforcement strategies with statistical confidence to optimize policy interventions based on measurable outcomes
Constraints and Trade‑offs
- Rare categories can have wide daily CIs: we adapt γ [Equation 1], stratify, or pool to weekly as needed; the dashboard exposes CI width so owners can budget labels.
- Policy/prompt drift: Prompt and data versioning + selective time period based label backfills keep the series interpretable.
- LLM decision quality stability: LLM decision quality stability is required for metric conviction. We regularly run random‑sampling validations and monitor LLM outputs to detect and address potential decision quality drift.
- Cost guardrails: Token usage and per‑run cost per model/metric variant are tracked and periodically evaluated for cost efficiency.
Future Focus
- Pivots: Expand pivoting ability to viewer country, age, etc.
- Cost optimization:
— Multi step LLM labeling process: A first layer decides if labels are safe/unsafe using a short prompt. The second layer labels the unsafe items against a longer, comprehensive policy-prompt.
— LLM Fine Tuning: LLM’s fine tuned with SME labeled data have yielded improved performance during evaluations.
- Human-in-the-loop denoising/debiasing: Create an active denoising/debiasing system leveraging human review and SME labeling in the loop (prompt tuning, fine‑tuning, and label correction). The objective is to minimize LLM-human bias and reduce variance introduced by suboptimal decision quality.
- Further generalizing the pipeline for company‑wide measurement applications, further refining metric versioning and validation, developing prevalence based A/B testing guardrails.
Acknowledgements
Standing up a Trust and Safety prevalence radar has required sustained cross‑functional work across Trust & Safety teams including engineering, product and operations. Here’s an incomplete list of folks and teams who helped us design, ship, and operationalize daily prevalence:
- Data Science: Xiaohan Yang, Zehao Xu, Yuqi Tian, Minli Zang, Huan Yu, Robert Paine, Kevin O’Sullivan, Wenjun Wang, Benjamin Thompson
- Risk Intelligence: Jenny Bi, Mairead O’Doherty, Antons Tocilins-Ruberts
- Product: Monica Bhide, Prachi Wadekar, Dan Towne
- TPM: Nayan Patel, Helene Labriet-Gross
- Operations: Abby Beckman, Jessica Flora, Aaron Stein-Chester, Carol Davis
- Policy: Stanley Washington, Francesca Anzola
- Engineering: Vikram Deshpande, Ahmed Fayez, Naman Makhija
- Leadership: Faisal Farooq, Andrey Gusev, Sriram Subramanian
References:
- [Reservoir sampling trick] Weighted Random Sampling (2005; Efraimidis, Spirakis)
- [Hansen Hurwitiz 1943] On the theory of sampling from finite populations.pdf
