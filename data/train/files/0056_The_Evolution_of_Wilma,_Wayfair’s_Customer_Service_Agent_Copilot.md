# The Evolution of Wilma, Wayfair’s Customer Service Agent Copilot

Источник: https://www.aboutwayfair.com/careers/tech-blog/the-evolution-of-wilma-wayfairs-customer-service-agent-copilot

When one of our customers has an issue with a product they purchased, they have the option to chat with a customer service agent. Our agents are expected to arrive at a resolution to the customer's issue that balances the customer’s needs with Wayfair’s business needs, all while maintaining a friendly and empathetic attitude. Navigating an interaction with a customer while adeptly applying one of hundreds of Wayfair policies is challenging!
To help the customer service agent with this task, we developed a system called Wilma (Wayfair Integrated Language Model Application). Wilma uses large language models (LLMs) like Gemini and GPT to draft messages for agents to review and edit before sending to the customer. Wilma helps agents respond quickly and empathetically to customers while adhering to Wayfair’s guidelines and maintaining customer satisfaction. Agents using Wilma are able to address customers’ needs 12% faster and adhere to Wayfair’s customer policies between 2% and 5% more, depending on issue type. Agents especially appreciate Wilma during peak shopping season as it allows them to keep up with the high volume of customer contacts.
How Does Wilma Work?
An agent uses Wilma to create a response to send to a customer by taking the following steps:
- The agent clicks a button to select what they want Wilma’s help with (Discovery, Resolution, Empathy, or Give Me a Minute).
- A prompt template is selected based on which button the agent clicked, some business logic, and the analysis of a routing LLM.
- The prompt template is filled in with real-time customer, order, and product information that is pulled from Wayfair’s systems.
- The LLM generates a response using the filled in prompt template.
- The response is checked for appropriateness, information is added, and the final output is delivered back to the agent.
- The agent is now free to use, edit, or not use the message, as they see fit.
How Are Prompts Structured?
Wilma currently has over 40 different prompt templates. We use Jinja to render the prompt templates, allowing us to dynamically generate the prompt’s text based on data retrieved from Wayfair’s systems. Prompts are structured to have sections for the task description, tone, few-shot examples, and additional instructions.
How Has Wilma Evolved?
Wilma has evolved significantly since it first launched in 2023. Collecting data and receiving feedback from agents and customers has shown us many ways to improve. The two most significant changes were moving from one prompt to many prompts and moving from one LLM call to many LLM calls.
Multiple Prompts: In the first version of Wilma, we put all the instructions in one long prompt triggered by a single “Help Me Write It” button in the user interface. We found two things wrong with this approach:
- The LLM often got confused by all the content in the prompt and would follow examples and instructions that were irrelevant to the current situation.
- The agents felt they lacked control over the direction of the conversation.
Now we have four buttons in the user interface, allowing the agents to have finer-grained control over the conversation flow, and over forty tailored prompts, each providing the LLM with only the information it needs at that point in the conversation.
Multiple LLM Calls: Resolution negotiation with a customer is especially tricky for an LLM. Over a long conversation, an LLM could get confused about which options had already been discussed and sometimes offer inappropriate resolutions such as replacement parts for a pillow. To address these issues, we now use a series of LLM calls to analyze the conversation before generating a response.
- The routing LLM identifies if we are in a negotiation situation.
- The proposal LLM identifies resolutions that have already been proposed.
- The suitability LLM decides which resolutions are reasonable to offer.
- The current resolution LLM identifies what resolution is on the table, who proposed it, and if it has been accepted or rejected.
When we switched to this framework we saw significantly improved behavior during resolution negotiation and far fewer embarrassing mistakes.
The Future of Wilma
Right now the burden is still on the customer service agent to decide when and how to use Wilma. As we continue to refine Wilma’s behavior, our hope is to automate the “easy” parts of the conversation with the customer, freeing our agents to focus on the truly challenging problems that require their expertise. In the long term, we envision our agents supervising multiple simultaneous AI-driven conversations, acting as a manager who only steps in when needed.
The authors would like to acknowledge and thank Farshid Bahrami, Graham Ganssle, Eric Lee, and Shashank Menon for their contributions to Wilma.
