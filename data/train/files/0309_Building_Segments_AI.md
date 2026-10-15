# Building Segments AI

Источник: https://klaviyo.tech/building-segments-ai-fe33d9cab822

In November 2023, Klaviyo released a new segmentation feature called Segments AI to its 130,000 customers. The service helps companies automate the process of building intelligent segments of their customers’ profiles.
This post explains how Segments AI works and reflects on how to validate creative, non-deterministic outputs.
Background: What the heck is a segment?
Companies use Klaviyo to better understand and target their customers. Customer segmentation is a key part of that process.
Specifically, users build segments of their customers using logical conditions — usually based on things that customers have/have not done or properties about those customers.
For example, a Klaviyo user could build a segment for customers who have recently viewed myProductName, but have not purchased it. The output of a segment is a dynamic list of customers for whom these conditions are true. As time passes and new events stream in, Klaviyo keeps the segments up to date.
What problem are we solving?
When done right, segments are a powerful tool to understand and laser target your customers. But too often our users are not getting the most from the functionality — specifically, some users either spend too little or too much time in the UI:
- Problem 1: Less experienced users may not know how to express their concept as a Klaviyo segment.
- Problem 2: Highly experienced users can spend hours a week building repetitive segments.
This service seeks to give inexperienced users a simpler way to interact with segments and give experienced users a way to automate creating complex segments.
How does it work?
Like many other exciting features developed over the past 1.5 years, it involves an OpenAI account. That said, the service is far from just being a wrapper around ChatGPT.
Prompt chaining
Segments AI makes extensive use of prompt chaining internally. That means when we generate content with an LLM, we try to make each request as small, atomic, and simple as possible.
Prompt chaining typically makes generations quicker and higher quality in cases where outputs can be joined together without loss of cohesion. In other words, prompt chaining is great for generating parts of a JSON object, but generating a paragraph sentence by sentence as a series of discrete requests would create a frankenstein.
While prompt chaining typically increases generation quality, it also creates the risk of errors propagating like an LLM game of telephone. There is not an agreed upon term for this risk error propagation, but we call it chain entropy.
The issue of chain entropy is especially pronounced in use cases like Segments AI where generations need to adhere to a specific style (in our case, Klaviyo’s segment JSON schema). To mitigate this issue, we try to keep subtasks as separable and parallelized as possible such that there are fewer gates to pass through. Much like with product development, a waterfall structure can lead to unfortunate outcomes when a wrong path is taken early in that process.
Get Robert Huselid’s stories in your inbox
Join Medium for free to get updates from this writer.
Clarification: Prompt chaining is the common name for this approach but it is a bit of a misnomer in the case of Segments AI. A chain of prompts implies a synchronous process (i.e. one execution happening after another). However, Segment AI does many of these processes asynchronously (i.e. occurring in parallel).
Few shot learning: aka reading ChatGPT bedtime stories
In data science, the idea of few shot learning is to take a generalist model (e.g. ChatGPT) and transition it into a subject matter expert on a specific topic (e.g. defining Klaviyo segments) by finetuning it with just a few instructive examples. The idea of few shot learning can be pushed beyond its classic use case though. Instead of creating a segment expert, we can create dozens of subtask experts each with their own niche of expertise.
Few shot learning is classically done by explicitly finetuning the model in question with hand-designed training examples. In the case of LLMs though, this process can be done implicitly by seeding training examples into the system instruction. We find best performance when these training examples are annotated with input, ideal output, and the generalizable lesson to be learned.
It is analogous to teaching GPT via children’s stories. We find it surprisingly effective.
Paired with prompt chaining, this means we can ask a series of small, highly specific questions to specialized chatbot agents and paste together these results into a final composition.
Challenges
Validation
Engineers test new features by designing unit tests to poke at edge cases. Data Scientists validate models using ground truth test datasets.
It is becoming increasingly clear across industry that no one is quite sure how to evaluate LLM features. When we use an LLM-based feature such as Segments AI, we lose a one-to-one mapping between input and desired output.
In short, when there are dozens of jointly valid ways to define a segment of “engaged users,” it becomes difficult to evaluate feature performance in a quick, scalable, and cost effective way.
It seems as though people have primarily converged on three approaches all with their own strengths and weaknesses:
Over the course of Segments AI feature development, the team went back and forth between these options. Validation was a constant thorn in the side as we flitted between different options week over week. Moreover, as new functionality was added, the test cases expanded as well making regression analysis more complicated.
Ultimately, we decided to use a mix of LLMs evaluating LLMs and hand-designed test cases. The validation suite we created was packaged such that it could be run before major changes to the codebase. Both evaluation strategies are imperfect, but they were a useful, directional tool for quick feedback and bug diagnosis.
Validating LLM features with creative outputs is worth doing — even with all the headaches it can cause. That said, ultimately users are going to use your feature, not your validation suite. If you find yourself spending more than a third of your time tinkering with validation, there are probably better uses of time.
The most important thing is to make sure validation is a clear signal and expectations are clear and consistent with stakeholders.
Final thoughts
Generative AI features are never truly finished. Customer needs change, bugs pop up, and there are always non-deterministic hiccups to wrangle.
So, while this blog post may be ending, the work on AI at Klaviyo certainly is not. In fact, stochastic outputs and a rapidly changing state of the art mean that Gen AI features often require more maintenance than more standard data science projects. That may be for the best though since we’ve found that the time spent working on these sorts of tools has positive spillover effects.
The more time that data science teams spend building generative AI tooling, the more internal muscle and expertise they develop to tackle those problems. The more time customers spend with tools out in the wild of production, the better we understand their needs. The more time Data Science and Product spend collaborating together on customer-facing features, the better those pairings go.
Generative AI features are substantively different from ‘normal’ projects that data scientists have typically worked on for the past decade or two. They need to be validated differently, involve new risks, and are often more outward facing than teams are used to.
Teams, people, and even machine learning models learn by example. Happy building.
