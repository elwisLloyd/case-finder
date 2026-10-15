# Advancing Menu Content with AI: How DoorDash uses AI to generate menu descriptions

Источник: https://careersatdoordash.com/blog/doordash-ai-menu-descriptions/

Our mission at DoorDash is to empower local businesses of all sizes to thrive and grow in the digital age. For small and local restaurants, crafting enticing, high-quality menu item descriptions is more than a nice-to-have; it's a crucial driver of online visibility and customer conversion. A well-written description can entice a diner to try something new or help them feel confident about their order, especially when browsing unfamiliar dishes. For many busy restaurant owners, however, writing detailed descriptions for every menu item can be daunting and time-consuming, pulling them away from the already demanding responsibilities of daily operations.
To solve this, we engineered a production-grade AI system that doesn't just generate mundane descriptions. Instead, it closes the loop from data retrieval to personalized generation to continuous quality evaluation. As shown in Figure 1, our innovation lies in how we combine three pillar systems into a single, robust pipeline:
1. A retrieval system that extracts large amounts of relevant and accurate input data — even when information is sparse — by leveraging multimodal signals and similar items within the same cuisine.
2. A learning and generation system that helps ensure accuracy and personalization, adapting to each restaurant's unique voice and culinary style.
3. An evaluation system that incorporates a feedback loop to blend automated and human review, helping to ensure quality and drive ongoing improvement.
Challenge: Generate both accurate and personalized descriptions
While AI has made content generation scalable, it is far from trivial to build a system that produces personalized, high-quality menu item descriptions at scale. Among the core challenges are:
- Retrieving authentic, detailed item information — especially for items with little or no existing data (similar to a cold-start problem)
- Ensuring quality and personalization during generation so that every description feels true to the merchant
- Evaluating and improving the quality of AI-generated descriptions over time
Our tightly integrated, three-pillar architecture provides a solution that addresses each challenge head-on.
Pillar 1: Intelligent retrieval
High-quality input lays the foundation for high-quality AI output. Our retrieval system uses a multimodal approach to gather the richest possible context for every menu item:
- Structured data extraction: We mine item options such as protein choices or sizes, item categories, and other metadata to provide essential context.
- Vision model integration: For items with photos, we use computer vision to extract ingredients and cooking methods, grounding the description in what diners actually see.
- Similarity-based retrieval: When we lack direct information, we create embeddings for the target item and retrieve top-matching descriptions from similar items within the same cuisine. This allows the system to learn from the common characteristics of related dishes, even in cold-start scenarios.
This retrieval-first approach ensures that every description is built on a foundation of accurate, relevant, and diverse data — never "garbage in, garbage out."
Pillar 2: Learning and generation
A great menu description is both accurate and personalized. It should clearly describe the item and reflect the unique voice and culinary identity of the restaurant. As shown in Figure 2, our generation system achieves this through a number of techniques, including:
- Conditional prompting: Prompts are dynamically assembled based on available data such as options, photos, or similar items, ensuring the model is always grounded in the right context.
- In-context and few-shot learning: We inject relevant examples from similar merchants and cuisines directly into the prompt, enabling the model to "write like a merchant."
- Retrieval-augmented generation (RAG): When data is sparse, we enhance prompts with relevant descriptions from similar items. Using a vector-similarity search, we retrieve top-matching dishes within the same cuisine and feed their descriptions to the model to fill in the blanks and maintain cultural or culinary accuracy.
- Real-time customization: Merchants can generate and refine descriptions instantly, choosing from multiple tones such as descriptive, concise, playful, or enthusiastic to match their brand identity, as shown in Table 1. Our low-latency infrastructure enables sub-second response times, making real-time iteration seamless.
This system allows us to deliver high-quality, customized descriptions at scale, capturing the diversity and uniqueness of thousands of restaurants from ramen shops to vegan bakeries.
Pillar 3: Evaluation and feedback
Creating a description is just the beginning. To ensure it’s accurate, readable, and relevant, we need to establish quality controls programmatically at scale. A successful evaluation system for AI-generated content requires a hybrid approach that combines the speed and consistency of automatic quality control with the nuanced judgment of human reviewers. The key to improving efficiency lies in establishing robust feedback loops that enhance both human decision-making and machine learning. Before deploying each model, we use A/B testing to confirm that our AI descriptions generate positive business impact to ensure we're moving in the right direction.
As shown in Figure 3, our tested hybrid system includes:
- Automated quality control: Our pipeline flags outputs that don't meet length or format requirements, contain irrelevant or generic language, or appear hallucinated. These filters uphold baseline quality before any description reaches a customer.
- Human-in-the-loop review: Human reviewers play a central role in validating content, tuning system behavior, and providing nuanced feedback that automation can't capture. During development, we compare outputs from different strategies. Before launch, we conduct live menu reviews, while after launch we monitor feedback and retrain as needed.
- A/B testing validation: Before scaling any model, we conduct rigorous A/B tests to measure business impact, ensuring our AI descriptions drive meaningful improvements in customer engagement and merchant success.
- Continuous feedback loop: We create a virtuous cycle through combining automated evaluation for scale and human insight for nuance. Every round of feedback helps us refine prompts, retrain models, and raise the bar for quality.
Stay Informed with Weekly Updates
Subscribe to our Engineering blog to get regular updates on all the coolest projects our team is working on
Please enter a valid email address.
Thank you for Subscribing!
Bringing it all together: A blueprint for scalable, accurate AI content
Our three-pillar approach — intelligent retrieval, personalized generation, and continuous evaluation — forms a complete, production-grade loop. This architecture enables us to:
- Solve the cold-start problem for items with little or no data;
- Deliver accurate, relevant descriptions that align with restaurant culinary style and allow merchants to customize their tone;
- Maintain and elevate quality through a robust feedback loop.
By thoughtfully combining these innovations, we’re enhancing the way menu content is created at scale — supporting local businesses in presenting their offerings online, helping diners make more informed choices, and advancing the capabilities of AI-driven menu solutions.
Moving forward, we aim to refine our models even more, further enhancing the quality of each generated description. We plan to expand this technology to other areas, empowering merchants to showcase their offerings more effectively and enabling them to continue to elevate their presence on the platform.
Acknowledgments
Special thanks to our cross-functional partners Andrew Kritzer, Christina Lu, Doris Li, Dylan Estes, Hemant Sharma, Kaila Lee, Michelle Ma, Sameer Salim, and Tiffany Taimoorazy who all worked together to make this exciting work happen.
