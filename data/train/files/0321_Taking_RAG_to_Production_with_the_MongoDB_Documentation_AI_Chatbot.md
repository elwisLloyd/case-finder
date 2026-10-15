# Taking RAG to Production with the MongoDB Documentation AI Chatbot

Источник: https://www.mongodb.com/developer/products/atlas/taking-rag-to-production-documentation-ai-chatbot/

Quickly try MongoDB Vector Search in the MongoDB Search Playground by using a RAG chatbot that answers questions on your data with vector search. The Chatbot Demo Builder in the MongoDB Search Playground allows you to bring your own data, try different chunking strategies, generate embeddings using Voyage AI embedding models, and ask questions about the data without an Atlas account, cluster, or collection. You can also share a link to a snapshot of your MongoDB Search Playground with others.
The Chatbot Demo Builder uses two aggregation pipeline stages, $vectorSearch and $project.
This is a generative AI chatbot. All information should be verified prior to use. Do not upload sensitive data. MongoDB logs your workload data for monitoring the system health and to help troubleshoot any issues in the Chatbot Demo Builder.
- The Chatbot Demo Builder processes the imported PDF file or copy-pasted text as a single, unified knowledge source. You cannot define or combine separate data collections within the builder.
- The Chatbot Demo Builder uses a pre-configured vector search index that is not editable. The query is generated based on the specified retrieval settings and cannot be directly edited using the code editor.
- The Chatbot Demo Builder environment does not persist. To save an environment, use the Share button to generate a snapshot URL that persists for 30 days.
- The Chatbot Demo Builder only supports text-based embeddings. If your PDF file contains images, the chatbot will not be able to process or answer questions about the content within those images.
- The Chatbot Demo Builder has the following data limitations: 
  - You cannot import files larger than 100 MB.
  - The total character count cannot exceed 100,000 characters.
  - You cannot bring your own vector embeddings or API credentials for embedding solutions.
The Chatbot Demo Builder provides three data source options.
| Upload PDF | Upload a PDF file from your local device with a maximum size of 100 MB. If the character count exceeds 100,000, you must use only the first 100,000 characters or upload a file with less characters. You can preview the text with SEE TEXT. | 
| Copy & Paste Text | Copy and paste text up to 100,000 characters. If the character count exceeds 100,000, you must use only the first 100,000 characters or reduce the text size. | 
| Sample Data | Use sample data provided by MongoDB, which is a PDF about a fictional park. | 
Chatbot Demo Builder is a public demo. Do not upload sensitive data.
Customize your chunking settings and embedding model.
| Chunking strategy | Choose either Recursive Chunking (default option) or Fixed Token Count with Overlap. To learn more about chunking strategies, see Chunking Strategies. | 
| Chunk size | Define the number of tokens per chunk. The number of tokens must be at least double the amount of chunk overlap. | 
| Chunk overlap | Specify the size of the overlap of tokens between adjacent chunks. The overlap size must be at most half of the chunk size. | 
| Embedding model | Select one of the following embedding models: | 
To modify these options after creating embeddings, use the side panel DATA SETTINGS. Changing the settings clears previous chat history.
Each question and answer pair is independent, with no reliance on previous interactions. When you select Share, the playground saves your data configurations and retrieval settings. Question and answer history is neither saved nor can be shared.
For every question that you ask, the Chatbot Demo Builder shows the following settings:
| Setting or Output | Location on Page | Description | 
|---|---|---|
| Search Query | Linked in chat box with answer | View the MongoDB Vector Search query syntax. | 
| [number] DOCUMENTS | Linked in chat box with answer | View the documents retrieved from running the search query and how the results are scored. | 
| Data to Evaluate (numCandidates) | Right side panel | Adjust the number of potential matches the system reviews to select the best result. To exhaustively search all indexed vector embeddings, click the Evaluate all [number] documents (ENN) check box. This may impact query latency. | 
| Data to Retrieve (limit) | Right side panel | Adjust the number of documents (chunks) returned. | 
| Data Source | Bottom panel tab | View your data as MongoDB Documents or Full Extracted Text. | 
| Index Definition | Bottom panel tab | View the generated MongoDB Vector Search index definition. | 
| Search Query | Bottom panel tab | View the MongoDB Vector Search query syntax used for the most recent question and answer. | 
| LLM & Prompt | Bottom panel tab | View the Large Language Model (LLM) used. | 
Note
The Chatbot Demo Builder performance might differ from production performance.
To learn more about vector search queries, see Run Vector Search ANN and ENN Queries. To learn more about Retrieval-Augmented Generation (RAG), see Retrieval-Augmented Generation (RAG) with MongoDB.
