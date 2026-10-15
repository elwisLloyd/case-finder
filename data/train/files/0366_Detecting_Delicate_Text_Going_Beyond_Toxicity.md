# Detecting Delicate Text: Going Beyond Toxicity

Источник: https://www.grammarly.com/blog/engineering/detecting-delicate-text/

Protecting users from harmful communications is something we care about deeply at Grammarly. For that reason, our research has recently explored the concept of sensitive, or “delicate,” text. This is writing that discusses emotional, potentially triggering topics.
While there has been a lot of research into detecting and combating toxic text in recent years, we’ve seen a gap when it comes to the broader category of delicate text, which may not be characterized as toxic but still presents a risk. To address this, Grammarly researchers have developed a benchmark dataset of delicate texts, DeTexD, which we’ve used to evaluate the strengths and limitations of different delicate text detection techniques.
In this article, we summarize the results from our paper, “DeTexD: A Benchmark Dataset for Delicate Text Detection,” by Serhii Yavnyi, Oleksii Sliusarenko, Jade Razzaghi, Olena Nahorna, Yichen Mo, Knar Hovakimyan, and Artem Chernodub. This paper was published through the Association for Computational Linguistics’ 7th Workshop on Online Abuse and Harms. A link to the paper and other artifacts, along with an ethics statement, can be found at the end of this article.
What is delicate text?
We define delicate text as any text that is emotionally charged or potentially triggering, such that engaging with it has the potential to result in harm.
Delicate text may not be explicitly offensive and may contain no vulgar language, but it carries a risk for users or agents (e.g., LLMs) that are exposed to it. This risk varies; some delicate texts are highly risky, such as texts about self-harm or content that promotes violence against certain identity groups, while others are less risky, such as text that discusses a controversial political topic in a measured way.
Delicate texts cover various subjects, with topics ranging from race, gender, and religion to mental health, socioeconomic status, and political affiliations. There is no clear border between delicate text and toxic text, and it’s possible for text to fall into both categories. Examples of delicate texts can be found in our paper.
List of delicate text topics
Building a dataset of delicate texts
To source data, we used the following techniques:
- Domain specification: We specifically targeted news websites, forums discussing sensitive topics, and generally controversial forums.
- Keyword matching: We developed a dictionary of delicate keywords along with a severity rating for each keyword. We used this dictionary to further refine our dataset and extract delicate texts covering a variety of topics and levels of risk.
The annotation of datasets containing delicate text presents a unique challenge given its subjective nature. To mitigate this, we provided annotators with detailed examples and instructions, which can be found in our paper. We also used a two-step annotation process: annotators first identified whether texts were delicate or not, and then rated the risk level of delicate texts. All annotators were expert linguists with previous experience in similar tasks; the final label was decided by majority vote.
The result was the labeled DeTexD Training dataset of 40,000 samples and the labeled DeTexD Benchmark dataset of 1,023 paragraphs.
Experiments
With these new datasets in hand, we were eager to experiment with training a model to detect delicate text. We began by fine-tuning a classification model on the DeTexD Training dataset. As our base model, we used the RoBERTa-based classifier (Liu et al., 2019a); more details on the setup are in our paper.
Our theory was that delicate text detection and toxic text detection are two distinct tasks. To test this, we evaluated our model on several canonical toxic text datasets. While there is some overlap (hate speech is both toxic and delicate), our model tends to be more permissive around texts that contain profanities that are not related to a sensitive topic. On the other hand, our model tends to classify texts dealing with topics like race, violence, and sexuality as delicate, even though these texts may not be labeled as toxic. Ultimately, “toxic” and “delicate” are very different concepts.
Due to differences in definitions, we hypothesized that approaches to detect hate speech will underperform on the DeTexD Benchmark dataset, compared to our baseline model. We evaluated several methods on precision, recall, and F1 score (a metric that combines precision and recall).
| Method | Precision | Recall | F1 | 
| HateBERT, AbusEval | 86.7% | 11.6% | 20.5% | 
| HateBERT, AbusEval# | 57% | 20.2% | 62.9% | 
| HateBERT, HatEval | 95.2% | 6.0% | 11.2% | 
| HateBERT, HatEval# | 41.1% | 86.0% | 55.6% | 
| HateBERT, OffensEval | 75.4% | 31.0% | 43.9% | 
| HateBERT, OffensEval# | 60.1% | 72.6% | 65.8% | 
| Google’s Perspective API | 77.2% | 29.2% | 42.3% | 
| OpenAPI content filter | 55.0% | 64.0% | 58.9% | 
| OpenAPI moderation API | 91.3% | 18.7% | 31.1% | 
| Our baseline model | 81.4% | 78.3% | 79.3% | 
Performance of various methods on the DeTexD Benchmark evaluation dataset. After receiving valuable feedback from reviewers, we calibrated optimal thresholds for F-score for several methods (marked with #).
As methods apply a more broad and permissive definition of toxicity, they tend to perform better at detecting delicate texts. OffensEval from Caselli et al., 2021, for example, uses this definition: “contains any form of non-acceptable language (profanity) or a targeted offense, which can be veiled or direct.” Google’s Perspective API has a similar definition that includes a wide range of categories.
However, none of the toxic language detection methods that we studied perform very well at detecting delicate text. The evaluated methods either miss coverage, specifically on medical and mental health topics, show lower precision on examples that contain offensive keywords (but aren’t deemed delicate according to our definition), or both.
We hope that datasets like DeTexD can help lead to safer AI by broadening how and where we look for potentially harmful content.
Conclusion and ethics statement
Hate speech, offensive language, and delicate texts are sensitive and very important matters. In this research, we’ve tried to dive deeper into the challenges and opportunities of delicate text detection.
We’ve made our annotation guidelines, annotated benchmark dataset, and baseline model publicly available. Please note that we do not recommend using these artifacts without proper due diligence for privacy, security, sensitivity, legal, and compliance measures.
Due to the nature of the subject matter, the DeTexD Benchmark dataset includes a variety of uncensored sensitive content, such as hate speech, violence, threats, self-harm, mental health, sexuality, and profanity. Our paper includes keywords and partial text examples of the same type. The most extreme occurrences of such examples in the paper are partially obscured with asterisks, but the semantics are retained.
You can find more information about Grammarly’s research team here. If our work sounds like a good fit for you, consider applying to join—we’re hiring!
Link to paper: DeTexD: A Benchmark Dataset for Delicate Text Detection
Artifacts:
