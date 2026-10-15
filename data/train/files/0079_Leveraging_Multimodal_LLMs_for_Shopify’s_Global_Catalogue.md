# Leveraging Multimodal LLMs for Shopify’s Global Catalogue

Источник: https://shopify.engineering/leveraging-multimodal-llms

I. Introduction
As the world of commerce rapidly evolves—shifting from browsing websites to conversing with AI agents—the need for high-quality, standardized product data has never been greater. The future of shopping increasingly looks like this: “Show me sustainable running shoes under $150”, but the answer you get depends entirely on the quality of the data the AI has access to.
For Shopify merchants, that’s both an opportunity and a challenge. Merchants need their products to be fluently understood by machines, not just humans. The challenge? Shopify hosts millions of merchants who describe billions of products in wonderfully unique ways. That diversity, while an incredible strength for commerce, is kryptonite for machine understanding.
That’s where Shopify’s Global Catalogue comes in—a new intelligence layer that unifies, standardizes, and enriches product data across Shopify. At the International Conference on Learning Representations (ICLR) 2025 Expo in Singapore, we presented the core engineering behind this initiative—how we use multimodal Large Language Models (LLMs) to organize and augment every item sold across our platform.
In this recap post of our presentation, you’ll get a technical summary of our approach: from data curation through model fine-tuning and training, to the infrastructure that lets us make 40 million multimodal LLM-powered inferences daily. We will also cover the impact of these new data pipelines across Shopify’s search, recommendations, conversational commerce, and where we are heading next.
II. The problem: fragmented product data and discovery challenges
Historically, Shopify revolved around the merchant and their shop. Each shop was an independent island, with the merchant free to create products with virtually any structure they desired. This approach dramatically lowered the barrier for entrepreneurs, and encouraged merchants’ creativity and freedom. However, this flexibility came with a few important challenges:
- Unstructured data: Most product information is provided in free-form text instead of being organized in structured and standardized fields. There is no uniformity. One merchant might give us a novel’s worth of product description, while another might provide just a title and price.
- Schema heterogeneity: Each merchant on Shopify can define their own keys (attribute names) and values for these options, leading to non-uniform data structures.
- Data quality and sparsity: Product listings can have typos, missing values, misclassifications, or irrelevant content. Structured product records may not consistently contain the correct value in the correct field (e.g., the brand of the product is listed in the title but omitted in the brand field).
- Multimodality: Information about a product may be present in text, images or videos. Key attributes may only be featured in an image and omitted from text fields.
- Multilingual: Merchants are present in every continent and leverage different languages and market terminologies.
Traditionally, this patchwork of product data leads to classic e-commerce pain points: difficulty in semantic search, poor faceting, duplicate or hard-to-find listings, and limited ability to surface the best—or most relevant—choices for buyers.
As commerce shifts toward AI-driven experiences, the impact of fragmentation becomes even more acute. Even the most advanced AI agents are limited by messy, inconsistent product data—without unified, structured information, they struggle to deliver accurate, trustworthy, and efficient product discovery experiences.
Unlocking the full potential of AI-driven commerce requires product data that machines can reliably understand, compare, and act upon at scale.
III. The solution: The global catalogue powered by multimodal LLMs
The Global Catalogue is a unified foundation for product knowledge, built to organize and enrich product data across all of Shopify. It operates through four integrated layers: product data, product understanding, product matching, and reconciliation.
Layer 1: Product data foundation
Handles the full variety, volume, and volatility of commerce data. We process over 10 million product updates daily from merchant uploads, APIs, apps, and integrations, in a streaming fashion. A custom schema-evolution system keeps data compatible as merchants innovate. A change data capture mechanism records all product modifications, enabling consistent historical views and robust incremental processing.
Layer 2: Product understanding
The product understanding layer transforms unstructured data into standardized metadata through multiple tasks:
- Product classification: Assigns each product to a hierarchical taxonomy.
- Attribute extraction: Identifies and normalizes key features such as color, size, material, brand, and model.
- Image understanding: Extracts color (as hex codes), evaluates image quality, and detects visual product attributes.
- Title standardization: Normalizes verbose merchant titles (e.g., “iPhone 16 Pro 256GB Silver” → “iPhone 16”).
- Description analysis: Summarizes descriptions and surfaces key selling points.
- Review summarization: Generates aggregated quality and sentiment signals from customer reviews.
We structure these as a multi-task, multi-entity problem. Each entity represents a different grain of the catalogue. In the diagram, we have highlighted three key entities: media, products, and variants. Other examples of entities include sellers and reviews.
For each catalogue entity, we fine-tune a vision large language model to perform multiple tasks simultaneously, rather than following the traditional approach of building separate models for each task. This architectural choice was not only efficient, we found that these tasks have strong interdependencies—category inferences provide crucial context for text summarization, while text summarization can refine classification decisions—yielding higher quality inferences than a siloed approach.
Shopify’s taxonomy
Shopify’s open-source product taxonomy defines the inference space for categories and attributes. We leverage LLMs to continuously identify new attribute and category requirements by analyzing product listing patterns, with changes validated through both automated and human-in-the-loop review. The taxonomy attributes are linked to taxonomy nodes, ensuring each product type receives relevant attributes; these propagate hierarchically and adapt as the taxonomy evolves.
Layer 3: Product matching
After understanding individual products, we must identify when different merchants sell the same item. This involves a multi-stage process to cluster related listings.
Candidate generation focuses on producing high-recall candidate clusters. We use locality-sensitive hashing, embedding-based clustering and other probabilistic methods to create fuzzier connections between products. We also identify deterministic matches through features like universal product codes and high-confidence feature combinations, such as “same-title and same-image match.”
A cascade of discriminator models validates these matches. The system maintains high-precision through what we call 'edge pruning.' After identifying candidate matches, we apply these discriminators to remove potentially incorrect edges. This is crucial because a single incorrect edge can create a large cluster of mismatched products.
We formulate the matching problem as a bipartite graph where:
- Products form the left-hand nodes
- Attributes, such as deterministic features and fuzzier candidate matches, form the right-hand nodes
By computing connected components on this graph, we obtain initial product clusters to which we assign Universal Product IDs.
Layer 4: Reconciliation
For identified product clusters, the reconciliation layer constructs a canonical product record by aggregating all inferred metadata:
- Attribute merging: Complementary data from multiple listings is combined to yield the broadest, most accurate set of attributes (technical specs, options, etc.).
- Variant normalization: Different representations of variants (e.g., color names, size choices) are standardized and unified.
- Content aggregation: Descriptions, technical information, and review summaries are merged; highest-quality media are selected to represent the item.
The resulting canonical product serves as the authoritative source for downstream systems.
All four layers depend on the use of multimodal LLMs for product understanding, entity resolution, and to create a canonical representation of each item. The following sections detail our approach to model training, data generation, and production deployment at scale.
IV. Fine-tuning for flexibility and performance
Fine-tuning LLMs involves taking a pre-trained language model and training it further on a specific dataset for a particular task. While commercial APIs like OpenAI and Gemini work well at a smaller scale, our volume makes them prohibitively expensive. We achieved better performance and control by fine-tuning smaller open source vision large language models.
We have deployed three successive open-source models: LlaVA 1.5 7B, LLaMA 3.2 11B, and currently Qwen2VL 7B. Each transition delivered higher accuracy while reducing GPU requirements. We continuously assess emerging models, weighing accuracy gains against computational costs.
Selective field extraction
Returning to our multi-task, multi-entity setup, while we found that tackling multiple tasks simultaneously led to improved performance across each individual task, we also found that asking the model to predict all fields during fine-tuning led to a loss of generalizability at inference time.
Instead of training our models to extract all fields, we adjusted our training strategy to randomly select for each training instance which fields the model should predict. During training, a model might be asked to extract only the category for one example, then category plus title for another, and perhaps just the standardized description for a third. This approach teaches the model to adapt to different extraction requirements at inference time without retraining.
The benefits of this strategy became clear in production. Not only did models trained with selective field extraction retain better generalization capabilities, but we reduced median latency from 2 seconds to 500 milliseconds. Moreover, by generating fewer tokens, we substantially reduced GPU usage by 40%, allowing us to serve more requests with the same hardware, which has made our system more cost-effective.
V. Data generation and continuous improvement
Shipping fine-tuned models starts with high-quality data for training and evaluation. We developed an annotation pipeline that combines LLM agents and human expertise.
Automated annotation pipeline:
We structure our training datasets around each individual catalog entity. We begin by sampling data and taking a temporal snapshot of the entity data. Then, for each extraction task, such as category classification, we deploy multiple LLM agents that act as annotators. These agents independently analyze the product and suggest appropriate categories.
- For test samples, suggestions from these agents are presented to human annotators using a specialized interface. Humans resolve ambiguities and provide gold labels; consensus is established for evaluation.
- For train samples, we scale up using an LLM arbitrator—another model trained to select the best agent suggestion or abstain with human fallback as needed. This balances accuracy and scalability, allowing us to build high quality datasets much faster than by relying on human annotators alone.
Test set review interface:
- Annotators see the product image(s), raw description, and LLM suggestions. They can pick, reject, or search for the best label in the taxonomy tree.
- We leverage randomization to measure and correct for bias in human annotations and to encourage searching for the correct label when none of the agent annotations are appropriate.
Comprehensive model evaluation:
Evaluating multi-task extraction models requires additional metrics that go beyond traditional machine learning metrics. We developed three categories of evaluation metrics to ensure our models perform well across all dimensions.
- Task-specific metrics: Precision/recall at multiple category hierarchy levels for classification; accuracy for attribute extraction.
- LLM judge metrics: For generative fields (like standardized title or description), synthetic “judges” grade outputs against detailed guidelines.
- Instruction metrics: Since our models must respond to selective extraction requests, these metrics measure instruction following capability.
- Field compliance rate: How often the model outputs only the requested fields.
- Field invariance rate: Consistency of answers for a given field, regardless of changes in the requested output schema.
The instruction metrics are particularly important for maintaining model accuracy. We need confidence that requesting additional fields at inference time will not change the model’s inference for previously requested information.
Continuous improvement through active learning:
We implemented an active learning loop that continuously identifies areas for improvement and incorporates new training data. The active learning system operates on two fronts.
- First, LLM judges flag low-quality inferences in production, queuing them for additional human review and retraining.
- Second, we analyze the token probability distributions of model outputs. We target samples where output token probabilities are low, signaling model uncertainty. These re-enter the training pipeline, improving robustness over time.
By identifying and retraining on these uncertain inferences, we systematically improve model performance across our corpus.
VI. Scaling and deployment infrastructure
Our inference infrastructure handles supports 40 million LLM calls daily, representing about 16 billion tokens inferred per day, through several optimization techniques:
- Triton inference server: Orchestrates model serving across our GPU fleet, handling request preprocessing, batching, and routing from multiple surfaces (admin UI, Shop app, APIs, bulk pipelines).
- Dataflow streaming pipeline: Kafka-based architecture writes inferences back to all relevant data sinks in real-time.
- FP8 quantization: Reduces GPU memory footprint while maintaining inference accuracy, enabling larger batch sizes
- Key value cache: Stores and reuses previously computed attention patterns.
- Selective field prompting: Different surfaces request only required fields, reducing median latency from 2s to 500ms and GPU token usage by 40%.
VII. Impact and future applications
The catalogue is actively integrated across Shopify’s ecosystem:
- Merchant admin: The system provides real-time suggestions on category classification and missing attributes during product creation, improving data quality at the point of entry.
- Search and recommendations: Enriched product data and universal identifiers enable better matching, faceting, and surfacing of relevant results.
- Embeddings creation: Product and variant representations, based on standardized output, inform core ML functionality for personalized ranking and recommendations.
The Catalogue has already begun to unlock a powerful set of downstream benefits:
- Search: Canonicalized, enriched product metadata means semantic and keyword queries (e.g., “best local coffee in Singapore”) return diverse, high-relevance results—including long-tail gems, not just well-known brands.
- Personalization: The unified product catalogue enables advanced recommendation systems, using user interaction data and standardized attributes for surfacing of products, bundles, and merchants that match individual interests.
- Conversational commerce: AI assistants (e.g., Shopify Sidekick, Shop app’s chat) rely on catalogue data as structured context, guiding users through dynamic, needs-based shopping workflows—mimicking the expertise of an in-store associate.
- Multi-channel integration: Having a common schema and universal product IDs makes Shopify’s ecosystem interoperable—not just internally, but across channels, partners, and emerging marketplaces. Our open-source taxonomy and standards help ensure Shopify data can power any commerce innovation.
Ongoing challenges and next steps:
- Balancing scalability, accuracy, latency: Ensuring quality without sacrificing speed or cost at our scale remains a central engineering challenge.
- Unified vs. multi-model: Today, each key entity (media, product, etc.) has a dedicated, size-optimized model. We are actively exploring consolidation into a single, multi-entity model to streamline our architecture and potentially bring similar performance gains we have observed from tackling multiple tasks simultaneously.
- Graph-based reasoning: Exploiting inter-entity relationships using LLM reasoning over graphs is a promising direction for entity resolution.
- Continuous pipeline improvement: As data and requirements constantly evolve, active learning, dynamic retraining, and infrastructure scaling remain a perpetual focus.
VIII. Conclusion
Building Shopify's Global Catalogue required rethinking how we approach product understanding at scale. By combining multimodal LLMs with careful system design, we've created infrastructure that makes millions of merchants’ products truly understandable by machines. This isn't just about better search or recommendations—it's about enabling entirely new ways of discovering and interacting with products.
As commerce continues its evolution toward AI-driven experiences, the importance of structured, reliable product data only grows. We're excited to continue pushing the boundaries of what's possible and sharing our learnings with the community.
For more details, watch our ICLR 2025 talk or explore our open-source taxonomy. Interested in these challenges? Join our team and help build the future of commerce.
