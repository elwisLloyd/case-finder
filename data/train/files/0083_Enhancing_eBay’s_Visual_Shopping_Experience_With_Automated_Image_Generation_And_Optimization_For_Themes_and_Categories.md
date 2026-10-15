# Enhancing eBay’s Visual Shopping Experience With Automated Image Generation And Optimization For Themes and Categories

Источник: https://www.linkedin.com/pulse/enhancing-ebays-visual-shopping-experience-automated-image-galsurkar-9pgle/

Preface
To scale high-quality, thematically specific images for thousands of categories on eBay, we developed an automated image generation system leveraging Multimodal Generative AI to reduce manual effort required for curation.
Introduction
In e-commerce, each visual element in a user’s shopper journey is more than just an image, it’s a doorway to engagement. While each eBay item has a representative image, typically uploaded by the seller, the eBay category is represented by plain text, which is not as visually exciting. In order to generate an image for an eBay category, or more broadly a theme or set of items, a curator/designer would have to manually create an image. This process is time-intensive, requires extensive resources, and cannot quickly adapt to emerging trends. To address these limitations, our team developed a Multimodal Generative AI-powered system that automates the generation of category or thematic images. As we leverage AI to enhance this experience, applying it safely and responsibly is our guiding principle. By integrating multimodal LLMs, our solution produces high-quality, visually engaging images at scale, using a unique feedback loop that refines both prompts and images to ensure they meet predefined quality standards. Our approach allows for efficient creation of category and thematic-specific images, enabling rapid updates, improved merchandising flexibility, and consistency across the platform.
Background
Every item in the eBay inventory falls into one or more categories in the category taxonomy. The category taxonomy is represented by text as a breadcrumb (see Figure 1). eBay displays a variety of banner images for featured categories or promotions that play a vital role in enhancing the browsing experience by visually guiding users through various themes, products, and styles. Previously, these images were manually designed, which was time-consuming and not easily scalable for thousands of categories.
To automate this process, we developed a pipeline that utilizes multimodal LLMs for generating category-specific images. By extracting relevant item information, simplifying item titles, generating detailed prompts, and creating images with minimal human intervention, our system transforms eBay’s ability to produce fresh, engaging visuals across categories.
Approach
The data processing pipeline is depicted in Figure 2. Broadly, there are three components: 1) Data pre-processing, 2) Initial Image Generation, and 3) Automated Evaluation Framework.
1) Data pre-processing
Since a category is defined by a simple category breadcrumb text, we would like to add additional contextual information to feed into our image generation system. Items have a wealth of information, including title and behavioral interaction data. Therefore, we select items from each given category for additional information for image generation.
Item Title Extraction
We start by sampling popular item titles that belong to each category or theme. Popularity is determined by the click through rate. For example, below are two popular items from the Fashion category:
          
      
        
    J Jason Wu V Neck Crossover Shirt Purple 3X Long Sleeve A389855 Women YG17
    Women’s L L Bean Medium Hawaiian Long Sleeve Button Up Collared Shirt Blue/white
      
