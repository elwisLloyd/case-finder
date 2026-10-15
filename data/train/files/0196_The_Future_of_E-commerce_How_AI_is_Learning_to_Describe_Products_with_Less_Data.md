# The Future of E-commerce: How AI is Learning to Describe Products with Less Data

Источник: https://blog.flipkart.tech/the-future-of-e-commerce-how-ai-is-learning-to-describe-products-with-less-data-8dfbf05f83a1

The Future of E-commerce: How AI is Learning to Describe Products with Less Data
In the vast world of online shopping, accurately describing a product is everything. From the colour of a shirt to the pattern on a suitcase, these details, known as attributes, are crucial for helping you find exactly what you’re looking for. But with millions of items, manually labelling every single product is a monumental task. This is where Artificial Intelligence, specifically Vision Language Models (VLMs), comes in. Our new research paper, titled “Efficient Learning for Product Attributes with Compact Multimodal Models,” tackles a significant challenge in e-commerce: the high cost and impracticality of supervised fine-tuning for large VLMs. The paper is published at the International Conference on Computer Vision (ICCV) 2025 Workshop on Curated Data for Efficient Learning.
The Challenge: Too Much Data, Not Enough Labels
Manually labelling product attributes is not only expensive but also prone to errors, especially when dealing with massive and diverse catalogs. While large VLM APIs can automate this process, the cost becomes a major hurdle at the scale of a modern e-commerce platform. On the other hand, there is a treasure trove of unlabelled product images that could be used for training, if only we had an effective way to harness them.
Get Mandar Shrikant Kulkarni’s stories in your inbox
Join Medium for free to get updates from this writer.
Our research focuses on using compact VLMs (with 2–3 billion parameters), which are more suitable for real-world e-commerce applications where speed is critical. We explore how to train these smaller models using a small, initially labeled dataset and a much larger pool of unlabelled product listings.
The Solution: Smart AI That Teaches Itself
We propose a method that uses label-efficient, semi-supervised fine-tuning strategy that leverages Direct Preference Optimization (DPO). Here’s a breakdown of the process:
- Initial Training with a Small Labelled Set: We begin by fine tuning a pre-trained VLM on a small, curated dataset where the product attributes have been labeled using a large multimodal model (like Gemini/GPT). To keep the training efficient, we use Parameter-Efficient Fine-Tuning (PEFT), which involves training only a small set of adapter modules rather than the entire model.
- Self-Correction with Unlabelled Data: For each unlabelled product, the model is prompted to generate multiple “reasoning-and-answer” chains. Think of this as the AI “thinking out loud” before giving its final answer. We then use a technique called self-consistency to determine the most likely correct answer. The answer that appears most frequently is considered the “preferred” output, while the others are “dis-preferred”.
- Learning from Preferences with DPO: Instead of traditional training methods, the model is fine-tuned using DPO. This technique teaches the model to favour the “preferred” reasoning chains over the “dis-preferred” ones. The DPO loss function directly aligns the model’s probabilities with this preference data.
The DPO loss is calculated using the following formula:
This process is iterative, meaning the model continuously improves by generating better pseudo-labels in each cycle.
The Results: A Leap in Accuracy
The experiments were conducted on a dataset spanning twelve e-commerce verticals, including everything from sandals and sarees to suitcases and watches. The results are impressive.
- DPO Outperforms Supervised Learning: DPO-based fine-tuning using only unlabelled data showed a significant improvement over the initial supervised model. For instance, the accuracy of the Qwen2.5-VL-3B-Instruct model jumped from 75.1% to 85.7% after DPO training.
- More Data, Better Performance: The study found that as the amount of unlabelled data increases, the accuracy of the DPO-trained model steadily improves. This is a crucial finding, as it shows that the vast amount of unlabelled data in e-commerce catalogs can be effectively used to enhance model performance.
- Self-Learning vs. DPO: We also experimented with a simpler “Self-Learning” (SL) approach, where the model is retrained on its own high-confidence predictions. However, this method led to a drop in accuracy for smaller VLMs, likely due to the model reinforcing its own biases — a phenomenon known as “model collapse”. In contrast, DPO proved to be a much more stable and effective method for leveraging unlabelled data. The following table from the paper shows the comparison of different approaches and models.
Accuracy Results:
Why This Matters for Your Online Shopping Experience
This research is a significant step forward in making e-commerce AI more efficient and scalable. By using smaller, faster models and a clever self-improvement technique, this approach can lead to:
- More Accurate Product Listings: Better attribute prediction means more accurate and detailed product information, making it easier for you to find what you want.
- Faster and Cheaper Cataloging: E-commerce platforms can automate their cataloging process more efficiently, reducing costs and manual effort.
- Improved Search and Recommendations: With more accurate product data, search algorithms and recommendation engines can provide more relevant results.
In conclusion, we propose a powerful and practical method for training compact VLMs for a critical e-commerce task of product attribute prediction. By combining the efficiency of PEFT with the self-correcting power of DPO, this research paves the way for a new generation of smarter, more efficient e-commerce AI.
References:
- Our paper is available online at: https://openaccess.thecvf.com/content/ICCV2025W/CDEL/html/Kulkarni_Efficient_Learning_for_Product_Attributes_with_Compact_Multimodal_Models_ICCVW_2025_paper.html
- D. Rafailov, D. Mann, and R. Krishna. Direct preference optimization: Your language model is secretly a reward model, 2023.
- Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi,Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models, 2023.
