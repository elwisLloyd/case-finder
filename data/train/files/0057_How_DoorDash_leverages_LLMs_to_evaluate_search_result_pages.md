# How DoorDash leverages LLMs to evaluate search result pages

Источник: https://careersatdoordash.com/blog/doordash-llms-to-evaluate-search-result-pages

At DoorDash, delivering relevant and high-quality search results is essential to ensure that customers find what they’re looking for quickly and effortlessly. Traditionally, evaluating search relevance relied on human annotations, which posed challenges in scale, latency, consistency, and cost. To solve this, we built AutoEval, a human-in-the-loop system for automated search quality evaluation that is powered by large language models (LLMs). Through leveraging LLMs and our whole-page relevance (WPR) metric, AutoEval enables scalable, accurate, and near-real-time search result assessments.
AutoEval has accelerated iteration cycles, improved consistency, and achieved strong alignment with human judgments, even outperforming crowd annotators in key categories. While the system significantly enhances efficiency, it frees up expert raters to focus on guideline development, edge cases, and calibration.
Why traditional search evaluation doesn’t scale
It’s helpful to understand the limitations of traditional human-driven relevance annotation before we dive into the details of AutoEval and WPR. For years, DoorDash and many others relied on human labelers to evaluate — query by query — the quality of search results. While effective in small batches, this approach simply cannot scale with the burgeoning complexity and size of modern search systems. Among the challenges are:
- Scalability constraints: It isn’t feasible to manually assess millions of query-document pairs, especially as search evolves daily.
- Slow feedback loops: Human annotation cycles can take days or weeks, slowing iteration speed for search improvements.
- Inconsistent ratings: Each human rater interprets guidelines differently, leading to label noise and requiring calibration.
- Limited coverage: Annotated datasets overrepresent high-frequency, or head, queries, while underrepresenting tail queries, where relevance problems often hide.
These limitations became increasingly costly as DoorDash scaled to support diverse verticals, including restaurants, retail, grocery, and pharmacy.
Enter LLM-powered evaluation
To overcome these challenges, we transitioned to an evaluation approach powered by LLMs capable of delivering scalable, consistent, and near-real-time relevance judgments. LLM-powered evaluation unlocks:
- Automated assessments of millions of relevance judgments per day.
- Faster iteration on new ranking models, filters, and user interface (UI) changes.
- Broader coverage across head, torso, and tail queries.
- Consistent reasoning grounded in well-structured prompts and guidelines.
Paired with human oversight and auditing, LLMs became a powerful tool to scale our evaluation capability without sacrificing quality.
Whole-page relevance: Measuring the page, not just the result
We developed our WPR metric to align with what users see and engage with so that we could rigorously evaluate a search page’s usefulness. This custom metric is designed to evaluate the entire search impression, not just individual results. It builds on the idea behind normalized discounted cumulative gain (NDCG) but adapts the concept for a 2-D user interface.
Unlike NDCG, which evaluates a vertical list, WPR measures multiple content blocks arranged spatially on the screen, including stores, dishes, and items. As shown in Figure 2, each content type is weighted by its visual prominence and expected user impact, which is similar to how we assign real estate value on the DoorDash app. This lets us measure how successfully the entire page, not just the top result, fulfills a user's intent.
WPR supports full-stack search evaluation across all stages, including:
- Retrieval: Are the right candidates being retrieved?
- Ranking: Are results presented in the most useful order?
- Post-processing: Are filters and blends improving relevance?
- User experience composition: Does the layout guide the user effectively?
Two key WPR applications
- Offline feature evaluation: When launching a new ranking model, processing logic change, or UI update, we use WPR to assess its offline impact before rollout to online A/B testing. This helps detect regressions or confirm improvements with confidence.
- Continuous production monitoring on relevance: We use the WPR score daily to measure search relevance and capture quality signals beyond user engagement and system performance.
Introducing AutoEval: LLM-powered evaluation at scale
As DoorDash’s search system scaled to support multiple verticals – from restaurants to retail to pharmacy – and increasingly complex UI layouts, evaluating relevance across such a diverse and dynamic landscape became a major engineering challenge. While useful, manual human annotation was too slow to keep pace with fast iteration cycles and real-time production needs.
To address this, we built AutoEval: a human-in-the-loop, LLM-powered evaluation system designed to assess search relevance quickly, scalably, and consistently. AutoEval has become a critical part of how we evaluate everything from offline experiments to daily production traffic.
How AutoEval works
As shown in Figure 3, AutoEval’s architecture is designed to turn a query and its corresponding search results into structured tasks that are evaluated by LLMs. Each judgment is rolled up using our WPR metric to give the search result page a holistic score.
AutoEval supports a full evaluation pipeline, including:
- Query Sampling: We sample real user queries from live traffic across intent, frequency, geographic, and daypart dimensions.
- Prompt construction: Each query-result pair is converted into a structured prompt tailored to the evaluation task such as dish-to-store or cuisine-to-store.
- LLM inference: The prompt is passed to an LLM, base or fine-tuned, which returns a structured relevance judgment.
- WPR aggregation: Judgments are aggregated to generate a page-level WPR score.
- Auditing and monitoring: Judgments are regularly sampled for human review to ensure quality, stability, and alignment.
Designing prompts to reflect rating guidelines
Prompt engineering is at the core of AutoEval’s effectiveness. Each prompt mirrors our internal human rating guidelines and includes structured context, such as store name, menu items, dish titles, or metadata tags, to help the LLM replicate the type of reasoning a trained human evaluator would perform.
Prompts are carefully crafted to reflect:
- The user’s query intent, for example cuisine, dish, or brand
- Document type, for example store card or item result
- Expected criteria for relevance, grounded in our expert-created rating rubrics
Over time, we experimented with various prompting strategies, including zero-shot, few-shot, and structured templates. We found that task-specific structured prompts paired with rule-based logic and domain-specific examples offered the most consistent, interpretable, and human-aligned results.
In addition to structure, we employ several prompt techniques that enhance LLM judgment quality, including:
- Chain-of-thought reasoning: We explicitly break down rating tasks into multi-step logic — for example, exact match → substitute → off-target — so the model can reason in stages. It is designed to mirror this thought process using inline instructions and fallback reasoning, allowing the LLM to simulate the evaluator’s decision-making process step-by-step.
- Contextual grounding: Prompts include rich, structured metadata such as geolocation or store menu to mimic what a human would review.
- Embedded guidelines: For complex domains like food or retail stores, we incorporate fragments of evaluation criteria directly into the prompt as in-context instruction.
- Alignment with internal rubrics: Prompts reflect the same conditional logic and categories used by internal and crowd raters, ensuring interpretability and calibration across judgment sources.
Fine-tuning with expert-labeled data
In addition to prompt engineering, we fine-tune our LLMs on high-quality, human-labeled data for key evaluation categories.
This process starts with internal DoorDash experts, who generate relevance annotations following well-defined guidelines. These labels form our golden dataset, which we split into training and evaluation sets for fine-tuning models and benchmarking their performance.
It is critical to have experts justify their annotations to ensure the model not only learns the correct label but also the reasoning behind it. These justifications guide prompt refinement, reveal ambiguous cases, and help align model behavior with human expectations.
Fine-tuned models improve alignment in high-impact categories such as:
- Store name search: Analyzes store category and menu overlap to determine if the store result accurately matches what was intended.
- Cuisine search: Identifies relevant items from the menu to evaluate whether a store satisfies a cuisine-based query.
- Dish/item search: Finds close or exact menu matches to assess whether a store offers the queried dish or item.
Human-in-the-Loop: Auditing and iteration
While the fine-tuned model drives scale, we keep human expertise in the loop through structured auditing. First, external raters review a sample of LLM-generated judgments, flagging low-quality outputs which internal experts then investigate. This effort leads to prompt improvements, creation of new golden data, and ongoing fine-tuning and evaluation. The resulting tight feedback loop looks like this:
- Internal experts generate golden data.
- Model is fine-tuned and evaluated.
- External raters audit outputs.
- Experts analyze flagged outputs and refine prompts or labels.
- Loop continues with improved models and better-aligned prompts.
Stay Informed with Weekly Updates
Subscribe to our Engineering blog to get regular updates on all the coolest projects our team is working on
Please enter a valid email address.
Thank you for Subscribing!
Key wins and impact
AutoEval has delivered substantial improvements across DoorDash’s relevance evaluation life cycle, enabling us to scale faster, iterate more confidently, and focus human expertise where it matters most.
- Throughput and turnaround time: AutoEval has reduced relevance judgment turnaround time by 98% compared to human evaluation, unlocking a nine-fold increase in capacity and resolving a major bottleneck in our offline experimentation pipeline.
- Efficiency: AutoEval has freed expert raters from repetitive labeling tasks, allowing them to focus on guideline development, auditing, and edge case resolution, which has raised overall quality and consistency of our evaluation standards.
- Accuracy: Fine-tuned LLMs consistently match or outperform external raters in key relevance tasks, including store name and dish-level search satisfaction.
These wins have transformed how we evaluate, monitor, and improve the DoorDash search experience, turning what was a slow, manual process into a fast, scalable, and efficient structure.
Future directions
While AutoEval has already transformed how we evaluate search relevance at DoorDash, we’re just getting started. We have several exciting areas on our roadmap that will push accuracy, flexibility, and scalability even further, including:
- Decoupling from a single LLM provider via internal gateway: We plan to migrate from directly calling OpenAI’s public API to routing traffic through our internal GenAI gateway. This abstraction layer will allow us to compare performance flexibly across multiple LLM vendors, enabling experimentation with cost, latency, and accuracy trade-offs without changing downstream systems.
- Exploring in-house LLMs for greater control and cost efficiency: In collaboration with DoorDash’s machine learning research team, we’re exploring the feasibility of training and deploying in-house LLMs optimized for our specific search evaluation tasks. This could unlock further scalability, model efficiency, and cost reductions while allowing tighter alignment with DoorDash-specific language patterns and domain expertise.
- Enhancing prompt context with external knowledge sources: To better handle tail queries and unfamiliar entities, we plan to enrich prompts using external data sources. For instance, if a user searches for a local store that hasn’t yet onboarded with DoorDash, we could fetch additional context — say, from external search APIs — about the store and its menu to allow the LLM to make a more informed relevance judgment even with limited internal data.
Conclusion
AutoEval demonstrates how a thoughtful combination of LLMs, prompt engineering, and human expertise can create a scalable, reliable, and efficient evaluation system. By powering both offline iteration and real-time relevance monitoring, AutoEval is helping DoorDash deliver better search results faster and more intelligently while maintaining the human judgment that underpins our quality standards.
Acknowledgements
Huge thanks to Minjie Zha, Shubhanshu Mishra, Raghav Saboo, Luming Chen, Eduardo Martinez, and Archit Bose for their engineering contributions. We also are grateful to Juchuan Ma, Prasad Sriram, Rui Hu, Hanning Zhou, and Bruce Wang for their thoughtful leadership and guidance throughout the project.
Thanks also go out to Alex Levy for product direction, and to Ariana Rudina, Christian Lai, and Kunal Moudgil from strategy and operations for their strategic insights. Additionally, we are grateful for Shyam Parikh’s analytics expertise, which helped inform key decisions.
Finally, many thanks to Robby Kalland and Marisa Kwan for their continuous support in reviewing and editing this article.
