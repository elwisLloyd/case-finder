# Accelerating incident response using generative AI

Источник: https://security.googleblog.com/2024/04/accelerating-incident-response-using.html

Introduction
As security professionals, we're constantly looking for ways to reduce risk and improve our workflow's efficiency. We've made great strides in using AI to identify malicious content, block threats, and discover and fix vulnerabilities. We also published the Secure AI Framework (SAIF), a conceptual framework for secure AI systems to ensure we are deploying AI in a responsible manner.
Today we are highlighting another way we use generative AI to help the defenders gain the advantage: Leveraging LLMs (Large Language Model) to speed-up our security and privacy incidents workflows.
Incident management is a team sport. We have to summarize security and privacy incidents for different audiences including executives, leads, and partner teams. This can be a tedious and time-consuming process that heavily depends on the target group and the complexity of the incident. We estimate that writing a thorough summary can take nearly an hour and more complex communications can take multiple hours. But we hypothesized that we could use generative AI to digest information much faster, freeing up our incident responders to focus on other more critical tasks - and it proved true. Using generative AI we could write summaries 51% faster while also improving the quality of them.
Our incident response approach
When suspecting a potential data incident, for example,we follow a rigorous process to manage it. From the identification of the problem, the coordination of experts and tools, to its resolution and then closure. At Google, when an incident is reported, our Detection & Response teams work to restore normal service as quickly as possible, while meeting both regulatory and contractual compliance requirements. They do this by following the five main steps in the Google incident response program:
- Identification: Monitoring security events to detect and report on potential data incidents using advanced detection tools, signals, and alert mechanisms to provide early indication of potential incidents.
- Coordination: Triaging the reports by gathering facts and assessing the severity of the incident based on factors such as potential harm to customers, nature of the incident, type of data that might be affected, and the impact of the incident on customers. A communication plan with appropriate leads is then determined.
- Resolution: Gathering key facts about the incident such as root cause and impact, and integrating additional resources as needed to implement necessary fixes as part of remediation.
- Closure: After the remediation efforts conclude, and after a data incident is resolved, reviewing the incident and response to identify key areas for improvement.
- Continuous improvement: Is crucial for the development and maintenance of incident response programs. Teams work to improve the program based on lessons learned, ensuring that necessary teams, training, processes, resources, and tools are maintained.
Google’s Incident Response Process diagram flow
Leveraging generative AI
Our detection and response processes are critical in protecting our billions of global users from the growing threat landscape, which is why we’re continuously looking for ways to improve them with the latest technologies and techniques. The growth of generative AI has brought with it incredible potential in this area, and we were eager to explore how it could help us improve parts of the incident response process. We started by leveraging LLMs to not only pioneer modern approaches to incident response, but also to ensure that our processes are efficient and effective at scale.
Managing incidents can be a complex process and an additional factor is effective internal communication to leads, executives and stakeholders on the threats and status of incidents. Effective communication is critical as it properly informs executives so that they can take any necessary actions, as well as to meet regulatory requirements. Leveraging LLMs for this type of communication can save significant time for the incident commanders while improving quality at the same time.
Humans vs. LLMs
Given that LLMs have summarization capabilities, we wanted to explore if they are able to generate summaries on par, or as well as humans can. We ran an experiment that took 50 human-written summaries from native and non-native English speakers, and 50 LLM-written ones with our finest (and final) prompt, and presented them to security teams without revealing the author.
We learned that the LLM-written summaries covered all of the key points, they were rated 10% higher than their human-written equivalents, and cut the time necessary to draft a summary in half.
Comparison of human vs LLM content completeness
Comparison of human vs LLM writing styles
Managing risks and protecting privacy
Leveraging generative AI is not without risks. In order to mitigate the risks around potential hallucinations and errors, any LLM generated draft must be reviewed by a human. But not all risks are from the LLM - human misinterpretation of a fact or statement generated by the LLM can also happen. That is why it’s important to ensure there is human accountability, as well as to monitor quality and feedback over time.
Given that our incidents can contain a mixture of confidential, sensitive, and privileged data, we had to ensure we built an infrastructure that does not store any data. Every component of this pipeline - from the user interface to the LLM to output processing - has logging turned off. And, the LLM itself does not use any input or output for re-training. Instead, we use metrics and indicators to ensure it is working properly.
Input processing
The type of data we process during incidents can be messy and often unstructured: Free-form text, logs, images, links, impact stats, timelines, and code snippets. We needed to structure all of that data so the LLM “knew” which part of the information serves what purpose. For that, we first replaced long and noisy sections of codes/logs by self-closing tags (<Code Section/> and <Logs/>) both to keep the structure while saving tokens for more important facts and to reduce risk of hallucinations.
During prompt engineering, we refined this approach and added additional tags such as <Title>, <Actions Taken>, <Impact>, <Mitigation History>, <Comment> so the input’s structure becomes closely mirrored to our incident communication templates. The use of self-explanatory tags allowed us to convey implicit information to the model and provide us with aliases in the prompt for the guidelines or tasks, for example by stating “Summarize the <Security Incident>”.
Sample {incident} input
Prompt engineering
Once we added structure to the input, it was time to engineer the prompt. We started simple by exploring how LLMs can view and summarize all of the current incident facts with a short task:
Caption: First prompt version
Limits of this prompt:
- The summary was too long, especially for executives trying to understand the risk and impact of the incident
- Some important facts were not covered, such as the incident’s impact and its mitigation
- The writing was inconsistent and not following our best practices such as “passive voice”, “tense”, “terminology” or “format”
- Some irrelevant incident data was being integrated into the summary from email threads
- The model struggled to understand what the most relevant and up-to-date information was
For version 2, we tried a more elaborate prompt that would address the problems above: We told the model to be concise and we explained what a well-written summary should be: About the main incident response steps (coordination and resolution).
Second prompt version
Limits of this prompt:
- The summaries still did not always succinctly and accurately address the incident in the format we were expecting
- At times, the model lost sight of the task or did not take all the guidelines into account
- The model still struggled to stick to the latest updates
- We noticed a tendency to draw conclusions on hypotheses with some minor hallucinations
For the final prompt, we inserted 2 human-crafted summary examples and introduced a <Good Summary> tag to highlight high quality summaries but also to tell the model to immediately start with the summary without first repeating the task at hand (as LLMs usually do).
Final prompt
This produced outstanding summaries, in the structure we wanted, with all key points covered, and almost without any hallucinations.
Workflow integration
In integrating the prompt into our workflow, we wanted to ensure it was complementing the work of our teams, vs. solely writing communications. We designed the tooling in a way that the UI had a ‘Generate Summary’ button, which would pre-populate a text field with the summary that the LLM proposed. A human user can then either accept the summary and have it added to the incident, do manual changes to the summary and accept it, or discard the draft and start again.
UI showing the ‘generate draft’ button and LLM proposed summary around a fake incident
Quantitative wins
Our newly-built tool produced well-written and accurate summaries, resulting in 51% time saved, per incident summary drafted by an LLM, versus a human.
Time savings using LLM-generated summaries (sample size: 300)
The only edge cases we have seen were around hallucinations when the input size was small in relation to the prompt size. In these cases, the LLM made up most of the summary and key points were incorrect. We fixed this programmatically: If the input size is smaller than 200 tokens, we won’t call the LLM for a summary and let the humans write it.
Evolving to more complex use cases: Executive updates
Given these results, we explored other ways to apply and build upon the summarization success and apply it to more complex communications. We improved upon the initial summary prompt and ran an experiment to draft executive communications on behalf of the Incident Commander (IC). The goal of this experiment was to ensure executives and stakeholders quickly understand the incident facts, as well as allow ICs to relay important information around incidents. These communications are complex because they go beyond just a summary - they include different sections (such as summary, root cause, impact, and mitigation), follow a specific structure and format, as well as adhere to writing best practices (such as neutral tone, active voice instead of passive voice, minimize acronyms).
This experiment showed that generative AI can evolve beyond high level summarization and help draft complex communications. Moreover, LLM-generated drafts, reduced time ICs spent writing executive summaries by 53% of time, while delivering at least on-par content quality in terms of factual accuracy and adherence to writing best practices.
