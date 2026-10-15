# Snap Ads Understanding: From Pixels to Words

Источник: https://eng.snap.com/snap-ads-understanding

Snap Ads Understanding
From Pixels to Words
Introduction
Our advertising platform at Snap receives a large volume of new ads every day. To maintain a high-quality and relevant ad ecosystem, we need to review these creatives at scale, to ensure they align with our policies, are safe for our community, and are shown to the right Snapchatters. This involves creative understanding for both moderation and relevance: what themes it conveys, what products it highlights, and how it aligns with the user’s interests.
As part of our efforts to enhance creative understanding, we developed a technique that converts ad creatives, such as videos and images, into rich, structured, human-readable text that captures the core visual and thematic elements of the ad. These descriptions make it possible to extract interpretable and high-signal concepts which in turn power more scalable, accurate moderation tools and better models for relevance and ranking.
This technique opens up new opportunities for enhancing ad safety, trend detection, creative analysis, and user relevance, all by building a deeper understanding of the actual content within ads. Whether you are enforcing policy, modeling engagement, or spotting emerging creative trends, this is a technique that provides a scalable foundation for intelligent, content-aware systems.
Challenges
Ad platforms face significant challenges when handling vast volumes of ads daily. To effectively moderate, enforce policies, and ensure ad relevance, platforms must deeply understand each creative’s content. Traditional embedding-based methods have some limitations:
- Loss of context:
Embedding methods compress videos or dynamic visuals into single vector representations, losing important context such as scene changes, sequential frames, or essential text overlays like promotional details.
- Uninterpretable representations:
Embeddings produce high-dimensional vectors that can obscure the reasons behind performance issues in downstream models, making troubleshooting and model improvement difficult.
- Difficult to annotate:
Embeddings don't generate explicit labels or structured attributes, making specific queries, like retrieving all ads explicitly mentioning “50% off” promotions, challenging or impossible. Furthermore, introducing new labels or attributes usually requires retraining the embedding model, hindering rapid experimentation, iteration, and the quick addition of new features.
Embedding-only methods provide efficient, scalable representations and flexible general purpose embeddings useful across a wide range of downstream tasks. However, our applications often require clear, interpretable, and structured insights. Textual representations of the content complements embedding-based approaches by generating structured, explicit descriptions, enabling scalable, precise, and actionable creative content understanding tailored specifically for robust moderation, accurate targeting, and effective trend detection.
Solution
These textual representations address these limitations by automatically generating clear, keyword-rich descriptions of an ad’s visual and audio content. Instead of relying solely on embeddings, it leverages powerful multimodal language models to create coherent, structured annotations. Specifically:
- Samples representative frames from video ads (such as extracting key frames, or a fixed number) or selects a single representative image for image-based ads.
- Transcribes audio content using advanced speech-to-text models, if audio is present.
- Generates natural language descriptions from these inputs using a multimodal generative model, explicitly capturing brands, products, contexts, and key events depicted in the ad. (see Figure 1.)
To illustrate how these differences matter in practice, we'll walk you through an example showcasing both the limitations of traditional embedding approaches (such as semantic embeddings from models like CLIP) and how the content textual representation effectively addresses them. In the example below, we specifically compare results using CLIP embeddings.
A Case Study: Snap Spectacles Ads
Understanding an ad's core message is crucial for accurate retrieval, ranking, and recommendation. Below, we'll see how each approach (traditional embeddings versus the textual representations) is able to capture important themes and specific details within the content. Additionally, it's important to note that the traditional embedding approach typically requires additional data collection and model retraining if specific new attributes or themes need to be captured accurately.
Lets take a look at this example which is a Spectacles ad:
TheCLIP model 1 provides embeddings for both images and texts, enabling semantic alignment between visual and textual content. For video applications, a common practice is to compute embeddings by mean-pooling frame-level CLIP embeddings 2. Relevance is then typically measured using cosine similarity between these video embeddings and textual query embeddings. However,
- It may loosely match attributes like “Sale” but fail to recognize critical themes such as “Spectacles,” “glasses,” or the ad’s humorous tone.
- In our example, the cosine similarity scores between the CLIP embedding of the video (specifically mean-pool of frames embedding) and keyword embeddings are: 
  - Spectacles: 0.2603
  - Sale: 0.2713
  - Glasses: 0.2377
  - asdasd (random string): 0.2586
