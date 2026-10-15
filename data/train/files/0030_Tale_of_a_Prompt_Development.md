# Tale of a Prompt Development

Источник: https://medium.com/mercadolibre-tech/tale-of-a-prompt-development-c133081bca1e

Tale of a Prompt Development
Our Journey Building Solutions with AI at Mercado Libre
This isn’t your typical guide to prompt engineering. Here, you won’t find standard lessons on few-shot prompting techniques, nor detailed explanations of the “chain of thought” methodology, and certainly no acronyms like CRAFT, CREATE, or CTO (Context, Task, Output). It’s not about “22 prompts you can’t live without” — though I may consider this for a TikTok post later.
Instead, this narrative describes a real-world AI solution at scale. It goes beyond standard prompting — focusing on the effective orchestration of multiple LLMs, the sequencing of their interactions, cost optimization for scalability, and the design of a robust system capable of achieving human-level performance on a task critical to several key initiatives.
In the first part of this article, I will share the context around the problem we’re addressing. Afterward, I’ll walk you through our systematic design approach to developing an AI-powered solution that could operate at scale.
General Setup
This is indeed the classic product-matching challenge: having multiple items and wanting to know which ones are the same. Why? Because sellers, competitors, and providers can each follow their own logic when creating listings. While items may look alike, they can also vary significantly: photos taken from different angles, titles written with creative variations, and attributes described in inconsistent ways. Even standardized identifiers like EAN (European Article Number) codes, which should provide reliable matching, can differ wildly! 😕
So, we need an algorithm that can cut through the noise, identify similar products, and determine whether they’re truly identical — much like a detective who can spot identical twins even when they’re dressed differently!
The use cases are plenty: personalizing the store, displaying relevant ads, diversifying search results, optimizing inventory by promoting variety, and powering pricing or promotion recommendations. As trivial as it may sound, solving this problem is incredibly valuable in the e-commerce world.
Our Approach
The method goes like this:
- Get the Target Item: Select the specific item requiring matching.
- Use Different Open Source Embedding Models: Employ a variety of embedding models to encode the features of each item effectively.
- Find Candidates with ANN Algorithms: Deploy Approximate Nearest Neighbors (ANN) algorithms to quickly identify potential matching candidates.
- Evaluate Candidates with an ML Model: Process these candidates through a machine learning model to calculate match probabilities.
- Conduct Human Oversight: In certain scenarios, especially for sensitive products and use cases, a human reviews the ML model’s results for confirmation.
Behind the scenes, there’s a lot more going on. Our system incorporates multiple components, such as vector databases, data preprocessing pipelines, and a network of APIs that streamline each step of the flow. But as you might have noticed, there’s still a part of the process that isn’t fully automated.
So, where does the human in the loop come in? Take pricing, for example — if we’re going to change the price of an item to stay competitive, a wrong product match could be extremely costly. Our experience with pricing strategies has shown that, simply put, in some specific and high-stakes use cases, pure machine learning isn’t yet accurate enough to operate autonomously.
And believe me, the ML model we built to try to eliminate manual review was anything but basic. It combined advanced NLP techniques, multiple embeddings for both images and text, and attribute enrichment — a sophisticated system developed over years by our team.
Still, all this firepower under the hood wasn’t enough to fully automate the process.
All started creating a prompt
Drawing from our extensive experience with LLMs at Mercado Libre, where we had developed several prompts tailored to different use cases (see our lessons learned and our methodology), we approached the new challenge using standard prompt engineering techniques. Our first attempt? A three-step pipeline of LLMs. Unfortunately, the initial results were disappointing, with precision at 38% and recall at 13% — significantly below our existing ML model’s performance. After some days of refining the prompt, precision jumped to 65%, and recall soared to 79%. With models improving rapidly and costs declining, it was clear that we were moving in the right direction.
We weren’t just optimizing for performance; the solution also had to stay within a tight cost threshold to be truly scalable, especially given that we were evaluating millions of items and matches.
Shaping the Strategy
We followed an iterative approach based on the methodology in Jurafsky & Martin’s (2025) “Speech and Language Processing” playbook. The process includes running the prompt on a sample of training examples, identifying failure cases where the results don’t meet expectations, modifying the prompt to address these issues, and then generalizing it to prevent overfitting and ensure it works more broadly.
We started small and smart by putting this plan into action with datasets containing 50, 500 and 5,000 human-labeled examples. You might wonder why we used such small samples. The answer is simple: True improvement often comes from scrutinizing individual failures so we can identify patterns and make generalizations. When you can look at each mess-up in detail, you start seeing patterns you can fix.
Along the way, we tweaked prompts, adjusted the flow, and split or merged tasks, whatever the iteration required.
Get Camilo Ernesto Martínez’s stories in your inbox
Join Medium for free to get updates from this writer.
Iteration
So it wasn’t just about getting each individual prompt right; we had to orchestrate how these AI players would work together in perfect harmony. Plus, we needed prompts that could handle everything from designer handbags to tech gadgets without breaking a sweat!
The complexity of the project unfolded across three main dimensions:
- Designing the LLM nodes and their interactions
- Crafting and refining our prompts
- Selecting the right models/providers
Think of it like cooking a gourmet meal — you need the right ingredients (models), the perfect recipe (prompts), and the know-how to bring it all together (orchestration). And just like any good chef, we had to taste-test and adjust along the way! 👨🍳
This diagram illustrates various LLM configurations, each color representing a different model/provider. Thanks to our in-house LLM orchestration system (“Verdi”), we could rapidly iterate and produce multiple experimental versions daily. Key insights from our process included:
- Trial and error was our core strategy: Breaking down tasks into structured, human-like steps and allowing the models space to reason significantly improved performance and outcomes.
- Incremental improvements were essential: Rather than adjusting every component simultaneously, we worked systematically, focusing on one aspect at a time. This allowed us to isolate precisely which changes led to better or worse outcomes.
- Dealing with model inconsistency was paramount: Simpler models run twice outperformed complex models in reliability.
- Prompting approaches varied in effectiveness: Automated prompting tools were not as useful as we had initially thought. However, explicitly asking the LLM for feedback (e.g., “Here’s my prompt and the error I’m getting; what should I change?”) returned surprisingly valuable suggestions.
- Reflection significantly improved results: Encouraging models to explain or justify their responses helped their internal reasoning process and also made it clearer to us how the models arrived at their conclusions. Reflection benefited not just performance but also the interpretability and communication of LLM outputs.
- Starting powerful brought results, optimizations could wait: Testing initially with more powerful models proved effective. Once we achieved good results, we could scale down carefully until the system met cost requirements, resulting in greater confidence and overall efficiency.
- Approaching sensitive or extreme cases cautiously ensures reliability: Identifying challenging or sensitive examples provided us with valuable benchmarks. These samples were instrumental in detecting overfitting and ensuring genuine improvements in generalization.
The path wasn’t linear. Some days brought significant progress; on others, improving one metric — like precision — came at the cost of another, such as recall. These trade-offs often forced us to reconsider even the smallest changes. At times, days of work led to dead ends, requiring full rollbacks. As our performance graphs show, the trajectory of improvement was more of a roller coaster than a steady climb.
Ultimately, this exhaustive and iterative process yielded remarkable results. We reached our target, which was ambitious: 95% precision and at least 50% recall, with a cost of less than $0.001 per request — a threshold necessary for ROI-effective scalability across millions of items. This success demonstrated that carefully crafted prompts and strategic model selection could deliver both high performance and economic viability at scale.
We hit human-level performance with a more reliable, consistent, and cost-effective autonomous method that allows us to scale the process and reach new use cases.
Costly errors
Throughout our development journey, we came across critical lessons about managing costs in AI services. It’s important to note that token counts and input processing methods vary widely among providers. Some assess tokens on a pixel-by-pixel basis, while others enforce strict character limits, which can lead to unexpected costs during experimentation. Midway through our tests, we had to implement specific controls to keep our budget in check. This experience serves as a valuable reminder that Gen AI services, like any on-demand solution, require robust safeguards to scale production without incurring costly errors. 🚨
Summary of the system evolution
Looking at how far we’ve come, this journey has been mindblowing! Our system evolved from an initial 2-node configuration to a sophisticated 7-node architecture with enhanced capabilities. Beyond mere expansion, we implemented significant improvements, including adaptive prompts, context-aware decision-making processes, and collaborative consensus mechanisms between nodes.
Conclusion: Let’s Talk About What Made Our AI Tick
So yes, the trick wasn’t just because we wrote some clever prompts. It was more like conducting an orchestra — we had these awesome embeddings, some pretty smart ML models, super-fast databases, and our LLMs all jamming together.
We realized that the real game-changers won’t come from one breakthrough moment — they’ll come from bringing together lots of smart pieces, each one doing what it does best. It’s not about solo performances anymore — it’s about the whole band playing together.
And hey! There are still several manual processes in Meli where we think we can sprinkle this magic! We’re diving headfirst into image and video generation in depth, but completely reimagining marketing… well, that’s a whole different story that deserves its own spotlight. Stay tuned for more exciting updates!