Item Title Simplification/Theme Identification
Since item titles often include extraneous non-visual details (e.g. brand names, sizing information or model numbers) that could mislead the LLM in prompt creation, we utilize LLMs to simplify these titles. By filtering out non-visual elements, we ensure that only the essential details related to the category and theme are preserved
2) Initial Image Generation
Image Prompt Generation
Once item titles are simplified, we use an LLM to generate image prompts that capture the category’s theme. Using the category name and simplified titles as input, the LLM produces detailed prompts specifying the subject, style, and background of the image to be generated. The generated prompts follow best practices in product photography, focusing on minimalism and professional aesthetics. This structured approach ensures that the generated images align with eBay’s visual standards.
Recommended by LinkedIn
Image Generation
The LLM-generated prompts are passed to a Large Vision Model, which produces representative images for the specified category. This process replaces the need for human intervention and allows for scalable, automated image creation.
3) Automatic Quality Assessment Framework
A novel multimodal LLM-driven evaluation framework automatically assesses each generated image to ensure high quality and thematic alignment before storage. Since these generative models are non-deterministic, the same prompt can produce a range of images, some of which may contain distortions or other unintended visual elements. While we can’t entirely prevent such variations, our evaluation system is designed to detect and exclude images that don’t meet the standards.
In our initial trials, common problematic variations included distorted objects. Below you can see examples such as warped laptops or “melting” sunglasses, as well as unexpected random objects, like flowers or leaves, that detracted from the intended theme. Other problematic characteristics were dark, shadowy backgrounds as well as blurred or incomplete details. Addressing such inconsistencies is crucial, and our approach throughout this work was guided by eBay’s Responsible AI principles, ensuring we developed and evaluated these generative capabilities in a safe and responsible manner. At eBay, ensuring the responsible and safe use of AI is one of our top priorities.
Based on these observations, we identified a set of quality benchmarks and developed a targeted evaluation rubric that helps us work within the limitations of the multimodal LLM’s detection abilities.The evaluation framework uses a rubric approach, applying the following criteria to each image:
          
      
        
    Fidelity to the Prompt: How well the image aligns with the prompt provided.
    Detail Sharpness and Clarity: The visibility, sharpness, and clarity of each detail.
    Adherence to Product Photography Style: How well the image follows eBay’s stylistic guidelines.
      
Each image is scored in these categories and images that meet or exceed a predefined threshold are kept, while those scoring below are excluded. This rubric-based system provides a structured way to screen and refine generated images, ensuring consistency and quality across our automated visuals.
Image Representation and Quality Optimization
In cases where an image does not meet the required threshold, the system uses a multimodal LLM to analyze the image, prompt and the evaluation results, to generate an improved prompt. This enhanced prompt is then used to create a new image, with the evaluation and refinement cycle continuing until an image meets all necessary criteria or the system reaches a predefined retry limit.
Novelty
This pipeline distinguishes itself by its innovative feedback and optimization loop. The system’s ability to automatically evaluate and refine prompts and images through multimodal feedback is a novel approach to ensuring that AI-generated content meets high standards of visual quality and contextual relevance. This optimization cycle significantly reduces distortion, blurriness, and stylistic mismatches, resulting in better quality images with minimal human intervention.
Existing technologies focus primarily on single-pass image generation. However, this system introduces a multi-stage process: It begins with data preprocessing, where items representing the theme are collated and essential visual details are extracted. This is followed by generating an initial image prompt informed by the simplified item titles and category context. The process then incorporates a multimodal evaluation framework, which assesses the generated images against predefined quality benchmarks. If an image does not meet the standards, an iterative optimization loop refines both the prompt and the image until the desired quality and thematic relevance are achieved. This recursive improvement cycle allows the generation of highly optimized, contextually relevant images.
Evaluation
To assess the effectiveness of our automated image generation and evaluation framework, we conducted a human assessment on a sample of generated images, each representing a unique eBay category. These images have all passed our rubric’s threshold score for fidelity, detail, and adherence to photography style.
In our assessment, human evaluators confirmed that 88% of the images were suitable for use on eBay, meaning they met all quality and thematic criteria required for accurate category representation. This precision score highlights the robustness of our evaluation framework, though it also revealed some areas for improvement. We identified a subset of false positives, images that passed the automated rubric but didn’t fully meet human expectations, and false negatives where suitable images were rejected by the model.
With the foundation in place, future work will focus on refining the evaluation process by using feedback from both accepted and misclassified images to improve the rubric. Through iterative adjustments, we can better align automated assessments with human standards and ensure that only the most relevant, high-quality images are used to represent eBay’s diverse categories.
Conclusion
Our automated image generation framework marks a transformative step in enhancing eBay’s visual content, delivering high-quality, category-specific images with minimal manual intervention. By combining multimodal LLMs with a robust, iterative evaluation process, we’ve created a scalable solution that maintains the integrity of eBay’s brand standards while reducing the resource demands of traditional image curation. The success of this system in early trials demonstrates the potential of AI-driven solutions in elevating user experience and merchandising flexibility. By generating images for categories, instead of plain text, we enhanced the user shopping experience by creating visually appealing, contextually relevant representations that make browsing more engaging and intuitive. This aligns with our vision of enhancing eBay’s visual shopping experience through automated image generation and optimization.
