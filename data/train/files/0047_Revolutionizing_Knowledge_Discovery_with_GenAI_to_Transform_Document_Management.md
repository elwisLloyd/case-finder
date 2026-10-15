# Revolutionizing Knowledge Discovery with GenAI to Transform Document Management

Источник: https://medium.com/intuit-engineering/revolutionizing-knowledge-discovery-with-genai-to-transform-document-management-0cdf4385c11c

Revolutionizing Knowledge Discovery with GenAI to Transform Document Management
Today’s organizations typically have the tools and capabilities to handle huge amounts of data. Still, finding the right information at the right time can feel like searching for a needle in a digital haystack, particularly when it comes to technical documentation. The more comprehensive your documentation is, the more challenging it can be to make exactly the right information discoverable when your engineers need it most.
At Intuit, we’re harnessing the power of generative AI (GenAI) to transform the way we manage, improve and use our knowledge bases. By improving the quality and structure of the information we store, we’re making it easier than ever to answer a wide range of questions quickly and effectively.
Traditional documentation systems suffer from several key challenges:
- Documentation quality varies significantly depending on who writes it.
- Difficult to know if information retrieved from documentation is up to date.
- Documents aren’t necessarily structured to easily parse for relevant information.
- Documentation not written with target audiences and use cases in mind.
To overcome these challenges at Intuit, we’ve built a GenAI-Powered pipeline to improve the quality and structure of documents to make them more discoverable, make appropriate updates as needed, and track the context in which the information contained in a document might be most useful.
Driving continuous improvement with a dual-loop system
The heart of our solution relies on a sophisticated dual-loop system that continuously enhances both the information in the knowledge base and the system’s ability to pull information out of the knowledge base in ways that best answer user questions.
Get Roddam Harshavardhan Reddy’s stories in your inbox
Join Medium for free to get updates from this writer.
The inner loop refines each individual piece of documentation to ensure it is up to date and structured in a way that makes it possible for the system to extract the information it needs when it needs it. The outer loop adds context to the equation so it can retrieve the relevant information from across the content in the knowledge base and synthesize an answer to a specific query.
The inner loop: enhancing the knowledge base
The inner loop uses a sophisticated pipeline of GenAI plugins to enhance documentation. Each plugin looks at a different aspect of the documentation and makes improvements as needed:
- Document Analyzer — This tool looks at a document’s structure, completeness and ease of comprehension. It compares these elements against a custom rubric to come up with a score for the document. Any element that does not meet the required threshold moves through the pipeline where other plugins make improvements until it is suitable for inclusion.
- Document Improvement Plugin — If the analyzer plugin is a tough but fair editor, the improvement plugin is a skilled writer that restructures and enhances the content. The tool restructures the content with an eye toward making it more coherent and comprehensive.
- Document Style Guide Plugin — This tool modifies the voice and style of a document to ensure consistency across the entire knowledge base. Think of it as an editor dedicated solely to ensuring documents adhere to an organization’s style guidelines.
- Document Discoverability Plugin — This plugin modifies content to ensure the outer system can find it when it needs it. It accomplishes this by adding semantic context and linking it to relevant user queries. This optimizes documents for search algorithms and for providing clear information to human readers.
- Document Augmentation Plugin — This plugin uses retrieval-augmented generation to pull in new, relevant information from various knowledge sources that apply to the document in question. It uses this information to revise the documentation as necessary to keep it up to date. Think of it as a research assistant always on the lookout to ensure new information gets included where appropriate.
The outer loop: making knowledge more accessible
After the inner loop ensures documents undergo continuous improvement in quality and discoverability, the outer loop makes it possible for the system to pull relevant information out of multiple sources within the knowledge base:
- Embedding Plugin — This tool creates vector representations of documents that serve as the basis for sophisticated similarity searches and content clustering. This process guides the system toward the information needed to satisfy a given query.
- Search Plugin — This plugin uses semantic similarity to scan prospective areas of content and find the most relevant chunks to respond to user queries. This step helps ensure search results are appropriate within the context of the question being asked.
- Answer Plugin — This plugin brings the pieces together by synthesizing the information provided by the other two plugins into comprehensive, accurate answers to user queries.
How this approach revolutionizes knowledge discovery
The individual components of this system all use proven techniques to perform their tasks. Large language models (LLMs) and vector stores aren’t new technologies in and of themselves. Orchestrating them in a pipeline gives our solution unique qualities, however:
- Intelligent pre-processing. Traditional systems simply index content when it gets added to a knowledge base. Our pipeline looks at the content along multiple dimensions and actively improves it before adding it to the system.
- Feedback-driven improvement. When the system is unable to answer a query successfully, it updates the Search Plugin to improve results for future similar searches and updates the base documents with any missing information.
- Context-aware enhancement. Because the system updates its search parameters, it improves its ability to answer questions in additional contexts in addition to adding or updating information.
Designed for real-world impact
Although this system is designed to improve documentation, it has benefits that could make it suitable for other knowledge retrieval systems as well. Setting a base level of quality for inputs lays a foundation for a more accurate and comprehensive knowledge base. Ensuring up-to-date information helps maintain a high level of quality across the knowledge base. A well-structured knowledge base that’s easier and faster to search means less time spent seeking out information. Search results that are combinable and adaptable to fit the context of a query produce a better user experience for knowledge workers looking for quick, precise answers to their questions.
Looking ahead
This GenAI pipeline represents a significant step forward for document management, but it’s just the beginning. In the future, this type of pipeline can be applied across other collections of content to improve our ability to answer user questions efficiently and accurately across a wide range of domains, far beyond software documentation.
We’re proud of our progress to date and excited for what the future holds as we continue to revolutionize knowledge discovery here at Intuit with generative AI.
Many thanks to the team!
I’d like to thank Rakesh Ajmera, Principal Software Engineer, Shwetha Kalyanathaya Shashidhara, Staff Software Engineer, Pranika Jain, Senior Software Engineer, Krishna Chaithanya C, Senior Software Engineer, April Jernberg, Senior Content Designer, Praneet Singh, Staff Product Manager, Bhargavan Muthuselvan, Manager 3, Software Engineering at Intuit for their contributions to this achievement.
