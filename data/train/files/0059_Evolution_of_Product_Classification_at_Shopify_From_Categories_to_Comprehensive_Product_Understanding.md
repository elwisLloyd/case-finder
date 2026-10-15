# Evolution of Product Classification at Shopify: From Categories to Comprehensive Product Understanding

Источник: https://shopify.engineering/evolution-product-classification

At Shopify, we help millions of businesses sell products across our platform, ranging from handcrafted jewelry to industrial equipment. Understanding these products, including their categories, attributes, and characteristics, is crucial for providing better search, discovery, and recommendation experiences for both merchants and buyers.
Our journey through product classification has evolved significantly over the years. What started as a basic categorization system has evolved into a system that is built on two key foundations, which we’ll introduce in this post: Vision Language Models and the Shopify Product Taxonomy.
The Journey to Better Product Understanding
Early Days: Basic Classification
Our initial approach to product classification in 2018 focused on basic categorization using traditional machine learning methods with our first model baseline being a logistic regression with TF-IDF classifier. While effective for simple cases, this system struggled with the increasing complexity and diversity of products on our platform.
The Multi-Modal Evolution
In 2020, we implemented a multi-modal approach combining image and text data for classification. This multi-modal approach improved our ability to understand products, especially in cases where either text or image alone might be ambiguous. However, we recognized that category classification alone wasn't enough to fully understand products.
The Need for Comprehensive Understanding
By early 2023, as our platform grew, we identified several key requirements:
- More granular product understanding beyond just categories
- Consistent taxonomy across the platform
- Ability to extract meaningful product attributes depending on category.
- Need for more metadata, including things like simplified product descriptions, content tags, and product characteristics
- Content safety and trust features
The emergence of Vision Language Models presented the perfect opportunity to address these needs comprehensively.
Current Generation
Our current product understanding system is built on two key foundations: Shopify's Standard Product Taxonomy and Vision Language Models.
The Shopify Product Taxonomy is a comprehensive library of product data spanning more than 26 business verticals, mapping over 10,000 product categories with over 1,000 associated product attributes. It offers:
- Hierarchical Classification: Products are mapped to specific categories within a detailed hierarchy (e.g., Furniture > Chairs > Kitchen & Dining Room Chairs).
- Category-Specific Attributes: Each category has its own set of relevant attributes, ensuring comprehensive product description.
- Standardized Values: Pre-defined attribute values help maintain consistency while allowing customization.
- Cross-Channel Compatibility: The taxonomy aligns with other platforms' classification systems through cross walks that we provide, facilitating multi-channel selling.
Vision Language Models complement this taxonomy by providing several breakthrough capabilities:
- True Multi-Modal Understanding: Unlike previous systems that processed images and text separately, Vision Language Models can understand the intricate relationships between visual and textual product information.
- Zero-Shot Learning: In addition, they can understand and classify products they've never seen before by leveraging their broad knowledge.
- Natural Language Reasoning: These models can process and generate human-like descriptions, enabling them to extract rich metadata from complex product listings.
- Contextual Understanding: They also excel at understanding products in context, considering not just what an item is, but also its intended use, style, and characteristics.
Together, these technologies enable us to automatically classify products within our taxonomy while extracting relevant attributes and generating consistent product descriptions.
Technical Deep Dive: Our System Architecture
Model Evolution and Optimization
Our journey with Vision Language Models reflects our commitment to continuous learning. Each model transition - from LlaVA 1.5 7B to LLaMA 3.2 11B, and now to Qwen2VL 7B - has brought significant improvements in prediction quality while maintaining operational efficiency. We carefully evaluate each new model against our existing pipeline, considering both performance metrics and computational costs.
Technical Deep Dive: Inference Optimization
Our inference stack employs several key optimization techniques:
FP8 Quantization
We've implemented FP8 quantization for our current Qwen2VL model, which provides three key benefits:
- Reduced GPU memory footprint, allowing for more efficient resource utilization.
- Minimal impact on prediction accuracy, maintaining high-quality results.
- Enables more efficient in-flight batch processing due to the smaller model size.
In-Flight Batching
Our system uses an approach through Nvidia Dynamo that improves throughput:
- Dynamic Request Handling: Instead of pre-defining fixed batch sizes, our system dynamically groups incoming product requests based on real-time arrival patterns.
- Adaptive Processing: The system adjusts batch composition on the fly, preventing resource underutilization.
- Efficient Resource Usage: By processing products as they arrive, we minimize GPU idle time and maximize throughput.
When processing product updates, our system improves efficiency by:
- Starting to process a batch as soon as new products arrive, rather than waiting for a fixed batch size.
- Accepting additional products during this processing time and immediately forming new batches with incoming items.
- Maximizing GPU utilization by minimizing idle times and adaptively managing workload fluctuations to optimize both latency and throughput.
KV Cache Optimization
We've implemented a Key-Value (KV) cache system that significantly improves our LLM inference speed:
- Memory Management: The system stores and reuses previously computed attention patterns.
- Token Generation Efficiency: Particularly effective for our two-stage prediction process, where we generate both categories and attributes.
Pipeline Architecture
Our near real-time processing pipeline incorporates these optimizations while maintaining robust error handling and consistency:
The diagram shows our production architecture where a Dataflow pipeline orchestrates the end-to-end process, making two separate calls to our Vision LM service for category and attribute predictions. The prompt of the second call is dependent on the output of the first call, as the attributes we predict for a product depend on the category of the product. The service runs on a Kubernetes cluster with NVIDIA GPUs, using Dynamo for model serving.
- Input Processing
- Dynamic request batching based on arrival patterns
- Preliminary validation of product data
- Resource allocation based on current system load
- Two-Stage Prediction
- Category prediction with simplified description generation
- Attribute prediction using category context
- Both stages leverage optimized inference
- Consistency Management
- Transaction-like handling of predictions
- Both category and attribute predictions must succeed
- Automatic retry mechanism for partial failures
- Monitoring and alerting for prediction quality
- Output Processing
- Validation against taxonomy rules
- Result formatting and storage
- Notification system for completed predictions
Building Robust Training Data
Training data quality directly influences system reliability, so we developed a multi-stage annotation system to ensure consistency and high standards. At the core is our multi-LLM annotation system, where several large language models independently evaluate each product. Each model contributes unique strengths, and structured prompting is used to maintain annotation quality. Products thus receive multiple, independent annotations, maximizing coverage and robustness. When annotations disagree, a dedicated arbitration system comes into play, employing specialized models that act as impartial judges to resolve conflicts. This system enforces careful ruling logic to address edge cases, ensuring that all annotations remain aligned with our taxonomy standards and are consistent across millions of products.
To further reinforce quality, we incorporate a human validation layer focused on strategic manual review of complex edge cases and novel product types. This introduces a continuous feedback loop for ongoing improvement and adaptability. Regular quality audits are conducted as part of this process, guaranteeing that our annotation standards remain high and our training data remains both reliable and representative.
Impact and Results
The integration of Vision LMs with our structured taxonomy has delivered substantial improvements for both merchants and buyers across several key dimensions. For merchants, our metrics reveal an impressive 85% acceptance rate of predicted categories, reflecting high trust in the system’s accuracy. This has led to enhanced product discoverability and more consistent organization within merchant catalogs. Accurate categorization also drives better search relevance, facilitates precise tax calculations, and streamlines product management by automating attribute tagging and reducing manual effort.
Buyers, in turn, benefit from more accurate search results, highly relevant product recommendations, and a consistently organized browsing experience. The use of structured attributes clarifies product information, empowering customers to make more informed decisions.
At the platform level, these advancements have enabled the processing of over 30 million predictions daily, while hierarchical precision and recall have doubled compared to our earlier neural network approach. Our structured attribute system now spans all product categories, fostering more effective automated content screening and ultimately enhancing overall trust and safety on the platform.
Future Directions
While our current system is already delivering meaningful improvements for merchants, we are committed to its continuous evolution and have identified several avenues for future development. On the technical front, we aim to incorporate new Vision LM architectures as they become available, expand attribute prediction to encompass more specialized product categories, and improve the system’s ability to handle multi-lingual product descriptions. Additionally, we plan to further optimize our inference pipelines to achieve even greater throughput.
At the platform level, a major upcoming enhancement is the migration from our current tree-based taxonomy to a Directed Acyclic Graph (DAG) structure. This shift will allow for multiple valid categorization paths per product, supporting more flexible relationships and accommodating cross-category products more effectively. We also intend to enhance metadata extraction for finer-grained details such as product measurements, specifications, material composition, and design elements, as well as broaden attribute coverage across all branches of the taxonomy. These developments will ensure our system remains at the forefront of accuracy and adaptability.
Conclusion
The evolution of Shopify's product understanding system represents a significant leap forward in how we help merchants succeed through better search relevance, better tax calculations, better analytics and many other features built on top of this system. By combining cutting-edge Vision Language Models with our structured taxonomy, we've created a system that not only understands products better but also delivers practical benefits across our entire platform.
Our approach demonstrates a novel application of Vision Language Models beyond their typical use cases. We've pushed these models beyond basic image classification tasks to complex product understanding at scale. Our system now processes millions of products daily, extracting detailed metadata, ensuring accurate categorization, and enabling everything from improved search relevance to precise tax calculations.
The success of our system in handling such a massive scale, with 30 million daily predictions and billions of historical products, shows how Vision Language Models can be effectively optimized and deployed to handle large-scale production workloads.
As we look ahead, we remain committed to pushing the boundaries of what's possible in product understanding. With continued advances in AI technology and our deep understanding of merchant needs, we’re empowering merchants and delivering net new capabilities to the Shopify ecosystem.
