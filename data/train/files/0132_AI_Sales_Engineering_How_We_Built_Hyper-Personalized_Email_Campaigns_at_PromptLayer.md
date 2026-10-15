# AI Sales Engineering: How We Built Hyper-Personalized Email Campaigns at PromptLayer

Источник: https://blog.promptlayer.com/ai-sales-engineering-how-we-built-hyper-personalized-email-campaigns-at-promptlayer/

TL;DR for AI teams building and shipping LLM apps
Our AI sales system automates hyper-personalized email campaigns by researching leads, scoring their fit, drafting tailored four-email sequences, and integrating seamlessly with HubSpot. With this approach, we achieve:
- ~7% positive reply rate, resulting in way more meetings than we can handle
- 50–60% email open rates
The key advantage with PromptLayer is enabling our non-technical sales team to tweak email content, manage banned words, and update prompts directly—without engineering hand-holding.
Why We Re-Thought Outbound
If you've been in SaaS for more than a week, you already know the old outbound headaches: low-context lists, template fatigue, and the endless battle with spam filters. We all get those awful "Hey {first_name}, has my previous email offended you?" messages.
We’re an AI company, so obviously we should be using bespoke, AI-generated messaging. Custom prompts leveraging enriched company data, recent website scrapes, product usage insights, and tailored tone adjustments make each email distinct and engaging. Generic AI solutions use a one-size-fits-all prompt behind the scenes.
Modern AI can parse messy JSON, HTML, and CRM notes with minimal preparation. No more perfect structured data requirements. This is huge for teams where engineers need to collaborate with RevOps and non-technical growth leads.
That's where PromptLayer fits perfectly. We use our own platform to provide a:
- Prompt CMS for easy management (prompt versioning, comparisons).
- Batch evaluation runners to process datasets and run tests.
- Cost dashboards to track token usage transparently.
It's like WordPress for AI prompts—and it's becoming the backbone of our entire GTM motion.
Our GTM Stack at a Glance
Our outbound stack is pretty straightforward:
- Apollo for lead enrichment (though Seamless or Clay would work just as well)
- PromptLayer agent chains for research, lead scoring, subject lines, and email drafting.
- Make.com webhooks to trigger workflows on signup and handle CSV backfills.
- HubSpot sequences to log, manage, and send emails, with custom fields for tracking detailed information.
Future expansions will include integrations with NeverBounce, direct SendGrid dispatch, and ZoomInfo enrichment.
Agent #1 — Research + Scoring
This is where the magic starts. We take a raw account (just an email + rough company name), Apollo enrichment, and transform it into a rich company profile with a numeric fit score.
- Canonical-URL prompt (gpt-4o-mini) – Picks the most likely company domain from email, user input, and Apollo-enriched fields.
- Parallel content gathering
  - HTML web scrape – Custom Python fetch → strips boilerplate → gpt-4o-mini writes a 150-word gist. Quick, cost-effective, ideal for low-SEO sites but may miss recent news.
  - GPT web search summary – Uses OpenAI Perplexity-equivalent to pull top snippets, funding rounds, press hits. Excellent for fresh info; costs more and rate-limits at scale.
- "Relevance Reasoning" prompt: Matches discovered AI projects directly to PromptLayer features.
- Scoring: Assigns a numeric score (0-10) based on relevance, company size, revenue impact, and compliance risk.
- Branch gating: Skips low-score leads, optimizing resource use.
- Return payload – {score, reasoning, ai_projects[], url, company_name, website_summary}.
The cost profile is surprisingly low: ~$0.002 per lead, with 90% going to gpt-4o-mini.
Agent #2 — Subject-Line Generator
Getting the subject right is make-or-break for open rates, so we built a dedicated agent just for this task.
Our flow looks like:
- Draft subject with gpt-4o-mini (temp 0.5).
- Run a quality assurance (QA) prompt: must be ≤ 8 words, no banned words, no excessive title-case.
- If QA fails, retry once on gpt-4o-mini
- If still failing, escalate to gpt-4.5 (higher quality, but more than 10x the price) and accept result.
- Return {subject, passed_model} for logging.
The banned-word list lives directly in the PromptLayer UI so our sales team can update it directly without bugging engineering. We're on v16 of this prompt already.
Agent #3 — Email Sequencer
This agent generates a four-step cadence that feels genuinely hand-written, despite being fully automated.
The flow is elegant in its simplicity:
- Load static template with six placeholders: role, pain point, use-case, product blurb, social proof, CTA.
- Fill placeholders using values from Agent #1 (score, reasoning, AI projects) plus role from Apollo.
- Output four distinct emails plus sequence metadata.
The results are emails that trigger multi-paragraph thoughtful responses. Recipients genuinely believe a human spent time researching their company and crafting a personalized message—because we did, just with the help of AI.
The Results
The numbers tell the story clearly:
- 50–60% open rates.
- Positive-reply rate ≈ 10% across pilot batches—enough to book 4–5 demos daily from ~50 sends.
- Replies are long, thoughtful, and reference scraped details; none look auto-generated to prospects.
- Our VP of Sales now matches the throughput of himself AND a talented team of BDRs.
Why PromptLayer Makes This Possible
Non-technical collaboration has been the key piece of this puzzle.
Our VP of Sales, despite having no engineering background, directly iterates content in the PromptLayer UI, managing prompt templates, banned-word lists, and even model configurations.
Diffs and release labels let us ship 30+ prompt tweaks safely. Logs and evals mean every decision is traceable—no black-box surprises. Building the same chain, retries, and dashboards in raw code would take weeks.
A real iteration win: adding quoted titles to the subject prompt lifted opens by 6%. This idea was tested and deployed in an hour using the PromptLayer prompt CMS and evaluations tool.
Adapting It to Your Stack
PromptLayer supports various workflows.
Growth Leads: Easily upload leads via CSV, generate campaigns, review, and drop results into your CRM.
Developers & ML Teams: Integrate PromptLayer prompts into your infrastructure, manage versioning, tag prod / staging deploys, and track token costs.
RevOps Teams: Automate daily highly-personalized emails by feeding product usage data and past interactions; some are scaling to 10k+ emails/day using this approach.
Quick-start resources: PromptLayer Docs, Make.com plugin
Next Iterations We’re Shipping
We're far from done. Next on the roadmap:
- Real-time intent signals from live website activities.
- Multi-channel outreach using the same prompt infra across SMS and LinkedIn.
- Weekly automatic retraining loops with A/B tests to continuously optimize prompts.
Want to see how we built this yourself? Sign up for free at www.promptlayer.com
Or reach out for a demo—we'd love to show you how we built this. Maybe we'll even send you an AI-written email about it!
Appendix Diagram:
