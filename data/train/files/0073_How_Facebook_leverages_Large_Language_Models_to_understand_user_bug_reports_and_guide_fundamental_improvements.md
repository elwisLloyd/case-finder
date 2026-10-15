# How Facebook leverages Large Language Models to understand user bug reports and guide fundamental improvements

Источник: https://medium.com/@AnalyticsAtMeta/how-facebook-leverages-large-language-models-to-understand-user-bug-reports-and-guide-fundamental-70ab26475850

How Facebook leverages Large Language Models to understand user bug reports and guide fundamental improvements
Authors: Akos Lada, Xiaoxuan Liu, Yuchen Shao, Yi Wang, Rion Graham, Bee Padalkar, Charlie Walker, Molly Lewis
At Meta, we focus on optimizing the user journey by leveraging data-driven analytics to identify, quantify, and address key pain points throughout the experience. We value user feedback as a crucial component of our product development and optimization process. User feedback typically comes in unstructured formats, such as free-text descriptions, making it challenging to process and analyze at scale using traditional methods. The emergence of Large Language Models (LLMs) such as Llama, has been a breakthrough in this regard. By harnessing the power of LLMs, we have significantly improved our ability to measure and interpret feedback, enabling us to identify system issues more effectively and implement impactful product changes.
In this article, we’ll dive deeper into how we started leveraging the large language model to analyze user-filed bug reports and how it helps us prioritize efforts and identify opportunities to improve product quality and make fundamental changes. While this post details Facebook’s approach specifically, many other organizations within Meta are adopting a similar approach.
First, some basic terminology
- Large Language Model (LLM): a type of artificial intelligence (AI) program that can recognize vast amounts of text data and perform natural language processing tasks with a high level of accuracy.
- User Feedback Bug Reports: are the reports submitted by users through an in-app mechanism, such as shaking the phone. It usually contains text descriptions. This provides a vital source for understanding users’ pain points.
- Unstructured Data: information that doesn’t follow a predefined format or structure, such as text documents, images, etc.
- Dashboard: a way of displaying various types of visual data in one place, to track the progress and facilitate informed decision-making.
The benefit of LLM
How do we typically analyze the bug reports?
Traditionally, we rely on human reviewers and traditional machine learning models to analyze bug reports. While providing valuable insights, the human-review approach tends to be resource-intensive, challenging to scale, and harder to generate timely insights. Though traditional machine learning models offer some advantages, they sometimes fall short in processing and interpreting unstructured data directly. This is where large language models (LLMs) excel.
Our idea was to leverage LLMs to transform how we analyze user feedback, unlocking several key benefits:
- Understand complex and diverse user feedback at scale.
- Uncover patterns through daily monitoring via dashboards.
- Identify evolving issues to enable proactive mitigation strategies.
- Analyze root causes of user complaints to drive product improvements.
This innovative approach allows us to gain deeper, actionable insights and address user needs more effectively.
Case Studies
As an example, during a technical issue that caused external products and internal systems to be down for multiple hours, users experienced difficulties accessing our Family of Apps. Our LLM based approach immediately detected that and noticed that users were mainly complaining about “Feed Not Loading”, “Can’t post”, etc in bug reports, alerting to an issue.
Get Analytics at Meta’s stories in your inbox
Join Medium for free to get updates from this writer.
In addition, our method primarily identified less visible bugs that might have been missed and taken longer to detect otherwise. While obvious bugs are quickly noticed and fixed, our approach helped catch additional issues and quickly fix them, ultimately reducing topline bug reports by double digits over the last few months.
Playbook: Leveraging LLMs to Analyze User Complaints and Drive Impactful Product Changes
We’re leveraging LLMs to revolutionize how we understand and address user complaints. From classifying bug reports to uncovering the root causes, our LLM-driven approach combines cutting-edge technology with actionable insights to drive impactful product changes and improve user experiences. Here’s a look at our playbook:
LLM-Based Classification at Scale
- We developed an LLM-based classification system that assigns each report to a pre-defined category. This approach ensures structured understanding of unstructured feedback while enabling daily monitoring through integrated dashboards.
- It also involves iterative prompt engineering to guide the LLM to generate optimal and accurate outputs.
Getting to this automated stage, however, required significant human expertise and iterative prompt engineering.
- Domain knowledge was essential to define meaningful categories and ensure the outputs aligned with business needs and team goals.
- At the same time, prompt engineering was an iterative and crucial process to refine the LLM’s performance. This included testing different ways of framing questions and instructions to the model to ensure it produced accurate, consistent, and actionable outputs.
- This underscores an important lesson: while LLMs have the power to automate complex workflows and make sense of unstructured data, achieving reliable and actionable results requires upfront investment in tuning and iterations. It’s the synergy between human expertise and the model’s capabilities that arrives at automatic and effective decision-making.
Trend Monitoring
- We conduct weekly reporting and trend monitoring through our LLM-powered dashboards to track shifts in user complaints and identify emerging patterns
Generative Understanding: Uncovering the “Why” Behind Complaints
- LLMs could go beyond classification. They can also be effective at ‘rationalization’ and answering “why are users experiencing issues”, helping to find root causes during outages
- This root cause understanding of user pain points enabled us to develop actionable solutions to reduce the volume of bug reports.
Inform Bug Fixes and Product Strategies.
- Leveraging LLM-guided insights, we collaborate with a wide range of cross-functional teams — including Engineering, Product Management, User Experience Research, etc. — to identify system inefficiencies and build the solutions. In some cases, these efforts also extend to cross-organizational collaboration to implement the fixes.
Scaling your solution using data pipelines and dashboards
Once we have prototyped a first version, and seen its value in influencing product decisions, we started to consider scaling the data pipeline as well as building a dashboard for providing a centralized view of key metrics. This enabled us to regularly monitor key metrics, identify trends, and pinpoint areas for improvement, ultimately driving long-term impact.
For our use cases, we’ve created privacy-compliant, aggregated long retention tables to power our dashboard, providing a robust foundation for tracking user bug reports over an extended period. This integration provides a robust platform for:
- Easy issue identification: Our dashboard visualizations offer a straightforward way to detect new issues and verify the effectiveness of fixes.
- Comprehensive analysis: Our dashboard includes multiple filter combinations, enabling users to conduct in-depth deep-dive analytics and uncover valuable insights.
- Early issue detection: Our dashboard has data quality checks and threshold monitors set up to alert us to potential issues at the earliest possible time, ensuring prompt action can be taken.
Conclusion
At Meta, we’ve developed a comprehensive playbook supported by a suite of tools to enhance how we leverage LLMs for understanding user feedback.
Already, this methodology has successfully influenced product changes, demonstrating measurable, positive impacts throughout the user journey. By applying this framework, teams across any product area can gain scalable, quantitative insights into questions that were previously difficult to address. This, in turn, would pave the way for end-to-end improvements in user experience at a company-wide level.
As AI continues to evolve, we remain committed to refining our methodology to keep pace with innovation and deliver ongoing value across our products and services.
