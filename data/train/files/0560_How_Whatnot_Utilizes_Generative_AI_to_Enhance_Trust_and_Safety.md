# How Whatnot Utilizes Generative AI to Enhance Trust and Safety

Источник: https://medium.com/whatnot-engineering/how-whatnot-utilizes-generative-ai-to-enhance-trust-and-safety-c7968eb6315e

How Whatnot Utilizes Generative AI to Enhance Trust and Safety
Charudatta (CD) Wad | Commerce Engineering
As one of the fastest-growing marketplaces in the world, it’s pertinent we work to keep Whatnot a safe platform where the community can share their passions. To maintain a trusted environment as we build a dynamic live shopping marketplace, we continuously evolve our approach to trust and safety.
In this blog post, we will discuss how we are utilizing Large Language Models (LLMs) to enhance trust and safety areas including multimodal content moderation, fulfillment, bidding irregularities, and general fraud protection.
Rule Engine: T&S Platform Foundation
As our platform grows, ensuring policy compliance becomes a significant challenge. To address this, we started with a centralized rule engine, which serves as a powerful tool for enforcing policies consistently and efficiently. By harnessing data and signals from multiple sources, this engine applies data-informed heuristics to determine whether a violation has occurred. Particularly, this approach proves highly effective for data-related enforcements, such as managing shipping delays, processing refunds, and facilitating cancellations.
The centralized rule engine acts as a robust backbone, enabling us to handle policy enforcement at scale. It efficiently analyzes vast amounts of data, including event data, ML model outputs, user interactions, and system logs, to identify potential violations promptly. This system allows us to streamline and automate the enforcement process, reducing manual effort and ensuring consistent application of policies across the platform.
Rule Engine Shortcomings
While the rule engine offers a robust framework for policy enforcement, it bears certain limitations. The rule engine operates within the confines of distinct scalar values, rendering it inadequate for navigating ambiguous scenarios and contextual comprehension. Traditionally, ML has been employed to assess individual messages in isolation. Before allowing content to be published, we run it through our content moderation model to ensure compliance with our community guidelines. This process guarantees that each message meets our quality standards and aligns with the values we strive to uphold. While this is an effective measure, it does not help with understanding the context of complex topics like harassment or fraud.
Elevating the Rule Engine: Rule Engine++
With advances in LLMs and the advent of complex models like GPT4, we can advance beyond the limited context of the rule engine. We can use LLMs to broaden our understanding of user interactions and conversations.
Use case: Scam Detection
As Whatnot grows, the vibrant community also becomes a target for scams and deception. We noticed an increase in attempts to scam our users, especially targeting new users who are not well- versed in the policies of the platform. These attempts usually start with an innocuous direct message either inquiring about a product that’s on sale or notifying users that they have won a Giveaway. These messages tend to build confidence through a pleasant exchange before trying to take the conversation off the platform. So, trying to predict the probability of a message being a scam using a single message is pretty difficult and has low precision. However, if we look at the entire exchange, the patterns become pretty evident. This is where LLMs have been immensely helpful in proactively detecting fraudulent messages and keeping our community safe.
For example, here is a sample messaging pattern used to defraud our sellers:
Each message by itself may not be a strong indicator of potential fraud but by taking into account the overall conversation, user engagement history, message attachments, and other dynamics at play like account age, we can better interpret the context and intent. This contextual approach empowers us to make more nuanced and informed decisions regarding content moderation and other violations. By doing so, we can better discern between genuine engagement, constructive/friendly discussions, and potentially harmful content.
Flow
We use different user signals (messaging patterns, account age) as qualifiers to determine which messages should be analyzed through LLMs. Once an account is flagged, we look at the different messages and run them through LLM to determine the probability of the messages being malicious.
Get Whatnot Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
The sample prompt used to identify the likelihood of a scam is as follows:
Given are following delimited by a new line
1. User id for the user under investigation
2. A message sent by a user through direct messaging
3. Interaction between users 
The interaction data is delimited by triple backticks, has timestamp, sender id and message separated by a '>>'.
The sender may be trying to scam receivers in many ways. Following patterns are definitive and are known to occur frequently on the platform.
“”” Known scam patterns “””
Assess if the provided conversation indicates a scam attempt.
Provide likelihoods (0-1) of scam, assessment notes in json format which can be consumed by a service with keys with no text output:
scam_likelihood and explanation (reasoning for the likelihood)?
``` text ````
The json output format from LLM is as follows:
{
"scam_likelihood": [0-1],
"explanation": reasoning for the likelihood for scam
}
Sample output:
{
"scam_likelihood": 1,
"explanation": “The sender is asking for card details and trying to manipulate the receiver into sending money. This is a clear indication of a scam attempt. The sender is also pretending to be in urgent need of money and indicating that they are unable to buy any of the listed items due to some payment failures, which are known scam patterns.”
}
We use the LLM output and provide additional signals to our rule engine to determine if we should action the user:
scam_likelihood > 0.6 and account_age < X days and message_frequency > Y and lifetime_orders < Z
If it passes the rule engine, we take temp action to disable certain features on the app and notify our ops team and pass along the LLM output (with likelihood and explanation) to investigate/action the user.
Results
Using automated detection we are able to proactively detect over 95% of scam attempts on the platform within a few minutes. We have seen 96% precision and high recall with the LLM output.
Fighting fraud and other attacks is an ongoing battle and new tactics are often used to circumvent our checks. For example, using text embedded in images rather than text messages. We combat it by adding OCR to message attachments and using that as additional input to the LLMs. The messaging is usually tweaked very often and that’s where LLMs surpassed our expectations in adapting to the different messaging patterns. This flow has now also expanded to enforce other policies like off-platform transactions and harassment.
Trust and Safety LLM Stack
In our content moderation stack, Language Models (LLMs) have emerged as a pivotal component, enabling us to effectively detect and moderate content across various dimensions such as spam, fraud, harassment, buyer dissatisfaction in order issues, and support escalations.
We aim to harness Gen AI’s potential as a cognitive partner (not a decision maker), combining AI-driven insights with human judgment in a human-AI partnership for robust trust and safety. This human-in-the-loop approach ensures LLMs serve as thoughtful collaborators, enhancing evaluations and safety protocols.
The system architecture can be divided into three phases:
- Gather: In this phase, we curate data from various sources like (events, user data, order history, ML models). This phase includes data identification, filtering, annotation, and formatting.
- Evaluate: utilize LLMs to act on the curated data. We orchestrate getting additional insights from LLMs. The raw data ($previous_ts_actions, $account_age etc.) and LLM insights ($scam_likelihood, $spam_likelihood, etc.) are passed through to our rule engine as scalar values to get recommended next steps based on our enforcement matrix. We currently rely on zero-shot and few-shot learning LLM predictions. However, we are investing in fine- tuning for other related use cases like support.
- Enforce: In this phase, there are three options for enforcement: close (no violation detected with high confidence), act (violation found with high confidence), or escalate (unsure if the violation is detected, needs a human review). Rule engine takes into consideration multiple factors like previous violations, account age, etc. to recommend the action (warn, suspend, etc.). Once the action is confirmed, the user is notified of the violation and the system is updated to reflect product access changes (if any) through Kafka.
Conclusion
Using Gen AI as a reasoning agent has enhanced our platform’s trust and safety. It’s exciting to envision a future where the rule engine and enforcement seamlessly merge into a unified Gen AI system.
We’re hiring! If new opportunities in Trust and Safety Engineering and AI interest you, take a look at our careers page.
