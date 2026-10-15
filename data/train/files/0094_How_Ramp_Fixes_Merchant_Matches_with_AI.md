# How Ramp Fixes Merchant Matches with AI

Источник: https://engineering.ramp.com/post/fixing-merchant-classifications-with-ai

Automatically matching transactions to merchants helps us save our customers time and money. Merchant matching—also called classification or mapping—enables our customers to perform actions such as analyzing spending by merchant and setting up merchant restricted funds. Ramp's automatic matching of transactions to merchants works quite well, but is not perfect.
Incorrect merchant matches frustrate our customers. Suppose you are planning a work trip. You book a room at a small hotel on your Ramp card using a travel fund. But then, Ramp classifies the hotel as an entertainment merchant and now the expense is flagged as out of policy. This is because your travel fund only covers lodging merchants. Now, on top of travel related stress, you must contact your finance team, who may escalate to Ramp support to get this fixed. While there are instances where our merchant matching should have acted correctly, many times the matcher's input is simply not sufficient to make a perfect match.
Even large tech companies struggle with matching problems. For example, if you search for Ramp engineer Nithiwat Seesillapachai, you would expect to find a picture of him. Instead, at the time of writing, you will find pictures of other people including one of his former reports: Calix Huang.
An example of a Google image match gone wrong.
To resolve issues like the "entertainment" hotel, Ramp users are able to go to a transaction and request a merchant classification to be fixed by providing a new merchant name, website, and category.
How Ramp users can report incorrect merchant classifications.
In the past, these reports were serviced by a combination of customer support, finance, and engineering teams and would take hours of employee time.
💡 The problem of fixing merchant classifications scales proportionally with the number of Ramp card transactions. A manual approach to handling these requests simply is not sustainable as we grow.
We solve this problem using an AI agent consisting of a large language model (LLM) backed by embeddings and rapid online analytical processing (OLAP) queries, multimodal retrieval augmented generation (RAG), and a set of carefully constructed guardrails.
We have been monitoring our agent's performance on incorrect merchant reports for several months. It acts properly on nearly all of them. Instead of waiting for hours for manual human intervention, our customers are unblocked by our agent in less than 10 seconds. Furthermore, this agent unlocks our potential to more easily 100X our transactions without worrying about 100Xing our customer support staff.
Before we show how we fix merchant classifications, we clarify what we mean by mapping a transaction to a merchant and why it is hard to get right based on the input we have to work with.
When a user makes a transaction on their Ramp card, a payment processor, such as Stripe, sends us information in the card acceptor. The card acceptor contains transaction metadata including a name field to indicate the name of the business the user transacted with. However, this name is not what you would expect. For example, Bryant Park transactions may have a name like PTI*BRYANTPARKWV.
A merchant at Ramp can be thought of as a more useful, enriched, representation of the card acceptor data of a transaction. Ramp merchants include a more user friendly name, website, category, and logo. It is also important to note that Ramp merchants typically encompass multiple card acceptors.
The figure below shows some transactions' card acceptors and their mapped Ramp merchants.
Examples of card acceptors and their merchant matches on Ramp.
Enriching transaction data is a well-known problem. Here is a Starbucks enrichment example from Spade.
Mapping a transaction to a merchant can be done using the card acceptor name in addition to other card acceptor information such as:
Merchant Category Code (MCC): intended to describe the nature of the business, but can be misleading for businesses that offer multiple services.
Example: A hotel may offer lodging, food, and entertainment services.
Location information: can be the location of the business, but gets more complicated with online transactions.
Example: A transaction to book an Amtrak train trip between Boston and New York City can have a card acceptor location of Washington, D.C.
Illustration of the difficulty matching `SERVICE FEE` to the right government merchant.
There are various scenarios where merchant matching is quite difficult, even if a knowledgeable person was doing it by hand.
Scenario 1: The card acceptor name is very vague. A card acceptor name of SERVICE FEE has been observed in transactions with government agencies. These transactions cannot be distinguished based on MCC—since they are all government services— and card acceptor location information is not reliable.
Scenario 2: The card acceptor name remains the same for a merchant that rebranded in some way or it was changed as part of a rebranding. We observed the latter when Listening rebranded from Listening.io to Listening.com. As a part of this, the card acceptor changed in the same way.
User context is sometimes the only way to map a transaction to a merchant unambiguously. Card acceptor data alone is insufficient and can lead to our initial merchant classification being incorrect. As a result, we allow users to request our agent to fix these classifications.
When the user supplies a new merchant name, website, and category to fix a merchant classification, the agent's LLM must choose how to respond. In particular, the LLM has to map the user input to a resolution action.
Given the merchant name, website, and category a user provides in the UI, the LLM needs to map this request to an action.
Solving this problem with just the user's information would be extremely difficult. Consider the 'Praivi' example above:
We must also limit what the LLM can do. For example, we do not want the LLM to change our Amazon merchant record to have the website www.google.com.
We remedy these issues as follows:
🔨 We intelligently build up context for our LLM so that it can make an informed decision.
🚧 We put guardrails around what the LLM can do based on the nature of the request and the merchant involved.
To map a request to an action, we must determine whether the user's request is reasonable. The LLM uses three parts of its context to guide this decision:
Transaction card acceptor name and MCC.
Extracted merchant names, addresses, and line items from related receipt images.
User-provided memos for related transactions.
Below is part of the rationale provided by our LLM for a user requesting to change a transaction from the "Four Points by Sheraton" hotel to the "Four Points Service Station" gas station.
The original transaction information [has] an MCC code of 5541, which corresponds to a fuel and gas station. … Upon reviewing the merchant information from receipts with the same transaction card acceptor, the most prevalent inferred merchant name is "FOUR POINTS STOP," which aligns with the updated merchant name suggestion. The line items and memos from these receipts also indicate purchases typical of a fuel and gas station, such as ice, regular fuel, and snacks.
Here we can see that the LLM uses the MCC, receipt information, and memos as strong signals that the user's request is legitimate. The original merchant misclassification was likely caused by the acceptor name being (the vague) FOUR POINTS.
It is also important to recognize LLMs' knowledge that has been distilled as part of their training. This has proven useful in solving rebranding cases. The following snippet is from our agent's LLM identifying such a rebrand (merchant names have been changed).
HarperGray officially rebranded to Clarity in April 2023, maintaining the same corporate entity and business operations. The website domain change from harpergray.com to clarity.com confirms this corporate transition. The merchant category remains unchanged as Professional Services. The similar merchant example (Harper Restaurant) is clearly a different business in the restaurant industry. Given this is a legitimate corporate rebranding, the [classification] request should be executed to reflect the company's current official name and website.
If a request is reasonable, the LLM must choose an action:
➕ Create a new Ramp merchant.
🔧 Update an existing merchant.
↔️ Reassign the transaction to a more fitting merchant.
We provide the LLM with related existing merchants so it can choose the right action. Giving it every Ramp merchant does not scale and would overload the LLM's context window. Instead, we use a RAG approach to fetch K related merchants. Suppose the user enters the merchant name Sandie Hill Flowers and the card acceptor name is SAND*HIL 0012.
Example illustration of why we need to intelligently pull related merchants using a RAG approach.
We pull merchants that are similar to the transaction using vector embedding similarity and merchants whose names roughly match the requested merchant name. Transaction embeddings come from transaction card acceptor names. Merchant embeddings come from the acceptor names of mapped transactions. We have used transaction level embeddings in other work and Stripe has also recently reported using transaction embeddings.
It is critical that we use both merchants from searching embeddings and merchants that match the requested name because the card acceptor name—the basis of the embeddings—can be different from the merchant's actual name. For example, the card acceptor name could be as vague as SERVICE FEE. Therefore, we also pull merchants using the user's requested merchant name.
By bringing in merchants using these two strategies, the LLM can inspect the names, websites, and categories of a good selection of merchants. It can then decide whether to create a new merchant or modify existing ones.
We allow the LLM to take only one of a select set of actions because modifying Ramp's merchant records correctly is not straightforward. The LLM can take a low impact action on nearly all requests. We carefully choose when the LLM is able to take an action with high impact.
We also have post-processing guardrails to catch LLM hallucinations. The figure below shows two types of LLM hallucinations we observed.
Illustration of possible LLM hallucinations.
We require that the LLM always chooses one of the provided actions. This is crucial to ensure the guardrails discussed above work. For example, if the LLM was restricted from changing the Amazon merchant, we want to ensure it did not.
Similarly, if the LLM chooses to reassign a transaction to another merchant, the target must be in the supplied list. Otherwise, the LLM may be moving transactions to an inappropriate merchant.
If the LLM hallucinates, we inform it of its mistake and have it retry until we get a valid response.
When our LLM takes an action that modifies the transaction's merchant classification in some way, the user will observe a change on the front end in seconds. For example, if the transaction is moved to a new merchant, the new merchant name will appear. But what if the LLM rejects the request?
Initially, we showed nothing, but users were rightfully confused:
We take our primary LLM's rejection reasoning and then use a second LLM to rewrite it in plain language. This will soon be returned to the front end so users get a clear, timely explanation of why their request was rejected.
We have evaluated our agent in four phases during development and rollout:
Our first form of evaluation was to manually review LLM responses on a few select users and transactions. We believe this is the best first evaluation strategy for multiple reasons:
We can determine whether an LLM can solve the problem.
Human evaluation is necessary for this problem given its complexity and requirement of Ramp background knowledge.
We can focus on improving the LLM's use—the prompt, context, guardrails—instead of deriving and implementing rigorous evaluations.
It is feasible at ~tens of requests per day.
Once we started rolling out our agent to more users, we could no longer manually review every request. However, we still wanted to focus on feature development as opposed to building a serious evaluation flow.
If the agent acted properly, the user is unlikely to report incorrect merchant information again, similar to how people typically only leave reviews on sites like Google or Yelp when they have a bad experience. Therefore, we can use the lack of a followup request as a signal that the LLM acted properly on the initial request.
This evaluation is very easy to setup and allowed us to identify the requests that would be useful to manually review.
Around the same time, we collected how often requests are rejected. If we assume that users are generally using the tool appropriately, we expect a low rejection rate. This evaluation is also easy to setup and enables focused manual review.
Once we were confident with our agent and began to roll out to more and more customers, we needed an evaluation strategy that satisfied two requirements:
Inspired by previous, heavily cited work that has demonstrated that state of the art LLMs are reliable evaluators, we use an LLM as a judge:
💡 By using an LLM for evaluation, we can scale to a high number of requests while providing a stronger signal of our agent's success at acting on a user's request.
As an added bonus, we can evaluate our agent when it runs in shadow mode. By "shadow mode", we mean the agent just tells us what it would do instead of taking any action. Given the context and what the LLM would do, we can mimic what would appear to a user and pass that into our LLM judge. We used this to see how our agent would behave on customers' transactions before actually rolling it out to those customers.
| Strategy | Signal of Correctness | Scalability | Impact on Development | 
|---|---|---|---|
| Manual Evaluation | Very Strong 💪 | Not Scalable | Rapid Iteration 🚀 | 
| Count Repeated Requests | Strong | Scales ✅ | Easy to Set Up | 
| Count Rejections | Strong | Scales ✅ | Easy to Set Up | 
| LLM Judge | Very Strong 💪 | Scales ✅ | Requires Cycles ⏳ | 
Table summarizing the main pros and cons of our four evaluation strategies.
Fewer than 10% of the transactions ever receive a second correction request and only 1 out of 4 requests are rejected by our agent.
Figure showing the proportion of transactions that receive multiple requests.
Figure showing the proportion of requests that are rejected by our agent.
According to our judge, our agent improves nearly 99% of transaction classifications and nearly two thirds of rejections are reasonable. It is worth noting that our weaker signal evaluations—followup and rejection rates—are supported by our judge.
Our key evaluation metrics demonstrating the success of our agent.
It would be reasonable to ask: why are nearly two thirds of user requests being reasonably rejected?
Reasonable rejections happen for a couple of reasons:
The agent delivers three key benefits:
😄 We improve Ramp customer satisfaction by quickly resolving more incorrect merchant information requests and constantly improving our merchant database.
Before: Customer support and engineering teams were able to service only 3% of requests in 2023 and 1.5% in 2024. As Ramp grows, these percents will only go down.
Now: Our agent handles close to 100% of requests 📈.
💰 We rapidly unblock our customers at a small cost to Ramp.
Before: Teams took hours to solve requests. This kept our customers blocked and cost Ramp hundreds of dollars.
Now: Our agent handles requests in under 10 seconds 🚄, instantly unblocking customers and costing Ramp cents.
🔎 By monitoring incorrect merchant information requests, we are monitoring the quality of both our transaction classification flow and merchant database.
We have extended the RAG-plus-LLM flow to two other merchant mapping problems:
Extension 1: The first is an internal, batch version of the above flow. Given an existing Ramp merchant that may have miscategorized transactions, we use an LLM with the proper context to map those transactions out of the merchant to more appropriate ones.
Illustration of how transactions are mapped to more appropriate merchants.
Extension 2: The second extension relates to matching transaction information in credit card statements to existing Ramp merchants. This is extremely valuable both internally and externally.
Illustration of mapping transactions on a credit card statement to Ramp merchants.
Matching transactions to merchants is hard given the limited information in the card acceptor data we receive from payment processors. Using an LLM wrapped in guardrails and supplied with powerful context, we have created an effective self-serve tool for our customers to fix merchant classifications. This has already saved both them and us time and money.
However, we are always looking to save even more. The success of our RAG-plus-LLM approach has led us to extend it to other merchant matching applications and we are sure more opportunities are around the corner.