These results highlight that pure embeddings lack semantic precision, as a random string (“asdasd”) achieves a similarity score comparable to meaningful keywords.
In our approach, we first generate structured, human-readable descriptions of the ads by incorporating both the visuals and the audio signals: “The ad features a series of frames showcasing stylish spectacles…” (full text in Figure 1).
These textual descriptions can be indexed and retrieved using standard text-based search techniques, making the system both scalable and efficient. Additionally, we can compute the embedding of the generated texts (instead of the embedding of the videos directly) and it significantly improves results compared to traditional embeddings alone.
For the same example, the cosine similarity score between the embeddings of the textual description with keyword embeddings are:
- Spectacles: 0.4559
- Sale: 0.4098
- Glasses: 0.4055 Compared to the previous approach, it increases the relevance of key terms while reducing noise from unrelated strings.
- Random text (“asdasd”): 0.1931
Compared to the previous approach, it increases the relevance of key terms while reducing noise from unrelated strings.
Figure 1. Content Textual Description in Action
Creative Description
The ad features a series of frames showcasing stylish spectacles. The first frame shows a close-up of a person adjusting the glasses on their face, highlighting the sleek design. The second frame zooms in on the reflective lenses, displaying vibrant colors. A bold yellow background with the word 'SALE' repeated in various orientations dominates the center frame, emphasizing a promotional offer. The bottom frames depict two circular images: one of a person holding a dog by the beach, and the other showing a view from a water slide, suggesting fun and adventure.
System Overview
Here is an overview of the system architecture provided in Figure 2. It involves sampling and combining video frames into a single frame, extracting audio signals from soundtracks, providing textual instructions to the model and extracting key concepts within the video or image.
Figure 2. System diagram for the creative textual representations pipeline
- Video Ingestion: An ad video (or image) is uploaded.
- Frame Extraction: We sample multiple frames to capture different scenes and on-screen text.
- Audio Transcription: The voiceover or soundtrack is converted to text via speech-to-text models.
- Generative Annotation: We fuse the visual and audio elements into a cohesive text narrative through an instructed call to a visual-language model (VLM). Note that the instruction/prompt will be task specific.
- Storage & Indexing: We store these textual descriptions in a database, both relational and vector-based, to support flexible search and retrieval.
Applications
These mappings of contents to rich textual descriptions unlock a variety of applications, from moderation and compliance to enhanced relevance ranking and performance analytics. The structured text can be indexed directly in keyword-based search engines or converted into embeddings for rapid similarity searches.
Fraud Trend Detection:
These content textual representations support early detection of emerging fraud patterns. By analyzing descriptions for phrases like “90% off luxury bag” or “limited-time iPhone deal”, systems can flag creatives that exhibit suspiciously aggressive promotions, repeated scam-like language, or patterns associated with counterfeit goods. Instead of building one-off detectors for each fraud scenario, teams can continuously scan the structured text to identify and act on trends as they emerge, greatly reducing response time and improving operational efficiency.
Brand Safety and Compliance Monitoring:
It also simplifies monitoring brand or policy compliance by enabling direct keyword searches within the text. Compliance teams can quickly identify restricted products, inappropriate content, or mentions of competitor brands without the complexity of specialized audio or visual processing.
Rapid Feature Expansion:
The textual nature of these content descriptions allows teams to easily add or extend features by parsing textual details. For example, teams can effortlessly detect:
- Animals: Keywords like “dog,” “cat,” or “pet.”
- Promotions: Phrases such as “50% off,” “limited offer,” or “sale.”
- Human presence: Terms like “man,” “woman,” or “person.”
By systematically including such detailed descriptions, we can eliminate the need for multiple specialized AI pipelines or frequent retraining. This streamlined approach accelerates feature iteration, making ad moderation and relevance enhancements faster, scalable, and highly adaptable.
Benefits
The content textual representation offers a powerful way to extract structured insights from multimedia content, transforming complex ad creatives into easily searchable and interpretable text. Instead of relying on multiple specialized models to detect different features, such as brand elements, promotions, or visual themes, it provides a unified textual representation that can be efficiently processed and scaled. This approach simplifies downstream applications while enhancing transparency, control, and cost-effectiveness. Here are some key reasons why this method stands out:
- Reduces Complexity: By converting multimedia content to text, you eliminate the need for specialized models to detect each new feature (animals, discounts, brand logos, etc.).
- Enables Fine-Grained Control: You can tweak prompts to hone in on specific details or brand guidelines, then parse the output.
- Scalable Architecture: As your video library grows, the textual representation pipeline can handle each new asset, generating standardized text in a consistent format to be used by downstream services instead of each of them processing each video multiple times to extract the information they need.
- Improves Transparency: Unlike black-box embeddings, you can read the final output, making it easier to trust and explain the results.
- Reduces costs: By providing and utilizing a textual representation of an ad, we can eliminate dependencies on image or audio modalities in the applications mentioned above. This makes downstream applications easier, cheaper, and faster to run, as processing text is highly scalable, cost-effective, and efficient.
Conclusion
Creative content textual representation transforms how we understand ad creatives, making it easier to moderate, annotate, and extract meaningful insights at scale. By converting multimedia content into structured text, it unlocks:
- Faster, more accurate moderation by surfacing sensitive or policy-violating elements directly from descriptions.
- More relevant ad targeting through high-signal features that improve downstream models.
- Simplified feature development by enabling flexible, text-based querying and rule-based extraction.
As the volume and complexity of creative content continues to grow, it offers a scalable foundation for building smarter, safer, and more effective ad systems.
