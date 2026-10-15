# Using AI to help SNAP recipients diagnose and restore lost benefits

Источник: https://www.propel.app/insights/using-ai-to-help-snap-recipients-diagnose-and-restore-lost-benefits/

Using AI to help SNAP recipients diagnose and restore lost benefits
Our editorial promise
All of our Propel editorial content meets our high bar for accuracy, timeliness, trust, and relevance. Our pages are edited and fact-checked to make sure we meet our mission of giving you information you can rely on.
Learn more about our editorial standards.
If this type of applied AI work interests you, Propel has also launched a AI Residency opportunity.
Each month, over 5 million people use Propel to check their SNAP balance and manage their benefits.
That also means that, for many, Propel is the first place they learn that a deposit has not arrived as expected. When this happens, it’s most often due to an administrative or paperwork issue with their SNAP case.
In many cases, resolving these interruptions in benefits can be easy if the issue is correctly identified and they know what action to take. But because it’s often a moment of panic for people, a stoppage in benefits can lead to increased call volume for state agencies, and then longer wait times for recipients.
Propel has been testing ways to leverage AI to help people fix these problems faster, reduce unnecessary churn, and lighten call volumes for state administrators by helping individuals solve issues on their own.
The problem: SNAP churn#the-problem-snap-churn
Our data shows that about 200,000 of our 5 million monthly users experience an interruption in benefit deposits. We know this because app activity spikes around regular and predictable deposit days, showing clear patterns when deposits are expected, but don’t arrive.
Most interruptions in benefits occur during the process of renewing eligibility with a state SNAP agency. When someone is still eligible to receive SNAP benefits, but they have a lapse because of a case issue, it’s known as "program churn." The two main acute drivers of churn we have witnessed are:
- Periodic Reports: Forms that most recipients submit about six months after applying or renewing, where they report any changes that may affect their benefit amount and eligibility.
- Recertification: The process of reapplying for benefits, typically once every 12 months.
Churn disrupts families’ access to food and adds unnecessary workload for state agencies. People who still qualify can go weeks without benefits, experiencing increased food insecurity, while agencies must handle extra calls and unnecessary additional workload instead of focusing on core work, like processing new applications.
Our approach to reducing SNAP churn for our users#our-approach-to-reducing-snap-churn-for-our-users
The first step to helping our users who experience an interruption in benefits is identifying and notifying them. We did this by first developing a highly accurate algorithm for detecting when a deposit is expected but did not come in—and informing the user ASAP in the app.
When someone misses a deposit, they generally need to do two things: (1) identify the reason for the interruption (usually documented in a notice from their SNAP agency), and (2) take the right action to fix it.
To address the first issue, we set out to design tools that help recipients locate and understand these notices without needing to call their agency. This reduces strain on call centers and helps people avoid long hold times.
To address the second issue, we focused on encouraging targeted actions instead of unnecessary reapplications. If someone reacts quickly by reapplying, it restarts a 30-day processing timeline, and can extend the wait for benefits to return by up to a month, when a smaller and easier action might have restored their benefits.
Examples of these smaller, more targeted actions include:
- Submitting a missed periodic report late (instead of submitting an entire new application)
- Resubmitting a report form (for example, if the person forgot to sign it the first time)
- Identifying and submitting an outstanding document (like a paystub needed for both recertifications and reports)
Testing AI-powered help for an interruption in SNAP benefits#testing-ai-powered-help-for-an-interruption-in-snap-benefits
We ran two tests. The first was a more structured triage flow (a multi-step web form) to simplify navigating the issue for users. This we manually edited prior to launching, but implemented with AI code generation.
The second was a more open-ended and higher-touch chat tool combining an underlying AI language model with a detailed written help guide.
Test 1: A missed-deposit triage flow (California)#test-1-a-missed-deposit-triage-flow-california
We developed a multi-step triage flow with logic to help people (1) self-diagnose the reason they might have missed their deposit and (2) point them to the most likely action needed to resolve the issue.
We used AI to generate the code that powers this diagnostic tool, allowing us to rapidly build and refine the flow. This demonstrated a key takeaway we had: today’s AI models are sufficiently capable at code generation to support the quick development of complex, multi-page form flows based on a written logic tree, like our “decision tree”/”triage” flow.
The initial choice for users in the triage flow
We chose to run this test in California for two reasons. First, as the largest state, even a small-scale test can demonstrate significant potential for broader impact.
Second, California’s periodic report policy and the way it’s implemented through the state’s online portal, BenefitsCal, give SNAP recipients a greater opportunity than in most states to easily fix case problems. Specifically:
- State policy allows someone to submit their periodic report (called the Semi-Annual Report, or SAR 7 in CA) a month late and still have their benefits reinstated — even if they missed the original deadline.
- The state's online benefits portal (BenefitsCal) allows people to fill out this form online even if it is late.
Both of these increase the odds that someone who missed a deposit due to a SAR 7 issue can successfully get their benefits back without having to reapply.
We assisted about 1,300 CalFresh (California SNAP) recipients with this flow during one month’s deposit cycle. The speed of AI code generation not only allowed us to build and test this tool quickly but also made it easy to adapt for other states — showing how today’s AI can accelerate process improvements.
Test 2: an AI chat assistant for a missing EBT deposit (nationwide)#test-2-an-ai-chat-assistant-for-a-missing-ebt-deposit-nationwide
For our second test, we created an AI chat tool designed to help people fix common issues that cause missed SNAP deposits.
This chat assistant uses AI to generate situation- and context-specific (e.g. specific to the state) responses in real-time, effectively mimicking the process a knowledgeable SNAP assister would follow to help someone resolve their program issues.
The notification a user saw if a missed deposit was detected, and initial guidance for someone who doesn’t know the reasons
The AI tool covers a wide range of possible scenarios and dynamically generates responses tailored to the person's specific state, directing them to the appropriate channel (like the state’s online portal, or its main call center phone number) accordingly.
Helping a Hawaii user navigate a periodic report problem
We built this chat tool using Decagon, a generative AI platform that let us quickly layer custom help on top of a knowledge base, with real-time monitoring, escalation to our team, and performance tracking.
In this AI chat interface test, we assisted about 1,000 SNAP recipients for one month’s deposit cycle in the spring of 2025.
Findings and impact#findings-and-impact
We ran these tests at a relatively small scale (on the order of ~1,000 users each) so that we could carefully monitor results and manually handle any escalations where necessary. For example, if the AI chat tool detected it could not help with an issue, it would escalate to someone on our team who would reach out to the user directly to help.
Despite the limited scale, these pilots yielded promising results:
- Strong uptake: In our AI chat test, more than half of eligible users (53%) used the help tools when offered, indicating significant demand for this type of assistance.
- Faster benefits restoration: Randomized testing with a control group showed modest but meaningful improvements in two key outcomes for the users in both tests:
  - Days to next deposit (getting benefits back faster), and
  - Higher rates of restored benefits in the same month (staying enrolled in the program, rather than churning and reapplying)
