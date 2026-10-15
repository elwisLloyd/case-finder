# Evaluating the performance of an LLM application that generates free-text narratives in the context of financial crime

Источник: https://medium.com/inside-sumup/evaluating-the-performance-of-an-llm-application-that-generates-free-text-narratives-in-the-context-c402a0136518

Evaluating the performance of an LLM application that generates free-text narratives in the context of financial crime
Evaluating a Large Language Model (LLM) application that generates unstructured data, such as a free-text narrative or dialogue, is a complex task that challenges traditional machine learning metrics. Accurately measuring any model’s performance is essential to assess the solution, iterate over versions, and enhance the model’s capabilities. In light of this, we present an alternative approach to evaluating LLM applications.
Specifically, we delve into using an LLM-driven evaluator that outperforms conventional NLP metrics and mimics a human evaluation method to identify custom evaluation criteria.
The stated evaluation method was applied to an LLM-driven free text report called Reason for Suspicion used in AML (Anti Money Laundering) to report suspicious activity.
About the LLM application
SumUp, as a financial institution with a diverse product offer, is subject to regulatory compliance and transactional monitoring. The efforts to fight fraud and money laundering include several machine learning models and rule engines whose results are verified by risk and compliance agents.
Once an agent confirms that an account has suspicious activity, they need to escalate and report it to the corresponding authority by writing a financial crime report. This document outlines the observed behaviour and provides supporting evidence.
The document contains information from different sources, such as previous machine learning model predictions, investigation notes from other linked cases and verification processes.
Writing a report can be repetitive and time-consuming as most narratives have similar structures. However, they might differ depending on each case’s typologies and behaviour.
In this context, Generative AI — Large Language Models (LLMs) in particular — can be a great tool to help us save a substantial amount of time, as these are models tailored to produce text responses with a significant degree of freedom.
Using a combination of the agent’s investigation and an LLM, documenting suspicious transactional activity is greatly optimised without the risk of an automated machine-driven false positive. In this context, prior human confirmation and investigation are paramount, as the consequences of automatically raising an alert without verification have an extremely high impact.
Proposed evaluation method
Evaluating an LLM application comes with unique challenges compared to the traditional machine learning model. In this context, we’re trying to assess the quality of a narrative, which involves several qualitative and, sometimes, subjective aspects into the assessment process. On the other hand, traditional machine learning models evaluate a numerical outcome using well-established mathematical methods. These are some of the main challenges encountered when evaluating an LLM application:
- Diverse output: The model needs to be stable to generate comparable results across different runs
- Subjective evaluation: Language is complex and ever-evolving, making it challenging to evaluate — different narratives can be adequate and contain relevant information but are written differently.
- Metric definition for “Good Response”: Defining objective metrics that effectively measure it is critical.
- Benchmarks for application evaluation: While existing benchmarks for LLMs focus on the models themselves, such as gpt-3.5, they often lack assessing the quality of LLM applications.
- Limitations of Traditional NLP metrics: Traditional Natural Language Processing (NLP) metrics may have a narrow scope in evaluating the output of LM models, potentially missing important nuances.
Traditional NLP metrics often need to catch up on capturing the essence of text evaluation from a human perspective, failing to provide a complete and accurate assessment of the narrative’s quality. These metrics have a limited perspective on the text, concentrating, for instance, on semantic similarity or n-gram-related metrics without considering the broader context of the problem. For example, does the report provide supporting evidence? Is the structure adequate? Does it cover the relevant topics? As a result, they differ significantly from how a human would approach the task of analysing a report and may not provide a complete or accurate assessment of the text.
To illustrate these challenges, we’ll define a scenario partially based on a real report of a merchant called Donald Duck [Appendix A]. Despite having a hypothetical character and behaviour, this scenario resembles a real financial crime report narrative.
Traditional NLP evaluation metrics provide a narrow overview
Metrics like the Rouge Score, commonly used in machine translation, measure the overlap of n-grams (unigrams — Rouge-1, bigrams — Rouge-2, and longest common subsequence — Rouge-L) between the machine-generated text and a reference text. These metrics deliver precision, recall, and F-scores.
In our evaluation, we used the Rouge Score metric to assess the quality of generated reasons for suspicion, distinguishing between well-generated and poorly generated texts. The following results were obtained:
Inaccurately-generated-text evaluation results:
Accurately generated text evaluation results:
The accurately generated text [Appendix A] is achieving a higher score, but the computed metrics show minimal differences between two texts representing opposing examples. We expect this metric to underperform more between texts with subtle differences. Additionally, this metric could catch some topic distributions but would be heavily affected by variations in paraphrasing.
Furthermore, this metric cannot check the structure of a text and compare the presence or absence of specific information between two texts. In contrast to evaluating a traditional prediction, the complete evaluation of a text is a more complex task that may require even some background context.
How can we solve this problem using an LLM-driven evaluator?
While human reviews are reliable, they’re time-consuming and often impractical in a fast-paced business environment. LLM-driven evaluation accurately compares 2 texts, providing both quantitative and qualitative insights into the quality and supportiveness of free-text narratives.
Specifically, we’ve developed an LLM-driven evaluation process that accurately compares two texts, delivering both quantitative and qualitative assessments of the text’s quality and supporting arguments. We created an evaluation with custom benchmark checks embedded in a prompt, each focusing on a specific reason why the text might be suspicious:
- Topic coverage: Ensuring consistency between the generated narrative’s topics and those in the reference text.
- Customer profile data: Confirming the inclusion of customer data in the narrative.
- Supporting facts: Checking for supporting facts related to the behaviour described.
- Avoiding invented facts: Verifying that no additional supporting facts have been created beyond those in the reference text.
- Conclusion: Ensuring the generated text includes a conclusion.
This approach provides a comprehensive evaluation of generated text, enabling efficient analysis of big chunks of data.
LLM-driven evaluators
LLM-driven evaluators are becoming increasingly popular, specifically in the chatbot context. According to the study “Judging LLM-as-a-judge with MT-Bench and Chatbot Arena” by Lianmin Zheng, LLMs as judged are scalable and explainable ways to approximate human preferences, which are otherwise very expensive to obtain.
Evaluating effectiveness: How well does this approach work?
Measuring the effectiveness of this approach requires quantifiable metrics. Numbers are straightforward to compare. For this reason, we instructed an LLM to create a score between 0–5, where 5 represents excellent coverage, and 0 signifies very poor coverage. While such a score system is easy to interpret, it may still lack some ground-based meaning.
To ensure objectivity, we need well-defined standards for a 0 and a 5. For this purpose, we can provide pre-labelled examples that exemplify a perfect 5, enabling the model to replicate these results and minimise subjectivity.
Get Néstor Castillo’s stories in your inbox
Join Medium for free to get updates from this writer.
When using an LLM in conjunction with the previous evaluation method, an accurately generated text produced the following results. We can observe an average score of 4,67:
{
"check_topic_coverage": 4,
"check_topic_coverage_explanation": "The generated text covers the same topics as the reference text. The suspicious indicators and reasons for suspicion are similar.",
"check_profile_data": 5,
"check_profile_data_explanation": "The generated text contains the same client information as the reference text. The client's business name, type of business, and country are present and match the reference text.",
"check_supporting_facts": 5,
"check_supporting_facts_explanation": "The generated text identifies the same suspicious indicators as the reference text, such as failed transactions, transactions being processed at unusual times, and excessive chargebacks. The narrative of the arguments is clear and makes sense.",
"check_facts_are_not_invented": 5,
"check_facts_are_not_invented_explanation": "All the facts in the generated text are consistent with the reference text. There are no invented facts or suspicious indicators that were not present in the reference text.",
"check_text_structure": 4,
"check_text_structure_explanation": "The structure of the generated text is slightly different from the reference text, but the narrative makes sense and is clear and concise. There is no repetition of facts over and over.",
"check_conclusion": 5,
"check_conclusion_explanation": "The generated text provides a clear conclusion that summarises the suspicious activities and explains why the client's account was closed.",
"general_score": 4.67,
"general_score_explanation": "The generated text is very similar to the reference text and covers the same topics. The client's information is present and the suspicious indicators are consistent with the reference text. The narrative is clear and concise, and the conclusion is provided. However, the structure of the text is slightly different from the reference text."
}
On the contrary, if we evaluate an inaccurately generated text, we get an average general_score of 2.5:
{
"check_topic_coverage": 2,
"check_topic_coverage_explanation": "The generated text mentions police reports and illicit activities, which are not present in the reference text. The suspicious indicators mentioned in the generated text are similar to the ones in the reference text, but the typology and reasons for suspicion are different.",
"check_profile_data": 3,
"check_profile_data_explanation": "The generated text contains the client's business name, type of business, and country, which are the same as in the reference text. However, the generated text also mentions linked accounts, which are not present in the reference text.",
"check_supporting_facts": 3,
"check_supporting_facts_explanation": "The generated text identifies suspicious indicators, such as failed transactions, transactions being processed at unusual times, and excessive chargebacks. However, the narrative of the arguments is not as clear as in the reference text.",
"check_facts_are_not_invented": 1,
"check_facts_are_not_invented_explanation": "The generated text mentions police reports and illicit activities, which are not present in the reference text. This is a clear sign of invented facts.",
"check_text_structure": 3,
"check_text_structure_explanation": "The structure of the generated text is similar to the reference text, but there is some repetition of facts and the narrative is not as clear.",
"check_conclusion": 4,
"check_conclusion_explanation": "The generated text provides a clear conclusion that summarises the suspicious activities and explains why the client's account was terminated.",
"general_score": 2.5,
"general_score_explanation": "The overall score is low due to the invented facts and the lack of clarity in the narrative. However, the profile data and conclusion checks have a higher score."
}
This evaluation method lets us differentiate between accurately and poorly generated text, offering valuable insights into the factors contributing to each outcome.
This benchmark covers various application-specific features that were ignored by the traditional metrics without requiring human labelling, thus measuring the text quality more precisely. It streamlines the evaluation process, allowing for rapid and efficient assessment of large data points without human intervention.
Limitations of using an LLM as an evaluator
It’s important to note that there are tradeoffs associated with using LLM-driven evaluators. One of the major limitations is that these metrics are application-specific, meaning they cannot be used to compare different applications or projects.
For instance, a numeric score of 3 in project A does not equate to the same score in another unrelated project. This can make it challenging to standardise metrics across different projects or contexts.
According to Zheng’s study, it is crucial to be mindful of the biases introduced by LLMs in 3 key areas when using them as evaluators:
1. Position bias: LLM evaluators tend to favour the first result when comparing 2 outcomes.
2. Verbose bias: LLM models tend to prefer longer responses, even if they lack clarity compared to shorter answers.
3. Self-enhancement bias: LLMs may prefer answers generated by other LLMs over human-authored text.
To overcome these limitations and address biases, there are a few strategies we can implement:
- Position swapping: This strategy involves swapping the reference and the result, ensuring the result is in the first position. This helps to counteract the position bias introduced by LLMs.
- Incorporating few-shot prompting: This technique involves adding a few examples or prompts to the evaluation task to calibrate the evaluator and reduce bias. This can be particularly effective for mitigating the verbose bias of LLMs.
By incorporating these strategies into the evaluation process, we can counteract the limitations of LLMs and obtain more accurate and reliable evaluations of free text and narrative-generating applications.
Testing the solution with real agents
First, we incorporated the automated LLM-driven evaluator to test the generation of narratives. We ran an initial iteration asking the agents to manually review and assess each LLM-generated narrative with a comment and a numeric score.
We found out that the automated text generation evaluation was, on many occasions, closely related to the comments and scores provided by an agent. Furthermore, the humanly stated reasons for improvements usually matched those highlighted by the automated evaluation.
Conclusion
To sum up, evaluating an LLM application generating unstructured data, such as free text, can be achieved through an LLM-driven evaluator that emulates a human evaluation process.
To accomplish this and make the results comparable, it’s essential to incorporate a set of benchmark checks into the evaluation prompt, which should output a numerical score within a predefined range. We recommend specifying and calibrating the range’s values via few-shot prompting for consistency and objectivising the scoring.
We showed the usefulness of an LLM-driven evaluator in providing quantitative and qualitative information when evaluating our financial crime report LLM free text-generating application. We created custom benchmark checks, ran a batch of automated narratives through the automatic evaluator, and compared the results with the manual observations provided by the agents.
We discovered that the automated evaluation of text generation was often consistent with the feedback and scores given by human agents. Moreover, the areas for improvement identified by humans closely matched those pinpointed by the automated evaluation.
Our findings revealed that LLM-driven evaluators have several limitations, including application-specific metrics, which make it challenging to standardise metrics across different projects or contexts. Additionally, LLMs introduce biases in three key areas: position bias, verbose bias, and self-enhancement bias. However, by employing strategies such as position swapping and adding few-shot prompting, we can counteract these limitations and obtain more accurate and reliable evaluations.
This automated evaluation method empowers data scientists to test model improvements without adding extra workload to the agents, allowing them to concentrate on reviewing final results. Overall, using an LLM-driven evaluator provides an efficient and effective way to evaluate LLM applications and improve their performance.
While the method mentioned earlier enables comparable results and guides the development in the right direction, its limitation lies in the standardisation of metrics. Since the evaluator is designed for a specific application, it cannot be generalised to multiple projects, which makes the metrics incomparable across projects.
About us
This project was an initiative driven by the SumUp Post-transaction Modelling squad. Our team focuses on building data products and machine learning solutions for continuous transaction monitoring (AML; Anti Money Laundering) and for ensuring robust merchants’ monitoring processes throughout their lifetime in the SumUp ecosystem.
Post-transaction squad members: Irati Rodriguez Saez de Urabain, Néstor Castillo, Saurabh Birari, Thomas Meißner
[Appendix A] — Synthetic example of a financial crime report narrative used for the model evaluation.
We define a human-generated financial crime report narrative as the following
Reasons for suspicion:
Suspicion was raised concerning our client “Donald Duck”. Mr Duck signed up for our service under the client category of ‘Beauty/Barber’, operating as a Limited company in Germany. Their business name was ‘DONALD DUCK BEAUTY LTD’.
All transactions, in this case, have been processed by a business based in Germany. The suspicious indicators identified in this case were as follows:
We received fraud reports against transactions carried out by the individual. These fraud reports came from a third-party service provider specialising in fraud prevention.
Our fraud department escalated the client. The investigation revealed that there were some scam alerts against this client’s transactions.
Our suspicions have been further amplified after reviewing the transaction statistics of Mr Duck’s account. During the course of the business relationship, Mr Duck processed 200 euros in successful transactions, of which 170 euros were refunded or charged back, with a further 15000 euros in failed transaction attempts. Such patterns are not compatible with the expected business activities.
The client was escalated for investigation due to the high volumes of failed transactions. Such behaviour is usually indicative of stolen cards.
During the investigation, we found that the individual was processing transactions outside regular business hours. For example, Mr Duck’s business was ‘beauty/barber’, and they had been processing transactions at 3 a.m. Such transaction patterns were incompatible with our previous knowledge of the client’s activity and expected behaviour.
The client was asked to provide proof of business during the business relationship. However, the client was unable to substantiate their business activity.
We define an accurate output of the LLM-generated financial crime report narrative as follows
We have been contacted by the German police notifying us about the client’s illicit activities. Namely, the police have indicated that the client has been involved in several fraudulent transactions. The police department has provided us with specific details of the fraudulent activities, which include an unusually high number of chargebacks against the client’s transactions. Furthermore, the police have highlighted that multiple failed transactions and transactions were being processed at 12 a.m., which indicates fraudulent activities.
Our fraud department escalated the client. The investigation revealed an unusually high number of failed transactions. Although failed transactions are a part of any business operation, we have previously identified that the businesses that receive excessive numbers of failed transactions are involved in illicit activities. Our suspicions have been further amplified after reviewing the transaction statistics of Donald Duck’s account. During the business relationship, Donald Duck processed 200 euros in successful transactions, of which 170 were refunded or charged back, with a further 15000 euros in failed transaction attempts. Such patterns are not compatible with the expected business activities.
In addition to the police request on Donald Duck’s account, there were fraud reports on some linked accounts listed above. Therefore, based on the information provided to us by the police and the findings of our own investigation, we have reason to believe that Donald Duck has been involved in fraudulent activities, and we have taken the necessary steps to terminate the client’s account.
