# Automation Platform v2: Improving Conversational AI at Airbnb

Источник: https://medium.com/airbnb-engineering/automation-platform-v2-improving-conversational-ai-at-airbnb-d86c9386e0cb

Automation Platform v2: Improving conversational AI at Airbnb
How Airbnb’s conversational AI platform powers LLM application development.
By: Chutian Wang, Zhiheng Xu, Paul Lou, Ziyi Wang, Jiayu Lou, Liuming Zhang, Jingwen Qiang, Clint Kelly, Lei Shi, Dan Zhao, Xu Hu, Jianqi Liao, Zecheng Xu, Tong Chen
Introduction
Artificial intelligence and large language models (LLMs) are a rapidly evolving sector at the forefront of technological innovation. AI’s capacity for logical reasoning and task completion is changing the way we interact with technology.
In this blog post, we will showcase how we advanced Automation Platform, Airbnb’s conversational AI platform, from version 1, which supported conversational systems driven by static workflows, to version 2, which is designed specifically for emerging LLM applications. Now, developers can build LLM applications that help customer support agents work more efficiently, provide better resolutions, and quicker responses. LLM application architecture is a rapidly evolving domain and this blog post provides an overview of our efforts to adopt state-of-the-art LLM architecture to keep enhancing our platform based on the latest developments in the field.
Overview of Automation Platform
In a previous blog post, we introduced Automation Platform v1, an enterprise-level platform developed by Airbnb to support a suite of conversational AI products.
Automation Platform v1 modeled traditional conversational AI products (e.g., chatbots) into predefined step-by-step workflows that could be designed and managed by product engineering and business teams.
Challenges of traditional conversational AI systems
We saw several challenges when implementing Automation Platform v1, which may also be broadly applicable to typical conversational products:
- Not flexible enough: the AI products are following a predefined (and usually rigid) process.
- Hard to scale: product creators need to manually create workflows and tasks for every scenario, and repeat the process for any new use case later, which is time-consuming and error prone.
Opportunities of conversational AI driven by LLM
Our early experiments showed that LLM-powered conversation can provide a more natural and intelligent conversational experience than our current human-designed workflows. For example, with a LLM-powered chatbot, customers can engage in a natural dialogue experience asking open-ended questions and explaining their issues in detail. LLM can more accurately interpret customer queries, even capturing nuanced information from the ongoing conversation.
However, LLM-powered applications are still relatively new, and the community is improving some of its aspects to meet production level requirements, like latency or hallucination.So it is too early to fully rely on them for large scale and diverse experience for millions of customers at Airbnb. For instance, it’s more suitable to use a transition workflow instead of LLM to process a claim related product that requires sensitive data and numbers of strict validations.
We believe that at this moment, the best strategy is to combine them with traditional workflows and leverage the benefits of both approaches.
Architecture of LLM application on Automation Platform v2
Figure 4 shows a high level overview of how Automation Platform v2 powers LLM applications.
Here is an example of a customer asking our LLM chatbot “where is my next reservation?”
- Firstly, user inquiry arrives at our platform. Based on the inquiry, our platform collects relevant contextual information, such as previous chat history, user id, user role, etc.
- After that, our platform loads and assembles the prompt using inquiry and context, then sends it to LLM.
- In this example, the first LLM response will be requesting a tool execution that makes a service call to fetch the most recent reservation of the current user. Our platform follows this order and does the actual service call then saves call responses into the current context.
- Next, our platform sends the updated context to LLM and the second LLM response will be a complete sentence describing the location of the user’s next reservation.
- Lastly, our platform returns LLM response and records this round of conversion for future reference.
Another important area we support is developers of LLM applications. There are several integrations between our system and developer tools to make the development process seamless. Also, we offer a number of tools like context management, guardrails, playground and insights.
In the following subsections, we will deep dive into a few key areas on supporting LLM applications including: LLM workflows, context management and guardrails.
Get Chutian Wang’s stories in your inbox
Join Medium for free to get updates from this writer.
While we won’t cover all aspects in detail in this post, we have also built other components to facilitate LLM practice at Airbnb including:
- Playground feature to bridge the gap between development and production tech stacks by allowing prompt writers to freely iterate on their prompts.
- LLM-oriented observability with detailed insights into each LLM interaction, like latency and token usage.
- Enhancement to Tool management that is responsible for tools registration, the publishing process, execution and observability.
Chain of Thought workflow
Chain of Thought is one of AI agent frameworks that enables LLMs to reason about issues.
We implemented the concept of Chain of Thought in the form of a workflow on Automation Platform v2 as shown below. The core idea of Chain of Thought is to use an LLM as the reasoning engine to determine which tools to use and in which order. Tools are the way an LLM interacts with the world to solve real problems, for example checking a reservation’s status or checking listing availability.
Tools are essentially actions and workflows, the basic building blocks of traditional products in Automation Platform v1. Actions and workflows work well as tools in Chain of Thought because of their unified interface and managed execution environment.
Figure 6 contains the main steps of the Chain of Thought workflow. It starts with preparing context for the LLM, including prompt, contextual data, and historical conversations. Then it triggers the logic reasoning loop: asking the LLM for reasoning, executing the LLM-requested tool and processing the tool’s outcome. Chain of Thought will stay in the reasoning loop until a result is generated.
Figure 7 shows all high-level components powering Chain of Thought:
- CoT (Chain of Thought) IO handler: assemble the prompt, prepare contextual data, collect user input and general data processing before sending it to the LLM.
- Tool Manager: prepare tool payload with LLM input & output, manage tool execution and offer quality of life features like retry or rate limiting.
- LLM Adapter: allow developers to add customized logic facilitating integration with different types of LLMs.
Context management
To ensure the LLM makes the best decision, we need to provide all necessary and relevant information to the LLM such as historical interactions with the LLM, the intent of the customer support inquiry, current trip information and more. For use cases like offline evaluation, point-in-time data retrieval is also supported by our system via configuration.
Given the large amount of available contextual information, developers are allowed to either statically declare the needed context (e.g. customer name) or name a dynamic context retriever (e.g. relevant help articles of customer’s questions ).
Context Management is the key component ensuring the LLM has the access to all necessary contextual information. Figure 8 shows major Context Management components:
- Context Loader: connect to different sources and fetch relevant context based on developers’ customizable fetching logic.
- Runtime Context Manager: maintain runtime context, process context for each LLM call and interact with context storage.
Guardrails framework
LLMs are powerful text generation tools, but they also can come with issues like hallucinations and jailbreaks. This is where our Guardrails Framework comes in, a safe-guarding mechanism that monitors communications with the LLM, ensuring it is helpful, relevant and ethical.
Figure 9 shows the architecture of Guardrails Framework where engineers from different teams create reusable guardrails. During runtime, guardrails can be executed in parallel and leverage different downstream tech stacks. For example, the content moderation guardrail calls various LLMs to detect violations in communication content, and tool guardrails use rules to prevent bad execution, for example updating listings with invalid setup.
What’s next
In this blog, we presented the most recent evolution of Automation Platform, the conversational AI platform at Airbnb, to power emerging LLM applications.
LLM application is a rapidly developing domain, and we will continue to evolve with these transformative technologies, explore other AI agent frameworks, expand Chain of Thought tool capabilities and investigate LLM application simulation. We anticipate further efficiency and productivity gains for all AI practitioners at Airbnb with these innovations.
We’re hiring! If work like this interests you check out our careers site.
Acknowledgements
Thanks to Mia Zhao, Zay Guan, Michael Lubavin, Wei Wu, Yashar Mehdad, Julian Warszawski, Ting Luo, Junlan Li, Wayne Zhang, Zhenyu Zhao, Yuanpei Cao, Yisha Wu, Peng Wang, Heng Ji, Tiantian Zhang, Cindy Chen, Hanchen Su, Wei Han, Mingzhi Xu, Ying Lyu, Elaine Liu, Hengyu Zhou, Teng Wang, Shawn Yan, Zecheng Xu, Haiyu Zhang, Gary Pan, Tong Chen, Pei-Fen Tu, Ying Tan, Fengyang Chen, Haoran Zhu, Xirui Liu, Tony Jiang, Xiao Zeng, Wei Wu, Tongyun Lv, Zixuan Yang, Keyao Yang, Danny Deng, Xiang Lan and Wei Ji for the product collaborations.
Thanks to Joy Zhang, Raj Rajagopal, Tina Su, Peter Frank, Shuohao Zhang, Jack Song, Navjot Sidhu, Weiping Peng, Kelvin Xiong, Andy Yasutake and Hanlin Fang’s leadership support for the Intelligent Automation Platform.
All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this website are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.
