# How Shopify improved consumer search intent with real-time ML

Источник: https://shopify.engineering/how-shopify-improved-consumer-search-intent-with-real-time-ml

In the dynamic landscape of commerce, Shopify merchants rely on our platform's ability to seamlessly and reliably deliver highly relevant products to potential customers. Therefore, a rich and intuitive search experience is an essential part of our offering. Over the past year, Shopify has been integrating AI-powered search capabilities into our merchants’ storefronts. Shopify Storefront Search has transformed the way consumers can shop online. With Semantic Search, we went beyond keyword matching. We improved our understanding of the intent behind a consumer’s search, so that we could match a search with the most relevant products.
The net result is helping our merchants boost their sales while offering positive interactive experiences for their consumers. It’s a win-win!
Building ML assets with real-time Embeddings
Around the same time, Shopify also started investing in creating foundational machine learning (ML) assets. These assets are built as a shared repository of ML primitives which are used as reusable building blocks for more sophisticated AI systems. Shopify Storefront Search is the perfect use case for these ML assets. Complex systems like this need primitives that can transform both text and images into data formats it can process.
How do we do that?
Enter embeddings, which translate textual and visual content into numerical vectors in a high-dimensional space. This transformation allows us to measure the similarity between different pieces of content, whether text or images, enabling more accurate and context-aware search results.
Simplified example of using embeddings to compare search text to result corpus
Now that we have a clear idea of the ML primitives that Shopify Storefront Search relies on, let’s take a look at how we send these embedding updates to their systems.
Designing ML inference streaming pipelines
Currently, Shopify processes roughly 2,500 embeddings per second (or roughly 216 million per day) across our image and text pipelines in near real time. These embeddings include net-new or updated content from across our merchants. Since most of our data platform infrastructure is built on BigQuery, we use Google Cloud’s streaming analytics service Dataflow to power these pipelines. We chose Dataflow for its native streaming capabilities, easy integration with the overall Google Cloud ecosystem, and its ability to scale with our ever-growing AI and data needs. The high-level architecture of our design is quite simple. Let’s walk through the image embeddings streaming pipeline as an example.
- At startup, the embedding model is loaded.
- The pipeline listens to new events from an input event topic that signals an image has been created or modified on a merchant’s website.
- The new event is then preprocessed before running inference:
- Download the image to the worker machine
- Load the image to memory
- Resize the image
- Next, the embedding vector is generated for the image.
- Some final postprocessing is applied to the embeddings.
- The embedding is written to:
- Data warehouse for offline analysis (reports, dashboards)
- An output event topic for downstream real time ingestion (Shopify Storefront Search)
At this point, the curious reader may wonder why we chose to go with near real-time embeddings vs. a simpler batch solution. Doesn’t this increase the complexity of our pipelines? Merchants and their customers expect a seamless experience from Shopify’s platform. When a merchant edits their products or uploads a new image, they want these updates to be available on their website instantly. Additionally, the ultimate objective is to boost sales for our merchants and offer pleasant interactive experiences for their consumers. Our data suggests that up-to-date embeddings achieved through a streaming pipeline allows us to optimize for this, despite the additional complexity it incurs when compared with a batch solution.
Challenges of maintaining a streaming pipeline
The reality of maintaining a streaming pipeline can be quite challenging. Adding GPU-accelerated inference to the mix further raises the complexity. As a result, we constantly have to make meaningful trade-offs between cost, throughput and latency. Let’s go through a few examples of these technical decisions.
1. Managing data in memory
When deploying the image embedding pipeline, our initial choice of worker machines on Dataflow was the n1-standard-16 mounted with a T4 GPU. However, we started running into Out of Memory (OOM) errors. Images consume a significant amount of memory so this wasn’t surprising.
Our first solution was to increase the memory of the workers. So we switched to n1-highmem-16 machines, which increased the memory on the worker from 60GB to 104GB. This worked for quite some time but it also increased our costs by 14%. Ultimately, we needed a better long-term solution.
Thus began our journey to get a better understanding of Dataflow internals. To maximize the utilization of the worker’s hardware, Dataflow’s python runner will typically create one process per core on the machine. Therefore, on an n1-highmem-16, the runner spawns 16 processes for the highest possible parallelism on the machine. Furthermore, to boost concurrency, each of those processes creates 12 threads by default. Each thread is then assigned elements to run inference.
With 16 processes, this meant that we had 16 x 12 = 192 threads concurrently processing elements. This translates to roughly 192 concurrent images in memory (in reality, this gets a bit more complicated when we consider that elements are grouped into bundles, but we can ignore this for now).
Luckily, the Dataflow Runner allows us to setnumber_of_worker_harness_threads to control this. Doing some quick napkin math, we estimated that lowering the thread count to 4 would theoretically reduce our memory footprint by 3x (i.e. 4 x 16 = 64 threads; 192 / 64 = 3). Lowering the thread count also naturally reduces the throughput of a pipeline’s preprocessing steps due to lower concurrency. Since the pipeline is already GPU-bound, we were accumulating more images than the GPU could process. As a result, the inference step’s throughput was not significantly impacted. What is the result of this change? Beforehand, we were consistently hovering around the high-mem machine’s max memory of 104 GB. After the change, it’s now closer to 40 GB: ~2.6x memory footprint decrease! As a result, we switched back to
n1-standard-16 machines, eliminating the extra 14% in cost in the process!
Apache Beam provides two concepts to enabling running inference in a batch or streaming pipeline:
- ModelHandler defines the ML model that will be used for inference.
- RunInference is the transform that generates embeddings based on the ModelHandler.
By default, each process on the worker loads its own instance of the embedding model to the GPU. Recall that we are using n1-standard-16. Therefore, the model was being loaded 16 times into the GPU’s memory. This increases throughput as more instances of the model can run in parallel but also increases memory consumption. 
Initially, we explored reducing the model’s memory footprint by determining if we could control how the model is loaded to memory. The most straightforward solution to this is to enable the ModelHandler to 
share the model across processes
This essentially loads the model once into a shared process. The python processes on the VM will then query it for inference.
This leads to a significant decrease in memory consumption but the throughput is also significantly degraded due to lower parallelism. We abandoned this approach due to the lower throughput.
Another option was to see if we can control how many python processes are created on each worker. Unfortunately, at the time of writing this, this is not currently possible. The only option is to enableexperiments=no_use_multiple_sdk_containers. This forces the Dataflow Runner to create only one process per worker but leads to a significant degradation in throughput, which we opted against.
Ultimately, our embedding models are small enough that we don’t need to worry about this too much. We eventually opted to stick with Dataflow’s default configuration.
3. Batching
While CPU utilization above 80% should typically be avoided where possible to avoid thrashing, GPU utilization should still ideally be as close to 100% as possible. This may seem surprising initially but this is because switching between threads on a GPU Streaming Multiprocessor (SM) is basically free.
Due to the GPU’s high throughput, the data transfer between a host (CPU) and a device (GPU) is almost always the main bottleneck in a streaming data pipeline (in reality the data transfer between the GPU’s global memory and the SMs running the kernels is also a major bottleneck but this is beyond the scope of this blog). This is where batching becomes crucial to effectively saturate the workers’ GPU.
Thankfully, Apache Beam offers helpful semantics to batch data in your streaming pipeline. By overriding thebatch_element_kwargs method in our Model Handler, we were able to define our desired batches to send to the GPU.
So we’re done right? Not so fast.
We are still sending batches of 1 to the GPU. What gives?
RunInference uses the BatchElements transform under the hood to do batching. It essentially has two methods of batching data. It can attempt to batch data within the existing bundle or across bundles using a stateful implementation.
Bundles are a Dataflow concept to manage parallelism. Essentially, a bundle is a collection of elements that are processed together. This is determined by the Dataflow Runner — the user has no direct control of this value.
In our case, due to the burstiness of the pipelines’ input topics, elements were being organized in bundles of 1, meaning Dataflow was unable to batch the elements in any meaningful way. On the other hand, stateful batching (by adding max_batch_duration_secs) attempts to guarantee that you get your desired batch size but also incurs higher latency. This is mainly because the Dataflow Runner forces a shuffle.
In the end, we are still able to saturate the GPU due to Dataflow loading a model instance per process (as we discussed previously). This creates enough parallelism to offset the higher number of data transfers between the host (CPU) and device (GPU). As a result, we chose to stick with the in-bundle batching option because the latency cost was too expensive. This is an area we are still actively investigating for best practices.
Conclusion
Shopify’s real-time embedding pipelines, which deliver text and image embeddings as centralized ML assets, are a powerful building block for innovation, enabling us to continue building new and exciting products. Semantic Search is just one awesome example of this. We are currently partnering with a few internal teams at Shopify to identify what problems might be worth solving and what centralized ML asset we could build to help solve them.
What’s next?
- Curious to learn more about Machine Learning at Shopify? Check out this blog on Building Shopify Inbox’s Message Classification Model.
- Want to get started with Dataflow ML? Check out this docs page.
*Co-authored by Danny McCormick, Software Engineer, Google Cloud