- Positively received and a more responsive user experience: Users could rate the chat conversation, and while most did not, among those who did, there were very few negative ratings.
AI also handled unexpected user situations remarkably well. For example, the chat tool recognized that a user’s mention of "smrf" referred to Hawaii's specific shorthand for a period report form (the "Six Month Report Form"). Perhaps more impressive, the AI model seamlessly switched languages mid- conversation when a user unexpectedly began replying in Haitian Creole.
The AI model switching into Haitian Creole: multi-lingual support was not explicitly designed ahead of time, but the underlying AI model identified the switch and responded accordingly
These instances from real user interactions revealed current AI models’ potential to understand context and adapt in ways that traditional automated systems cannot. This has implications for broader applications of these model capabilities to many parts of the benefits process.
Future directions#future-directions
Our tests surfaced several opportunities to improve how we help people address interruptions in SNAP benefits:
Reducing friction on accessing notices: Making it easier for people to find and understand the SNAP notices that explain the acute cause of a benefits lapse would shift more people away from the default action they take — calling the agency or going into the office. We are considering options to help users with this more.
Proactive reminders and support: Instead of waiting until a missed deposit is detected, we can help people know when to submit required forms—like periodic reports or recertifications — and guide them through completing them correctly (for example, ensuring they sign the form).
Closing the digital gap for SNAP case portal access: A follow-up survey found that 75% of Propel users have an account with their state SNAP agency’s online benefits portal. The remaining 25% (~1.25 million users) present an opportunity. They are digitally savvy enough to use a smartphone app (Propel) for checking their EBT card balance and yet they do not use their state’s online self-service tools to manage their SNAP case. Identifying ways to help these users set up and use online accounts could simplify their experience and reduce phone wait times at state agencies, given the scale of this group.
These directions all point toward a more comprehensive approach to benefit case support that anticipates and prevents disruptions, rather than simply responding to them as we did in these tests.
Conclusion#conclusion
Our small-scale tests show how today’s AI capabilities can help people navigate SNAP benefit interruptions, an acute example of the broader challenge of benefits navigation.
Our tests suggest that AI can reduce both the time it takes to restore food benefits and the administrative burden on people and state agencies by lowering call volumes and wait times. This technology's ability to provide personalized, multilingual support at scale–when paired with the right navigation tools— points to applications beyond SNAP in other public benefit programs with similar structures.
For organizations interested in building on this work, we recommend starting with small-scale pilots that allow for close monitoring, iteration, and human support for any necessary escalation.
If you work in SNAP administration or social benefit programs and are interested in more detail on our findings or have questions, we would love to hear from you: email Dave Guarino at dave.guarino@joinpropel.com
We are also announcing our AI Residency at Propel, for senior-level software developers, policy/benefits experts, and design engineers. If this type of applied safety net AI work is something you are interested in working on more directly, read the details and consider reaching out.
