# Monte Carlo, Puppetry and Laughter: The Unexpected Joys of Prompt Engineering

Источник: https://tech.instacart.com/monte-carlo-puppetry-and-laughter-the-unexpected-joys-of-prompt-engineering-4b9272e0c4eb

Monte Carlo, Puppetry and Laughter: The Unexpected Joys of Prompt Engineering
The universe of the current Large Language Models (LLMs) engineering is electrifying, to say the least. The industry has been on fire with change since the launch of ChatGPT in November of Last year. We’re all seeing the rise of AI tooling across the entire industry, and it’s opening up product and development possibilities at an astounding rate.
Instacart has been adopting LLMs and GenAI at a breakneck pace: just take a look at our internal assistant Ava, our superpowered AI search Ask Instacart, or the innovation in our ML Platforms. We’ve been exploring use cases, capabilities, and most importantly how to get value for our employees, customers, merchants, and shoppers.
Anyone who has worked with some of these models knows that this emerging tech has limitless possibilities; Possibilities that are currently constrained by a number of challenges: from context size issues, to hallucinations, to models that just don’t seem to be able to complete the tasks you set for them.
Fortunately, there are a number of techniques to help you in building products with LLMs. This article explores some of these techniques and, hopefully, really opens your mind to more possibilities!
A quick aside here: all of these prompt techniques have been implemented and used with GPT-4. Some have also been used with GPT-3.5. GPT-4 is currently the best-in-class conversational model, and is far superior to GPT-3.5 and all other conversational models. I highly recommend using GPT-4 if it at all makes sense economically for your use case.
This article will be an exploration of prompt techniques we’ve used for our internal productivity tooling at Instacart. These techniques are a combination of industry and academic research along with our own small-scale internal development efforts. It is recommended that you test these techniques out in your own evaluation environments and with your specific use cases.
The Power of Prompting
It’s a fascinating facet of working with Large Language Models — the concept of prompting. It’s our handshake with the model, the instrument through which we converse and interact with this AI entity. And, similar to the spice in your favorite recipe, the right prompting technique can transform the outcome notably. We’re going to cover some well known techniques here, skip ahead to see some of the more interesting techniques we’ve developed below.
First, let’s chat about a technique that sounds like it fell out of a cognitive science textbook: the Chain Of Thought (CoT). Chain of thought is a simple prompting technique that has very interesting implications we’ll get to in the next section. CoT takes several different forms, but one of the most popular is just adding the phrase “Let’s take this step by step” to the prompt. As with many of these techniques, it’s so simple that it feels silly. More recently “Take a deep breath and come up with a plan for answering”. The model doesn’t breathe any more than it can think deeply, but these phrases cue the model to think more and refine its position in the space of answers before committing to a direction.
Here is an example of using CoT to generate a title for an article you’ve fleshed out previously in the conversation (which is what I did for this article!):
Now we will generate a title for the article. First take it step
by step and determine what are the most important elements of the
article to include in the title and what makes a good title in general.
After you’ve done that, generate the title.
Another well-known prompt technique is ReAct. This is where you grant the model powers to take action outside of its own text generation flow. This could be looking up a webpage, performing a math calculation, or even looking up information in internal documentation sources. Generally you prompt the model with its abilities. Something like:
In answering the question below, you may also take the following actions to get more information:
In answering the question below, you may also take the following actions
to get more information:
INTERNAL_LOOKUP: <search terms> - perform a search across internal sources
GOOGLE_SEARCH: <search terms> - perform a web search for your terms
CALCULATION: <math terms> - Perform an arithmetic calculation i.e. 
CALCULATION: 2 * (8^10)
Actions must come at the end of your output, and you will be given the
result in response.  Please restate all information for the user.
Actions must come at the end of your output, and you will be given the result in response. Please restate all information for the user.
Now when the model responds it may use INTERNAL_LOOKUP, GOOGLE_SEARCH, or calculation, and our software will perform the action and re-ask the model to complete the task with the new information.
In this way we can build up a library of capabilities for the model. A more advanced form of this can be seen with ChatGPT’s plugin system.
Similarities between LLMs and Humans
Drawing parallels between human cognition and Large Language Models (LLMs) makes for an intriguing exploration. Often it’s uncanny how much an interaction with an LLM mirrors engaging with a bright but sleep-deficient intern. The latter requires clear, unambiguous instructions to churn out the desired output, as does an LLM. They both need guidance to stay on task, without veering off into the land of muddled responses or, for LLMs, hallucinations.
Just as with the human intern, LLMs too, benefit from space to err and self-correct. While anthropomorphizing LLMs can invite skepticism, it actually helps frame our interactions better, optimizing the chances of successful task completion. Here’s another strikingly ‘human’ element: an LLM, like an intern, when given the right nudges and course-corrections, can surprise you with a dose of unexpected humor or an astoundingly insightful response. The experience is exciting, unpredictable, and sometimes frustrating.
One example of this is using the phrase “Thank you” in few-shot learning examples. If you are polite to the model in your few shot examples it can help convey the correct meaning behind the next example. In few-shot learning we are providing 2–5 examples of output covering different cases. We’ve found that if you just do Question and Answer examples, sometimes the model gets confused and thinks the next Question is a correction to the previous answer rather than a new example. By saying “Thank you, that was great, the next question is:” it actually performs better than without. Literally “thank you” rather than other forms worked better in our tests!
When we reframe our perception of an LLM as an intern, it affords us a more pragmatic view of our prompts. Imagine how a person with a non-specialist, generalized education might approach your task, devoid of specific knowledge in your field. Upon reflecting and refining my own poorly behaving prompts, I found a trend. Treating the LLM as a bright yet often confused participant led me to rewrite the prompts, addressing the task requirements more overtly.
This change in perspective isn’t just theoretical; it has proven its value in both academic research and everyday prompt engineering encounters. By infusing a dose of humanity into our interactions with LLMs — treating them as well-intentioned but perhaps slightly befuddled — we can enhance their performance and our overall experience.
Advanced Prompting Techniques
We’re now going to cover some of the prompt techniques we’ve developed at Instacart. We don’t claim to be the only ones to come up with these, or even to be using the industry terms, but we have used all of these in developing the Ava family of products that we use for internal workflows. I’ve ordered this in increasing sophistication, so be sure not to miss Classifying and Puppetry!
Room for Thought — Make a Plan First
Room for thought is about explicitly encouraging the LLM to make a plan before starting to answer the question. This can be a pretty delicate balance of picking the right word. ChatGPT has, in particular, been trained with RLHF to answer the users question directly rather than waiting. Often you need to explicitly prompt the model to not answer the question. For instance, here is a section of the prompt we use to generate pull request (PR) titles and descriptions for internal code reviews.
First let’s create an outline for the pull request description.  Do not
generate a title and description, only write the outline. Be sure to think
about what the categories of the change are (i.e. 1. A change to add the
--foo argument, 2. Add retries for network calls, etc) based on what you
see in the diff.
This particular prompt also omits all formatting instructions for the output or how to select a title, for instance (we include these in follow up discussion in generating the PR).
This gives the model room to just think about how to best compose the pull request. Thinking about the model like a human, we’re just telling it to make a first draft or outline before actually writing the output.
Sometimes it can also be a good idea to prompt the model to think about what is important in good versions of the answers (“First list 5 things that make a good pull request”), though many times that kind of pre-thinking can just be built into the prompt, saving generation time. For instance:
A good pull request description is clear, concise, and fully lays out
the complex parts of the change. When composing a pull request
description, the best ones cite the changes with the description,but
also don't over describe small changes (especially one line changes).
Given this, create an outline for the pull request description, only
writing the outline
… etc …
In this way we’ve baked some of the thinking about “what makes a good pull request” into the prompt, and we don’t have to spend time or generation tokens on making this static list. We still want to give the model room to think about the pieces of the problem that are dependent on the specific query (the specific pull request changes in this example).
Monte Carlo — Brainstorm Options
In the Monte Carlo technique, we ask the model to generate several different options, and then use those options to create a final answer that brings the best aspects of all of the generated answers. You can see echoes of Room for Thought here, in that the model again has room to make mistakes, try different approaches, and only then create the output.
Monte Carlo is great for when you need to execute a creative process with the model. Thinking about how you try to approach creative problems with coworkers — first you brainstorm by listing ideas. Monte Carlo is the technique for doing it with the LLM.
Here is a prompt I recently used to generate ideas for my daughter’s birthday party, and create a final title from the ideas:
I am looking for ideas for my 9 year old's birthday party.  She is into
Pokemon, corgis, Roblox, and loves playing with her friends.
First list out elements of a good birthday party for a kid that can
be accomplished on a budget, and a list of fun themes/ elements of a
party given her interests.
Then create 5 radically different ideas for parties.
Finally create a final singular title recommendation that combines the
best elements of the options.
The best part of Monte Carlo is when you are doing it interactively, you get 5 additional options as part of the generation. Often I find one of the options in the list appeals to me, and I pick it. Note that specifying that the ideas should be as different as possible is a good idea, otherwise under some circumstances the model will repeat itself five times with slight wording variations.
Get Ben Bernard’s stories in your inbox
Join Medium for free to get updates from this writer.
I find this technique especially useful when generating ideas with humor. GPT-4 isn’t terribly good at humor or jokes, and so getting it to generate many options can be great for finding something that is actually funny.
Self Correction — Critique yourself
Self correction is about letting the model think about its answer and switch roles to thinking critically about what it could improve, then using those thoughts to inform its final answer. This works best with the Monte Carlo technique above, in that it can analyze each option and offer critiques. If you’ve also given guidance on what qualifies as a “good” response, you can ask it to keep those guidelines in mind as it offers its techniques.
Let’s try that PR title and description generation from above again, this time with self correction:
Now we will generate the title for the PR.  The title should succinctly
indicate what the pull request aims to do. Ideally, it should be a short
and clear description of the purpose of the pull request.
Generate 5 possible radically different titles and then critique them.
Finally generate a refined final title after the critique.
The important part here is “and then critique them”. By letting the model form critiques, you allow the model to improve on its observations. Again, when using a model interactively, you also get to peek into what the model is “thinking” as it forms these critiques and final answers.
Classifying — Only answer with a specific option
Classifying is an extremely interesting prompt technique that taps into some of the lesser-used features of LLMs. One problem that you can encounter with LLMs is the desire to ask the model to answer essentially a multiple choice question. With a standard prompt, you can run into a lot of problems with the model wanting to think about its answer first, or prefixing answers with header information (“The answer to your question is A” instead of just saying “A”). When using the output of LLMs programmatically it can be very difficult to extract the correct output from the LLM.
We’ve built an API endpoint on our internal OpenAI / LLM proxy that guarantees valid output. A key insight that enables this API is the LLM’s ability to repeat tags from the context in the answer reliably. Given that capability, we can craft a prompt like so:
Consider the following statement carefully and think through your
reasoning before answering:
The sky is blue.
Possible Answers:
000 True
001 False
002 Uncertain
Answer the question by directly referencing the number of the answer.
While this makes it easier to process the model’s output, simply using the prompt above introduces the problems we’ve discussed earlier. LLMs function by generating the next most likely token, a term which here refers to a character or word fragment, from a provided input. Calculating the probability of every potential next token, they select the one with the greatest likelihood. We can nudge that probability by using the logit_bias parameter in our request to OpenAI, and if we set the bias to 100, we can force the model to choose from a specific set of tokens. Once we’ve limited the model’s responses to ‘000’, ‘001’, ‘002’, etc., we ask it to generate a single token (by setting max_tokens to 1), ensuring our answer is always a valid option. It’s worth noting that all three-digit numerical combinations are considered single tokens.
But wait– what about Room for Thought, CoT, and all the other techniques for giving the model room to make the right decision? Our API actually allows a “deep thought” mode where it can do CoT and other “out loud” thinking by asking it first to think through the reasoning but not supply the answer, and then in a later round using logit_bias to force a final answer. Generally, using multiple rounds of prompting in a conversation style can allow the application of multiple techniques.
Let’s think about how that might work, with an example. Say you wanted to pick the correct title from the list of options we generated above for the pull request. Instead of generating a final title, we want to get the model to pick the best one it generated, and we want to force it to pick one and only one object, but we want to give it Room for Thought and Self Critiquing capabilities, we could do it like so:
Message 1:
Consider the following question carefully and think through your reasoning before answering:
Which of the titles below make the best pull request title, given these changes:
CHANGE
Be sure to take a deep breath and think through your answer
Possible Answers:
000 The best PR EVAR!!!
001 Adding CRUD endpoints
002 Adding POST and DELETE handlers for /api/books
You will first carefully consider the question and write down a bulleted list of thoughts that will lead me to an answer.
The model responses with its reasoning, then we say:
Message 2:
Thank you. Now please identify the answer that best matches the
reasoning above.
Just reference the item number from the answer list above.
The first completion asks for a normal response with full access to all the tokens. Only the response to the second message is limited to only the answer tokens. Also note that it takes some tinkering to get the correct prompting, as we’ve seen small word changes (for instance: removing the “Thank you”) cause large differences in fidelity of responses.
A note about this technique: we recommend a lower temperature (even 0) when classifying. Temperature represents how likely the model is to choose a token that isn’t the “most likely” token in its next generation cycle. In our case, we probably always want the most likely token. Another thing is that it can be important, depending on your question, to allow the model an out in your choices. “Uncertain” above is an example of this. But also “none” or “Nothing to do” can be appropriate in other circumstances.
Puppetry — Speaking for the model
This is my favorite prompt technique of all. I’ll note we aren’t the only ones to come up with this technique.
In almost all LLM APIs, you pass in the conversation state to each generation call. You have to pass in text / json that shows what the user said, what the assistant said, and what the system said. The interesting part is that you can tell the assistant that it has already started responding even if it didn’t. You can tell it that it said anything you want. This is commonly used in few-shot prompting already, but you can also use this to short-circuit the model’s tendency to ramble or answer weirdly when you need specific format of output, or even thinking.
For instance, when we want the model to output a JSON object for the pull request script, we do this:
User: Finally output the title and description according to the
below JSON format, it is very important to follow the format below exactly.
{
"title": "<title>",
"description": "<description">,
}
Assistant: {
"title": "
Note the addition of the last two lines in this prompt. In this way we are fooling the model into thinking that it already started by outputting a “{“ character, and therefore should be “thinking in json”. We also don’t let it guess on the “title” key and prompt it to already begin the title. This decreases the burden on the model to start its response in the exact format you want for your output. It makes the model relax a little bit and just output the answer you want. (In the above example User: and Assistant: refer to Roles in the OpenAI API)
We call this puppetry because you’re forcing the model to say the exact things you want it to. The model sees that and interprets it as having already said it. Then, in order to not contradict itself, it continues the thought from there.
This can also be used to get the LLM to to follow your prompting rules, like if you conclude a prompt with:
Assistant: First, I will think through the options, identifying the good
pieces of each approach.
In this case, we’re reminding the model that it is thinking through things before answering.
Conclusion
We’ve shared with you some of the techniques we’ve come up with, and would love to hear about any techniques you discover for yourself! Ada Cohen and Kevin Lei were instrumental in writing this article and coming up with these techniques.
Happy prompting!
Additional Reading
This is built off a ton of papers and popular articles and resources. Here are some we think are particularly good to read up on, if you’re looking for more information
- The Prompt Engineering guide — https://www.promptingguide.ai/
- Anthropic’s Guide to prompt design and useful prompt hacks
- Dair.ai’s Prompt guide: https://github.com/dair-ai/Prompt-Engineering-Guide
- Chain of Density Paper — a prompt technique for summarization
- OpenAI’s cookbook — especially Techniques to Improve Reliability
- Reduce fake facts with “according to”
- React Pattern for Python
